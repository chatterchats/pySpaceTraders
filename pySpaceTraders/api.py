import json
import math
import os.path

from pySpaceTraders.models import agents, contracts, factions, errors
from pySpaceTraders.models.enums import FactionSymbol, TradeSymbol
from pySpaceTraders.utils.pySpaceLogger import PySpaceLogger
from pySpaceTraders.utils.pySpaceParsers import PySpaceParser
from pySpaceTraders.utils.pySpaceRequest import PySpaceRequest


class Client:
    """SpaceTraders API Client Handler"""

    def __init__(
        self,
        agent_symbol: str,
        agent_faction: FactionSymbol = FactionSymbol.COSMIC,
        agent_email: str = "",
        log: bool = True,
        debug: bool = False,
    ):

        # Logging
        self.log: bool = log
        if self.log:
            self.logger = PySpaceLogger("pySpaceTraders", debug=debug)

        # Agent Data
        self.agent_symbol: str = agent_symbol.upper()
        self.agent_faction: FactionSymbol = agent_faction
        self.agent_email: str = agent_email if agent_email else ""

        # Initialize
        self.request = PySpaceRequest(logger=self.logger if self.log else None)
        self.parser = PySpaceParser(self)

        # Token and Login
        self.token: str = ""
        self._login()
        self.request.set_token(self.token)

        self.logger.info("Init complete")

    def _login(self):
        """Login to SpaceTraders.
        Looks for token.json, and checks if same"""
        loaded = False
        if os.path.isfile("tokens.json"):
            self.logger.debug("tokens.json present")
            with open("tokens.json", "r") as f:
                data = json.load(f)
                if self.agent_symbol in data.keys():
                    self.logger.debug("agent symbol present in tokens.json")
                    self.token = data[self.agent_symbol]["token"]
                    loaded = True

        if not loaded:
            self._register()

    def _register(self):

        self.logger.debug("Check Agent Symbol and Faction Validity")
        # Check validity of agent symbol
        if 3 < len(self.agent_symbol) > 14:
            raise ValueError(
                f"Agent Symbol `{self.agent_symbol}` has a length of {len(self.agent_symbol)}. Length must be >= 3 and <=14."
            )

        # Make sure faction_dict is recruiting
        factions_list = self.list_factions(all_factions=True)
        if type(factions_list) is factions.ListResponse:
            for faction in factions_list.factions:
                if faction.symbol == self.agent_faction and not faction.isRecruiting:
                    raise ValueError(f"`{self.agent_faction.value}` Faction is not recruiting new agents at this time.")

        self.logger.debug("Agent Symbol and Faction Valid")
        json_data = {
            "symbol": self.agent_symbol,
            "faction_dict": self.agent_faction.value,
        }

        if self.agent_email:
            json_data["email"] = self.agent_email

        register = self.request.api("POST", "https://api.spacetraders.io/v2/register", payload=json_data)

        if "data" in register.keys():
            self.logger.debug("Register Successful")
            self.token = register["data"]["token"]
            with open("tokens.json", "r") as f:
                self.logger.debug("Reading tokens.json")
                data = json.load(f)
            with open("tokens.json", "w", encoding="utf-8") as f:
                self.logger.debug("Writing new token to tokens.json")
                data[self.agent_symbol] = {"token": self.token}
                json.dump(data, f, indent=4, ensure_ascii=False)
        elif "error" in register.keys():
            self.logger.error("Error with registering.")
            return self.parser.error(register)

    def status(self):
        """Server Status and Announcements."""
        response = self.request.api("GET", "/")
        return self.parser.status(response)

    # Agent Endpoints #
    def my_agent(self) -> agents.Agent | errors.Error:
        """Fetch your agent's details"""
        response = self.request.api("GET", "/my/agent")
        if "error" in response.keys():
            return self.parser.error(response)
        return self.parser.agent(response)

    def list_agents(
        self, limit: int = 20, page: int = 1, all_agents: bool = False
    ) -> agents.ListResponse | errors.Error:
        """List all_factions agents. (Paginated)"""
        # token optional for get_agent
        query = {"limit": limit, "page": page}
        response = self.request.api("GET", "/agents", query_params=query)
        response["meta"]["pages"] = math.ceil(response["meta"]["total"] / limit)
        if all_agents and response["meta"]["pages"] > 1:
            for next_page in range(2, int(response["meta"]["pages"]) + 1):
                query["page"] = next_page
                additional_response = self.request.api("GET", f"/agents", query_params=query)
                response["data"].extend(additional_response["data"])
            response["meta"]["page"] = 1
            response["meta"]["limit"] = len(response["data"])
        if "error" in response.keys():
            return self.parser.error(response)
        return self.parser.agent_list(response)

    def get_agent(self, symbol: str = "CHATS") -> agents.Agent | errors.Error:
        """Fetch single agent details."""
        # token optional for get_agent
        response = self.request.api(
            "GET",
            f"/agents",
            symbol,
        )
        if "error" in response.keys():
            return self.parser.error(response)
        return self.parser.agent(response)

    # Contracts Endpoints #
    def list_contracts(
        self, limit: int = 20, page: int = 1, all_contracts: bool = False
    ) -> contracts.ListResponse | errors.Error:
        """Paginated list all contracts agent has (Paginated)"""
        query = {"limit": limit, "page": page}
        response = self.request.api("GET", f"/my/contracts", query_params=query)
        if "error" in response.keys():
            return self.parser.error(response)

        response["meta"]["pages"] = math.ceil(response["meta"]["total"] / limit)

        if all_contracts and response["meta"]["pages"] > 1:
            for next_page in range(2, int(response["meta"]["pages"]) + 1):
                query["page"] = next_page
                additional_response = self.request.api("GET", f"/my/contracts", query_params=query)
                response["data"].extend(additional_response["data"])
            response["meta"]["page"] = 1
            response["meta"]["limit"] = len(response["data"])
        response["contracts"] = [self.parser.contract(single_contract) for single_contract in response["data"]]
        response.pop("data")
        # TODO: Implement Parse Contract List
        return self.parser.contract_list(response)

    def get_contract(self, contract_id: str) -> contracts.Contract | errors.Error:
        """Fetch single contract details"""
        # token optional for get_agent

        response = self.request.api("GET", f"/my/contracts/{contract_id}")
        if "error" in response.keys():
            return self.parser.error(response)
        return self.parser.contract(response)

    def accept_contract(self, contract_id: str) -> contracts.ContractAgent | errors.Error:
        """Accept a contract."""

        response = self.request.api("POST", f"/my/contracts/{contract_id}/accept")

        if "error" in response.keys():
            return self.parser.error(response)

        return self.parser.contract_agent(response)

    def deliver_contract_cargo(
        self, contract_id: str, ship_symbol: str, trade_symbol: TradeSymbol, units: int
    ) -> contracts.Deliver | errors.Error:
        """Deliver cargo for a given contract."""
        payload = {
            "shipSymbol": ship_symbol,
            "tradeSymbol": trade_symbol,
            "units": units,
        }
        response = self.request.api("POST", f"/my/contracts/{contract_id}/deliver", payload=payload)
        if "error" in response.keys():
            return self.parser.error(response)

        return self.parser.contract_cargo(response)

    def fulfill_contract(self, contract_id: str) -> contracts.ContractAgent | errors.Error:
        """Fulfill (complete) a contract."""
        response = self.request.api("POST", f"/my/contracts/{contract_id}/fulfill")
        if "error" in response:
            return self.parser.error(response)

        return self.parser.contract_agent(response)

    # Faction Endpoints #
    def list_factions(
        self, limit: int = 20, page: int = 1, all_factions: bool = False
    ) -> factions.ListResponse | errors.Error:
        """List factions in the game. (Paginated)"""
        query = {"limit": limit, "page": page}
        response = self.request.api("GET", f"/factions", query_params=query)
        if "error" in response.keys():
            return self.parser.error(response)
        response["meta"]["pages"] = math.ceil(response["meta"]["total"] / limit)
        if all_factions and response["meta"]["pages"] > 1:
            for next_page in range(2, int(response["meta"]["pages"]) + 1):
                query["page"] = next_page
                additional_response = self.request.api("GET", f"/factions", query_params=query)
                response["data"].extend(additional_response["data"])
            response["meta"]["page"] = 1
            response["meta"]["limit"] = len(response["data"])

        return self.parser.faction_list(response)

    def get_faction(self, faction_symbol: FactionSymbol) -> factions.Faction | errors.Error:
        """View the details of a faction."""
        response = self.request.api("GET", f"/factions/{faction_symbol}")
        if "error" in response:
            return self.parser.error(response)

        return self.parser.faction(response)
