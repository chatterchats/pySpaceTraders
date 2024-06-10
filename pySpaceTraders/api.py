import json
import math
import os.path
from typing import List
from pySpaceTraders.models import agent
from pySpaceTraders.models.factions import Faction
from pySpaceTraders.utils.pySpaceLogger import PySpaceLogger
from pySpaceTraders.utils.pySpaceParsers import *
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
        self.agent_email: str = agent_email if agent_email else None

        # Initialize
        self.request = PySpaceRequest(logger=self.logger if self.log else None)

        # Token and Login
        self.token: str = ""
        self.__login()
        self.request.set_token(self.token)

        self.logger.info("Init complete")

    def __login(self):
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
            self.__register()

    def __register(self):

        self.logger.debug("Check Agent Symbol and Faction Validity")
        # Check validity of agent symbol
        if 3 < len(self.agent_symbol) > 14:
            raise ValueError(
                f"Agent Symbol `{self.agent_symbol}` has a length of {len(self.agent_symbol)}. Length must be >= 3 and <=14."
            )

        # Make sure faction is recruiting
        factions_list = self.list_factions(all_factions=True)

        for faction in factions_list:
            if faction.symbol == self.agent_faction and not faction.isRecruiting:
                raise ValueError(
                    f"`{self.agent_faction.value}` Faction is not recruiting new agents at this time."
                )

        self.logger.debug("Agent Symbol and Faction Valid")
        json_data = {"symbol": self.agent_symbol, "faction": self.agent_faction.value}

        if self.agent_email:
            json_data["email"] = self.agent_email

        register = self.request.api(
            "POST", "https://api.spacetraders.io/v2/register", payload=json_data
        )

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
            print(register)
            return parse_error(register)

    def status(self):
        """Server Status and Announcements."""
        response = self.request.api("GET", "/")
        return parse_status(response)

    # Agent Endpoints #
    def my_agent(self) -> agent.MyAgent:
        """Fetch your agent's details"""
        response = self.request.api("GET", "/my/agent")
        if "error" in response.keys():
            return parse_error(response)
        return agent.MyAgent(**response["data"])

    def list_agents(self, limit: int = 10, page: int = 1) -> agent.ListResponse:
        """List all_factions agents. (Paginated)"""
        # token optional for get_agent
        query = {"limit": limit, "page": page}
        response = self.request.api("GET", "/agents", query_params=query)
        if "error" in response.keys():
            return parse_error(response)
        response["data"] = [
            agent.Agent(**agent_token) for agent_token in response["data"]
        ]

        return agent.ListResponse(**response)

    def get_agent(self, symbol: str = "CHATS") -> agent.Agent:
        """Fetch single agent details."""
        # token optional for get_agent
        response = self.request.api(
            "GET",
            f"/agents",
            symbol,
        )
        if "error" in response.keys():
            return parse_error(response)
        return agent.Agent(**response["data"])

    # Contracts Endpoints #
    def list_contracts(self, limit: int = 10, page: int = 1):
        """Paginated list all_factions of your contracts. (Paginated)"""
        query = {"limit": limit, "page": page}
        response = self.request.api("GET", f"/my/contracts", query_params=query)
        if "error" in response.keys():
            return parse_error(response)
        response["contracts"] = [
            parse_contract({**single_contract, "ApiInstance": self})
            for single_contract in response["data"]
        ]
        response.pop("data")
        return response

    def get_contract(self, contract_id: str) -> contract.Contract:
        """Fetch single contract details"""
        # token optional for get_agent

        response = self.request.api("GET", f"/my/contracts/{contract_id}")
        if "error" in response.keys():
            return parse_error(response)
        return parse_contract({**response["data"], "ApiInstance": self})

    def __accept_contract(self, contract_id: str) -> contract.ContractAgent:
        """Accept a contract."""

        response = self.request.api("POST", f"/my/contracts/{contract_id}/accept")

        if "error" in response.keys():
            return parse_error(response)
        if "data" in response.keys():
            response = response["data"]
            return contract.ContractAgent(
                **{
                    "agent": agent.MyAgent(**response["agent"]),
                    "contract": parse_contract(
                        **{**response["contract"], "ApiInstance": self}
                    ),
                }
            )

    def __deliver_contract_cargo(
        self, contract_id: str, ship_symbol: str, trade_symbol: TradeSymbol, units: int
    ) -> contract.DeliverResponse:
        """Deliver cargo for a given contract."""
        payload = {
            "shipSymbol": ship_symbol,
            "tradeSymbol": trade_symbol,
            "units": units,
        }
        response = self.request.api(
            "POST", f"/my/contracts/{contract_id}/deliver", payload=payload
        )
        if "error" in response.keys():
            return parse_error(response)
        return contract.DeliverResponse(
            **{
                "contract": parse_contract(response["data"]["contract"]),
                "cargo": parse_cargo(response["data"]["cargo"]),
            }
        )

    def __fulfill_contract(self, contract_id: str) -> contract.ContractAgent:
        """Fulfill (complete) a contract."""
        response = self.request.api("POST", f"/my/contracts/{contract_id}/fulfill")
        if "error" in response.keys():
            return parse_error(response)
        return contract.ContractAgent(
            **{
                "agent": agent.Agent(**response["data"]["agent"]),
                "contract": parse_contract(response["data"]["contract"]),
            }
        )

    # Faction Endpoints #
    def list_factions(
        self, limit: int = 10, page: int = 1, all_factions: bool = False
    ) -> List[Faction]:
        """List all_factions discovered factions in the game. (Paginated)"""
        query = {"limit": limit, "page": page}
        response = self.request.api("GET", f"/factions", query_params=query)
        if "error" in response.keys():
            return parse_error(response)
        elif "data" in response.keys():
            response["data"] = [parse_faction(faction) for faction in response["data"]]
        if all_factions:
            pages = math.ceil(response["meta"]["total"]) / 10
            if pages > 1:
                for next_page in range(2, int(pages)):
                    addt_response = self.request.api(
                        "GET", f"/factions", query_params=query
                    )
                    response["data"].extend(
                        [parse_faction(faction) for faction in addt_response["data"]]
                    )

        return response["data"]

    def get_faction(
        self, faction_symbol: FactionSymbol
    ) -> factions.Faction | dict[str, str | int]:
        """View the details of a faction."""
        if faction_symbol in FactionSymbol:
            response = self.request.api("GET", f"/factions/{faction_symbol}")
            return parse_faction(response["data"])
        else:
            return parse_error({"code": 404, "message": "Faction not found"})
