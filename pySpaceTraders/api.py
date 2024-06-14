import json
import math
import os.path
from typing import List

from pySpaceTraders.models import (
    agents,
    contracts,
    factions,
    errors,
    systems,
    waypoints,
    markets,
    shipyards,
    jumpgates,
    constructionsites,
)
from pySpaceTraders.models.enums import FactionSymbol, TradeSymbol, WaypointType, WaypointTraitSymbol
from pySpaceTraders.utils.pySpaceLogger import PySpaceLogger
from pySpaceTraders.utils.pySpaceParsers import PySpaceParser
from pySpaceTraders.utils.pySpaceRequest import PySpaceRequest


class SpaceTraderClient:
    """SpaceTraders API SpaceTraderClient Handler"""

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
            "faction": self.agent_faction.value,
        }

        if self.agent_email:
            json_data["email"] = self.agent_email

        register = self.request.api("POST", "/register", payload=json_data)

        if "data" in register.keys():
            self.logger.debug("Register Successful")
            self.token = register["data"]["token"]
            data = {}
            if os.path.isfile("tokens.json"):
                with open("tokens.json", "r") as f:
                    self.logger.debug("Reading tokens.json")
                    data = json.load(f)
            with open("tokens.json", "w", encoding="utf-8") as f:
                self.logger.debug("Writing new token to tokens.json")
                data[self.agent_symbol] = {"token": self.token}
                json.dump(data, f, indent=4, ensure_ascii=False)
        elif "error" in register.keys():
            self.logger.error(f"Error with registering. {self.parser.error(register)}")

    def status(self):
        """Server Status and Announcements."""
        response = self.request.api("GET", "/")
        return self.parser.status(response)

    # Agent Endpoints #
    def my_agent(self) -> agents.Agent | errors.Error:
        """Fetch your agent's details"""
        response = self.request.api("GET", "/my/agent")
        if "error" in response:
            return self.parser.error(response)
        return self.parser.agent(response)

    def list_agents(
        self, limit: int = 20, page: int = 1, all_agents: bool = False
    ) -> agents.ListResponse | errors.Error:
        """List all_factions agents. (Paginated)"""
        # token optional for get_agent
        query = {"limit": 20 if all_agents else limit, "page": page}
        response = self.request.api("GET", "/agents", query_params=query)

        response["meta"]["pages"] = math.ceil(response["meta"]["total"] / limit)
        if "error" in response:
            return self.parser.error(response)

        if all_agents and response["meta"]["pages"] > 1:
            response["data"].extend(self.get_all_pages("/agents", response["meta"]["pages"]))
            response["meta"]["page"] = 1
            response["meta"]["limit"] = len(response["data"])

        return self.parser.agent_list(response)

    def get_agent(self, symbol: str = "CHATS") -> agents.Agent | errors.Error:
        """Fetch single agent details."""
        # token optional for get_agent
        response = self.request.api(
            "GET",
            f"/agents",
            path_param=symbol,
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.agent(response)

    # Contracts Endpoints #
    def list_contracts(
        self, limit: int = 20, page: int = 1, all_contracts: bool = False
    ) -> contracts.ListResponse | errors.Error:
        """Paginated list all contracts agent has (Paginated)"""
        query = {"limit": 20 if all_contracts else limit, "page": page}
        response = self.request.api("GET", "/my/contracts", query_params=query)
        if "error" in response:
            return self.parser.error(response)

        response["meta"]["pages"] = math.ceil(response["meta"]["total"] / limit)

        if all_contracts and response["meta"]["pages"] > 1:
            response["data"].extend(self.get_all_pages("/my/contracts", response["meta"]["pages"]))
            response["meta"]["page"] = 1
            response["meta"]["limit"] = len(response["data"])

        return self.parser.contract_list(response)

    def get_contract(self, contract_id: str) -> contracts.Contract | errors.Error:
        """Fetch single contract details"""
        # token optional for get_agent

        response = self.request.api("GET", "/my/contracts", path_param=contract_id)
        if "error" in response:
            return self.parser.error(response)
        return self.parser.contract(response)

    def accept_contract(self, contract_id: str) -> contracts.ContractAgent | errors.Error:
        """Accept a contract."""

        response = self.request.api("POST", "/my/contracts/{}/accept", path_param=[contract_id])

        if "error" in response:
            return self.parser.error(response)

        return self.parser.contract_agent(response)

    def deliver_contract_cargo(
        self, contract_id: str, ship_symbol: str, trade_symbol: TradeSymbol, units: int
    ) -> contracts.Deliver | errors.Error:
        """Deliver cargo for a given contract."""
        data = {
            "ship_symbol": ship_symbol,
            "trade_symbol": trade_symbol,
            "units": units,
        }
        response = self.request.api("POST", "/my/contracts/{}/deliver", path_param=contract_id, payload=data)
        if "error" in response:
            return self.parser.error(response)

        return self.parser.contract_cargo(response)

    def fulfill_contract(self, contract_id: str) -> contracts.ContractAgent | errors.Error:
        """Fulfill (complete) a contract."""
        response = self.request.api("POST", "/my/contracts/{}/fulfill", path_param=contract_id)
        if "error" in response:
            return self.parser.error(response)

        return self.parser.contract_agent(response)

    # Faction Endpoints #
    def list_factions(
        self, limit: int = 20, page: int = 1, all_factions: bool = False
    ) -> factions.ListResponse | errors.Error:
        """List factions in the game. (Paginated)"""
        query = {"limit": 20 if all_factions else limit, "page": page}
        response = self.request.api("GET", "/factions", query_params=query)
        if "error" in response:
            return self.parser.error(response)
        response["meta"]["pages"] = math.ceil(response["meta"]["total"] / limit)
        if all_factions and response["meta"]["pages"] > 1:
            response["data"].extend(self.get_all_pages("/factions", response["meta"]["pages"]))
            response["meta"]["page"] = 1
            response["meta"]["limit"] = len(response["data"])

        return self.parser.faction_list(response)

    def get_faction(self, faction_symbol: FactionSymbol) -> factions.Faction | errors.Error:
        """View the details of a faction."""
        response = self.request.api("GET", "/factions", path_param=faction_symbol)
        if "error" in response:
            return self.parser.error(response)

        return self.parser.faction(response)

    def list_systems(
        self, limit: int = 20, page: int = 1, all_systems: bool = False, confirm_all: bool = True
    ) -> systems.ListResponse | errors.Error:
        """List systems in the game. (Paginated)"""
        query = {"limit": 20 if all_systems else limit, "page": page}
        response = self.request.api("GET", "/systems", query_params=query)
        if "error" in response:
            return self.parser.error(response)
        response["meta"]["pages"] = math.ceil(response["meta"]["total"] / limit)
        if all_systems and confirm_all and response["meta"]["pages"] > 1:
            response["data"].extend(self.get_all_pages("/systems", response["meta"]["pages"]))
            response["meta"]["page"] = 1
            response["meta"]["limit"] = len(response["data"])
        return self.parser.system_list(response)

    def get_system(self, system_symbol: str) -> systems.System | errors.Error:
        """Get the details of a system."""
        response = self.request.api("GET", "/systems", path_param=system_symbol.upper())
        if "error" in response:
            return self.parser.error(response)
        return self.parser.system(response)

    def list_system_waypoints(
        self,
        system_symbol: str,
        limit: int = 10,
        page: int = 1,
        traits: WaypointTraitSymbol | List[WaypointTraitSymbol] | None = None,
        waypoint_type: WaypointType | None = None,
        all_waypoints: bool = False,
    ) -> waypoints.ListResponse | errors.Error:
        """List waypoints for specified system. (Paginated)"""
        limit = 20 if all_waypoints else limit
        query = {
            "limit": limit,
            "page": page,
        }

        if traits:
            if isinstance(traits, WaypointTraitSymbol):
                self.logger.debug(f"Single Trait: {traits}")
                query.update({"traits": traits})  # type: ignore
            elif isinstance(traits, list):
                self.logger.debug("Traits contains multiple traits")
                trait_list = []
                for trait in traits:
                    self.logger.debug(f"Trait: {trait}")
                    if isinstance(trait, WaypointTraitSymbol):
                        trait_list.append(trait.value)
                query.update({"traits": trait_list})  # type: ignore

        if waypoint_type:
            self.logger.debug(f"Waypoint Type Present: {waypoint_type}")
            query.update({"type": waypoint_type.value})  # type: ignore

        response = self.request.api(
            "GET", "/systems/{}/waypoints", path_param=[system_symbol.upper()], query_params=query
        )
        if "error" in response:
            return self.parser.error(response)
        response["meta"]["pages"] = math.ceil(response["meta"]["total"] / limit)
        if all_waypoints and response["meta"]["pages"] > 1:
            response["data"].extend(
                self.get_all_pages("/systems/{}/waypoints".format(system_symbol.upper()), response["meta"]["pages"])
            )
            response["meta"]["page"] = 1
            response["meta"]["limit"] = len(response["data"])
        return self.parser.system_waypoints_list(response)

    def get_waypoint(self, waypoint_symbol: str) -> waypoints.Waypoint | errors.Error:
        """Get single waypoint details"""
        system_symbol = "-".join(waypoint_symbol.split("-")[:-1])
        response = self.request.api(
            "GET",
            "/systems/{}/waypoints/{}",
            path_param=[system_symbol.upper(), waypoint_symbol.upper()],
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.waypoint(response)

    def get_market(self, waypoint_symbol: str) -> markets.Market | errors.Error:
        """Get waypoint market details"""
        system_symbol = "-".join(waypoint_symbol.split("-")[:-1])
        response = self.request.api(
            "GET",
            "/systems/{}/waypoints/{}/market",
            path_param=[system_symbol.upper(), waypoint_symbol.upper()],
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.market(response)

    def get_shipyard(self, waypoint_symbol: str) -> shipyards.Shipyard | errors.Error:
        """Get waypoint shipyard details"""
        system_symbol = "-".join(waypoint_symbol.split("-")[:-1])
        response = self.request.api(
            "GET",
            "/systems/{}/waypoints/{}/shipyard",
            path_param=[system_symbol.upper(), waypoint_symbol.upper()],
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.shipyard(response)

    def get_jumpgate(self, waypoint_symbol: str) -> jumpgates.JumpGate | errors.Error:
        """Get waypoint jumpgate details"""
        system_symbol = "-".join(waypoint_symbol.split("-")[:-1])
        response = self.request.api(
            "GET",
            "/systems/{}/waypoints/{}/jump-gate",
            path_param=[system_symbol.upper(), waypoint_symbol.upper()],
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.jumpgate(response)

    def get_construction(self, waypoint_symbol: str) -> constructionsites.ConstructionSite | errors.Error:
        """Get waypoint construction details"""
        system_symbol = "-".join(waypoint_symbol.split("-")[:-1])
        response = self.request.api(
            "GET",
            "/systems/{}/waypoints/{}/construction",
            path_param=[system_symbol.upper(), waypoint_symbol.upper()],
        )

        if "error" in response:
            return self.parser.error(response)
        return self.parser.construction_site(response)

    def supply_construction(self, waypoint_symbol: str, ship_symbol: str, trade_symbol: TradeSymbol, units: int):
        """Supply waypoint construction site."""
        system_symbol = "-".join(waypoint_symbol.split("-")[:-1])
        payload = {
            "ship_symbol": ship_symbol,
            "trade_symbol": trade_symbol,
            "units": units,
        }
        response = self.request.api(
            "POST",
            "/systems/{}/waypoints/{}/construction/supply",
            path_param=[system_symbol.upper(), waypoint_symbol.upper()],
            payload=payload,
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.construction_supply(response)

    def list_ships(self, limit: int = 10, page: int = 1, all_ships: bool = False):
        """List your ships. (Paginated)"""
        query = {"limit": 20 if all_ships else limit, "page": page}
        response = self.request.api("GET", "/my/ships", query_params=query)
        if "error" in response:
            return self.parser.error(response)

        response["meta"]["pages"] = math.ceil(response["meta"]["total"] / limit)
        if all_ships and response["meta"]["pages"] > 1:
            response["data"].extend(self.get_all_pages("/my/ships", response["meta"]["pages"]))
            response["meta"]["page"] = 1
            response["meta"]["limit"] = len(response["data"])

        return self.parser.ship_list(response)

    def get_all_pages(self, endpoint: str, pages: int) -> list:
        data = []
        for page in range(2, pages + 1):
            data.extend(self.request.api("GET", endpoint, query_params={"limit": 20, "page": page})["data"])

        return data
