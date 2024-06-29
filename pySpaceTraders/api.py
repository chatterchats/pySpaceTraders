import inspect
import json
import math
import os.path
from dataclasses import asdict

from dacite import from_dict

from pySpaceTraders.models.models import *
from pySpaceTraders.constants import __version__, DACITE_CONFIG
from pySpaceTraders.utils.pySpaceLogger import PySpaceLogger
from pySpaceTraders.utils.pySpaceRequest import PySpaceRequest


class SpaceTraderClient:
    """SpaceTraders API Client Handler"""

    def __init__(
        self,
        agent_symbol: str,
        agent_faction: FactionSymbol = FactionSymbol.COSMIC,
        agent_email: str = "",
        log: bool = True,
        debug: bool = False,
        testing: bool = False,
    ):
        # version
        self.__version__ = __version__

        # Logging
        self.log: bool = log
        if self.log:
            self.logger = PySpaceLogger("pySpaceTraders", debug=debug)

        # Agent Data
        self.agent_symbol: str = agent_symbol.upper()
        self.agent_faction: FactionSymbol = agent_faction
        self.agent_email: str = agent_email if agent_email else ""

        # Initialize
        self.request = PySpaceRequest(logger=self.logger if self.log else None, testing=testing)

        # Token and Login
        self.token: str = ""
        self._login()
        self.request.set_token(self.token)

        self.logger.info("Init complete")

    ########################
    # --- HELPER FUNCS --- #
    ########################

    def get_all_pages(self, endpoint: str, pages: int) -> list:
        data = []
        for page in range(2, pages + 1):
            data.extend(
                self.request.api("GET", endpoint, query_params={"limit": 20, "page": page})["data"]
            )

        return data

    @staticmethod
    def rename_yield(response_dict: dict) -> dict:
        """Since yield is a keyword, got to rename it or else Python gets mad."""
        if "yield" in response_dict:
            response_dict["yields"] = response_dict["yield"]
            del response_dict["yield"]
        else:
            for k, v in response_dict.items():
                if isinstance(v, dict) and "yield" in v:
                    response_dict[k]["yields"] = response_dict[k]["yield"]
                    del response_dict[k]["yield"]
        return response_dict

    def attach_self_ref(self, obj_class, response_dict: dict) -> dict:
        obj_class_list = [Agent, Ship, Waypoint, Contract, Construction, Shipyard]
        obj_list_class_list = [ListAgents, ListShips, ListWaypoints, ListContracts, ListSystems]
        obj_nested_class_list = [
            AcceptContract,
            DeliverCargo,
            FulfillContract,
            System,
            SupplyConstruction,
            ScanSystems,
            ScanWaypoints,
        ]
        if obj_class in obj_class_list:
            response_dict.update({"ApiInstance": self})
        elif obj_class in obj_list_class_list:
            response_dict["data"] = [
                item.update({"ApiInstance": self}) for item in response_dict.get("data", {})
            ]
        elif obj_class in obj_nested_class_list:
            if response_dict.get("agent", {}):
                response_dict["agent"].update({"ApiInstance": self})
            if response_dict.get("contract", {}):
                response_dict["contract"].update({"ApiInstance": self})
            if response_dict.get("waypoints", {}):
                response_dict["waypoints"].update({"ApiInstance": self})
            pass
        return response_dict

    def response_to_class(self, obj_class, response_dict: dict):
        # TODO: Fix v
        # response_dict = self.attach_self_ref(obj_class, response_dict)
        response_dict = self.rename_yield(response_dict)

        if "error" in response_dict:
            self.logger.debug("Response error returned")
            error = Codes(response_dict["code"]).name
            message = response_dict["message"]
            return from_dict(ApiError, {"error": error, "message": message}, config=DACITE_CONFIG)

        if obj_class not in [
            ListAgents,
            ListShips,
            ListWaypoints,
            ListContracts,
            ListSystems,
            ListFactions,
        ]:
            self.logger.debug("Object not a List Class")
            response_dict = response_dict.get("data", response_dict)

        return from_dict(obj_class, response_dict, config=DACITE_CONFIG)

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

    #############################
    # --- General Endpoints --- #
    #############################

    def _register(self):
        """Register a new agent"""
        self.logger.debug("Check Agent Symbol and Faction Validity")
        # Check validity of agent symbol
        if 3 < len(self.agent_symbol) > 14:
            raise ValueError(
                f"Agent Symbol `{self.agent_symbol}` has a length of {len(self.agent_symbol)}."
                + "Length must be >= 3 and <=14."
            )

        # Make sure faction is recruiting
        faction = self.get_faction(self.agent_faction)
        if (
            isinstance(faction, Faction)
            and faction.symbol == self.agent_faction
            and not faction.isRecruiting
        ):
            raise ValueError(
                f"`{self.agent_faction.value}` Faction is not recruiting new agents at this time."
            )

        self.logger.debug("Agent Symbol and Faction Valid")
        json_data = {
            "symbol": self.agent_symbol,
            "faction": self.agent_faction.value,
        }

        if self.agent_email:
            json_data["email"] = self.agent_email

        register_response = self.request.api("POST", "/register", payload=json_data)
        if "error" in register_response:
            self.logger.error(
                f"Error with {inspect.stack()[0][0]}. {self.response_to_class(ApiError, register_response)}"
            )
            return self.response_to_class(ApiError, register_response)

        if "data" in register_response.keys():
            self.logger.debug("Register Successful")
            self.token = register_response.get("data", {})["token"]
            data = {}
            if os.path.isfile("tokens.json"):
                with open("tokens.json", "r") as f:
                    self.logger.debug("Reading tokens.json")
                    data = json.load(f)
            with open("tokens.json", "w", encoding="utf-8") as f:
                self.logger.debug("Writing new token to tokens.json")
                data[self.agent_symbol] = {"token": self.token}
                json.dump(data, f, indent=4, ensure_ascii=False)
            return self.response_to_class(RegisterNewAgent, register_response)

    def status(self):
        """Server Status and Announcements."""
        status_response = self.request.api("GET", "/")
        return self.response_to_class(Status, status_response)

    ############################
    # --- Agents Endpoints --- #
    ############################

    def my_agent(self) -> Agent | ApiError:
        """Fetch your agent's details"""
        response = self.request.api("GET", "/my/agent")
        return self.response_to_class(Agent, response)

    def list_agents(
        self, limit: int = 20, page: int = 1, all_agents: bool = False
    ) -> ListAgents | ApiError:
        """List all_factions  (Paginated)"""
        # token optional for get_agent
        query = {"limit": 20 if all_agents else limit, "page": page}
        response = self.request.api("GET", "/agents", query_params=query)

        response.get("meta", {})["pages"] = math.ceil(
            response.get("meta", {}).get("total", 1) / limit
        )
        if "error" in response:
            self.logger.error(
                f"Error with {inspect.stack()[0][0]}. {self.response_to_class(ApiError, response)}"
            )
            return self.response_to_class(ApiError, response)

        if all_agents and response.get("meta", {})["pages"] > 1:
            response["data"].extend(
                self.get_all_pages("/agents", response.get("meta", {})["pages"])
            )
            response.get("meta", {})["page"] = 1
            response.get("meta", {})["limit"] = len(response["data"])

        return self.response_to_class(ListAgents, response)

    def get_agent(self, symbol: str = "CHATS") -> Agent | ApiError:
        """Fetch single agent details."""
        # token optional for get_agent
        response = self.request.api(
            "GET",
            f"/agents",
            path_param=symbol,
        )
        return self.response_to_class(Agent, response)

    ###############################
    # --- Contracts Endpoints --- #
    ###############################

    def list_contracts(
        self, limit: int = 20, page: int = 1, all_contracts: bool = False
    ) -> ListContracts | ApiError:
        """Paginated list all contracts agent has (Paginated)"""
        query = {"limit": 20 if all_contracts else limit, "page": page}
        contract_list_dict = self.request.api("GET", "/my/contracts", query_params=query)
        if "error" in contract_list_dict:
            return self.response_to_class(ApiError, contract_list_dict)

        contract_list_dict.get("meta", {})["pages"] = math.ceil(
            contract_list_dict.get("meta", {}).get("total", 1) / limit
        )

        if all_contracts and contract_list_dict.get("meta", {})["pages"] > 1:
            contract_list_dict["data"].extend(
                self.get_all_pages("/my/contracts", contract_list_dict.get("meta", {})["pages"])
            )
            contract_list_dict.get("meta", {})["page"] = 1
            contract_list_dict.get("meta", {})["limit"] = len(contract_list_dict["data"])
        return self.response_to_class(ListContracts, contract_list_dict)

    def get_contract(self, contract_id: str) -> Contract | ApiError:
        """Fetch single contract details"""
        # token optional for get_agent

        contract_dict = self.request.api("GET", "/my/contracts", path_param=contract_id)
        return self.response_to_class(Contract, contract_dict)

    def negotiate_contract(self, ship_symbol: str) -> Contract | ApiError:
        """Negotiate a new contract."""
        response = self.request.api(
            "POST", "/my/ships/{}/negotiate/contract", path_param=ship_symbol
        )
        response = response.get("data", response).get("contract", response)
        return self.response_to_class(Contract, response)

    def accept_contract(self, contract_id: str) -> AcceptContract | ApiError:
        """Accept a contract."""

        response = self.request.api("POST", "/my/contracts/{}/accept", path_param=[contract_id])

        return self.response_to_class(AcceptContract, response)

    def deliver_contract_cargo(
        self, contract_id: str, ship_symbol: str, trade_symbol: TradeSymbol, units: int
    ) -> DeliverCargo | ApiError:
        """ContractDeliver cargo for a given contract."""
        data = {
            "shipSymbol": ship_symbol,
            "tradeSymbol": trade_symbol,
            "units": units,
        }
        response = self.request.api(
            "POST", "/my/contracts/{}/deliver", path_param=contract_id, payload=data
        )
        return self.response_to_class(DeliverCargo, response)

    def fulfill_contract(self, contract_id: str) -> AcceptContract | ApiError:
        """Fulfill (complete) a contract."""
        response = self.request.api("POST", "/my/contracts/{}/fulfill", path_param=contract_id)
        if "error" in response:
            return self.response_to_class(ApiError, response)

        return self.response_to_class(FulfillContract, response)

    ##############################
    # --- Factions Endpoints --- #
    ##############################

    def list_factions(
        self, limit: int = 20, page: int = 1, all_factions: bool = False
    ) -> ListFactions | ApiError:
        """List factions in the game. (Paginated)"""
        query = {"limit": 20 if all_factions else limit, "page": page}
        response = self.request.api("GET", "/factions", query_params=query)
        if "error" in response:
            return self.response_to_class(ApiError, response)
        response.get("meta", {})["pages"] = math.ceil(
            response.get("meta", {}).get("total", 1) / limit
        )
        if all_factions and response.get("meta", {})["pages"] > 1:
            response["data"].extend(
                self.get_all_pages("/factions", response.get("meta", {})["pages"])
            )
            response.get("meta", {})["page"] = 1
            response.get("meta", {})["limit"] = len(response["data"])

        return self.response_to_class(ListFactions, response)

    def get_faction(self, faction_symbol: FactionSymbol) -> Faction | ApiError:
        """View the details of a faction."""
        response = self.request.api("GET", "/factions", path_param=faction_symbol)
        return self.response_to_class(Faction, response)

    ###########################
    # --- Fleet Endpoints --- #
    ###########################

    def list_ships(self, limit: int = 10, page: int = 1, all_ships: bool = False):
        """List your ships. (Paginated)"""
        query = {"limit": 20 if all_ships else limit, "page": page}
        response = self.request.api("GET", "/my/ships", query_params=query)
        if "error" in response:
            return self.response_to_class(ApiError, response)

        response.get("meta", {})["pages"] = math.ceil(
            response.get("meta", {}).get("total", 1) / limit
        )
        if all_ships and response.get("meta", {})["pages"] > 1:
            response["data"].extend(
                self.get_all_pages("/my/ships", response.get("meta", {})["pages"])
            )
            response.get("meta", {})["page"] = 1
            response.get("meta", {})["limit"] = len(response["data"])

        return self.response_to_class(ListShips, response)

    def purchase_ship(self, ship_type: ShipType, waypoint_symbol: str) -> PurchaseShip | ApiError:
        """Purchase a new ship"""
        payload = {"shipType": ship_type.value, "waypointSymbol": waypoint_symbol}
        response = self.request.api("POST", "/my/ships", payload=payload)
        return self.response_to_class(PurchaseShip, response)

    def get_ship(self, ship_symbol: str) -> Ship | ApiError:
        """Get specifics on specified ship."""
        response = self.request.api("GET", "/my/ships", path_param=ship_symbol)
        return self.response_to_class(Ship, response)

    def get_ship_cargo(self, ship_symbol: str) -> Cargo | ApiError:
        """Get cargo for specified ship."""
        response = self.request.api("GET", "/my/ships/{}/cargo", path_param=ship_symbol)
        return self.response_to_class(Cargo, response)

    def ship_refine(
        self, ship_symbol: str, refined_symbol: RefinedGoodSymbol
    ) -> ShipRefine | ApiError:
        """Refine raw material into refined material"""
        payload = {"produce": refined_symbol.value}
        response = self.request.api(
            "POST", "/my/ships/{}/refine", path_param=ship_symbol, payload=payload
        )
        return self.response_to_class(ShipRefine, response)

    def create_chart(self, ship_symbol: str) -> CreateChart | ApiError:
        """Chart the current waypoint."""
        response = self.request.api("POST", "/my/ships/{}/chart", path_param=ship_symbol)
        return self.response_to_class(CreateChart, response)

    def get_ship_cooldown(self, ship_symbol: str) -> Cooldown | ApiError:
        """Get ship cooldown"""
        response = self.request.api("GET", "/my/ships/{}/cooldown", path_param=ship_symbol)
        return self.response_to_class(Cooldown, response)

    def orbit_ship(self, ship_symbol: str) -> ShipNav | ApiError:
        """Move ship from docked status, to orbit."""
        response = self.request.api("POST", "/my/ships/{}/orbit", path_param=ship_symbol)
        response = response.get("data", response).get("nav", response)
        return self.response_to_class(ShipNav, response)

    def dock_ship(self, ship_symbol: str) -> ShipNav | ApiError:
        """Move ship from orbiting, to docked."""
        response = self.request.api("POST", "/my/ships/{}/dock", path_param=ship_symbol)
        response = response.get("data", response).get("nav", response)
        return self.response_to_class(CreateSurvey, response)

    def create_survey(self, ship_symbol: str) -> CreateSurvey | ApiError:
        """Survey current waypoint."""
        response = self.request.api("POST", "/my/ships/{}/survey", path_param=ship_symbol)
        return self.response_to_class(ExtractResources, response)

    def extract_resources(
        self, ship_symbol: str, survey: Survey | dict | None = None
    ) -> ExtractResources | ApiError:
        """Extract resources from a waypoint. Able to partially target resources if you provide a survey."""
        endpoint = "/my/ships/{}/extract"
        if survey:
            endpoint += "/survey"
            payload = asdict(survey) if isinstance(survey, Survey) else survey
            response = self.request.api("POST", endpoint, path_param=ship_symbol, payload=payload)
        else:
            response = self.request.api("POST", endpoint, path_param=ship_symbol)
        return self.response_to_class(ExtractResources, response)

    def siphon_resources(self, ship_symbol: str) -> ExtractResources | ApiError:
        """Siphon resources from gas based waypoints. Similar to Extract Resources from Asteroids."""
        response = self.request.api("POST", "/my/ships/{}/extract", path_param=ship_symbol)
        return self.response_to_class(SiphonResources, response)

    def jettison_cargo(
        self, ship_symbol: str, trade_symbol: TradeSymbol, units: int
    ) -> Cargo | ApiError:
        """Jettison specified item and amount in cargo to space."""
        payload = {"symbol": trade_symbol.value, "units": units}
        response = self.request.api(
            "POST", "/my/ships/{}/jettison", path_param=ship_symbol, payload=payload
        )
        response = response.get("data", response).get("cargo", response)
        return self.response_to_class(Cargo, response)

    def jump_ship(self, ship_symbol: str, waypoint_symbol: str) -> NavigateShip | ApiError:
        """Use a Jump Drive and anti-matter to jump a ship to another waypoint."""
        payload = {"waypointSymbol": waypoint_symbol}
        response = self.request.api(
            "POST", "/my/ships/{}/jump", path_param=ship_symbol, payload=payload
        )
        return self.response_to_class(NavigateShip, response)

    def navigate_ship(self, ship_symbol: str, waypoint_symbol: str) -> NavigateShip | ApiError:
        """Navigate the ship to another waypoint in the system."""
        payload = {"waypointSymbol": waypoint_symbol}
        response = self.request.api(
            "POST", "/my/ships/{}/navigate", path_param=ship_symbol, payload=payload
        )
        return self.response_to_class(NavigateShip, response)

    def patch_ship_nav(
        self, ship_symbol: str, flight_mode: ShipNavFlightMode
    ) -> ShipNav | ApiError:
        """Update the ship's flight mode."""
        payload = {"flightMode": flight_mode.value}
        response = self.request.api(
            "PATCH", "/my/ships/{}/nav", path_param=ship_symbol, payload=payload
        )
        return self.response_to_class(ShipNav, response)

    def get_ship_nav(self, ship_symbol: str) -> ShipNav | ApiError:
        """Gets the current navigation configuration of the ship."""
        response = self.request.api("GET", "/my/ships/{}/nav", path_param=ship_symbol)
        return self.response_to_class(ShipNav, response)

    def warp_ship(self, ship_symbol: str, waypoint_symbol: str) -> NavigateShip | ApiError:
        """Use Warp Drive to warp from current waypoint to another."""
        payload = {"waypointSymbol": waypoint_symbol}
        response = self.request.api(
            "POST", "/my/ships/{}/warp", path_param=ship_symbol, payload=payload
        )
        return self.response_to_class(NavigateShip, response)

    def sell_cargo(
        self, ship_symbol: str, trade_symbol: TradeSymbol, units: int
    ) -> BuySellCargo | ApiError:
        """Sell ship's cargo to market. Market must have item as an import."""
        payload = {"symbol": trade_symbol.value, "units": units}
        response = self.request.api(
            "POST", "/my/ships/{}/sell", path_param=ship_symbol, payload=payload
        )
        return self.response_to_class(BuySellCargo, response)

    def scan_systems(self, ship_symbol: str) -> ScanSystems | ApiError:
        """Scan systems around/connected to the ship's current system."""
        response = self.request.api("POST", "/my/ships/{}/scan/systems", path_param=ship_symbol)
        return self.response_to_class(ScanSystems, response)

    def scan_waypoints(self, ship_symbol: str) -> ScanWaypoints | ApiError:
        """Scan waypoints in the ship's current system."""
        response = self.request.api("POST", "/my/ships/{}/scan/waypoints", path_param=ship_symbol)
        return self.response_to_class(ScanWaypoints, response)

    def scan_ships(self, ship_symbol: str) -> ScanShips | ApiError:
        """Scan ships at the current waypoint."""
        response = self.request.api("POST", "/my/ships/{}/scan/ships", path_param=ship_symbol)
        return self.response_to_class(ScanShips, response)

    def refuel_ship(
        self, ship_symbol: str, fuel_units: Optional[int], from_cargo: bool = False
    ) -> RefuelShip | ApiError:
        """Refuel your ship by buying fuel from the local market or shipyard."""
        payload = {"fuelUnits": fuel_units, "fromCargo": from_cargo}
        response = self.request.api(
            "POST", "/my/ships/{}/refuel", path_param=ship_symbol, payload=payload
        )
        return self.response_to_class(RefuelShip, response)

    def purchase_cargo(
        self, ship_symbol: str, trade_symbol: TradeSymbol, units: int
    ) -> BuySellCargo | ApiError:
        """Purchase cargo from a marketplace"""
        payload = {"symbol": trade_symbol.value, "units": units}
        response = self.request.api(
            "POST", "/my/ships/{}/purchase", path_param=ship_symbol, payload=payload
        )
        return self.response_to_class(Contract, response)

    def transfer_cargo(
        self, from_ship_symbol: str, trade_symbol: TradeSymbol, units: int, to_ship_symbol: str
    ) -> Cargo | ApiError:
        """Transfer Cargo from one ship to another. Both ships must be owned by the same agent."""
        payload = {"tradeSymbol": trade_symbol.value, "units": units, "shipSymbol": to_ship_symbol}
        response = self.request.api(
            "POST", "/my/ships/{}/transfer", path_param=from_ship_symbol, payload=payload
        )
        response = response.get("data", response).get("cargo", response)
        return self.response_to_class(Cargo, response)

    def get_mounts(self, ship_symbol: str) -> GetMounts | ApiError:
        """Get mounts installed on the specified ship."""
        response = self.request.api("GET", "/my/ships/{}/mounts", path_param=ship_symbol)
        return self.response_to_class(GetMounts, response)

    def install_mount(self, ship_symbol: str, mount_symbol: str) -> InstallRemoveMount | ApiError:
        """Install a mount on the specified ship"""
        payload = {"symbol": mount_symbol}
        response = self.request.api(
            "POST", "/my/ships/{}/mounts/install", path_param=ship_symbol, payload=payload
        )
        return self.response_to_class(InstallRemoveMount, response)

    def remove_mount(self, ship_symbol: str, mount_symbol: str) -> InstallRemoveMount | ApiError:
        """Uninstall a mount on the specified ship"""
        payload = {"symbol": mount_symbol}
        response = self.request.api(
            "POST", "/my/ships/{}/mounts/remove", path_param=ship_symbol, payload=payload
        )
        return self.response_to_class(InstallRemoveMount, response)

    def get_ship_scrap_value(self, ship_symbol: str) -> ModificationTransaction | ApiError:
        """Get the value of the ship if it was scrapped."""
        response = self.request.api("GET", "/my/ships/{}/scrap", path_param=ship_symbol)
        response = response.get("data", response).get("transaction", response)
        return self.response_to_class(ModificationTransaction, response)

    def scrap_ship(self, ship_symbol: str) -> ScrapShip | ApiError:
        """Scrap a ship for credits."""
        response = self.request.api("POST", "/my/ships/{}/scrap", path_param=ship_symbol)
        return self.response_to_class(ScrapShip, response)

    def get_repair_ship_cost(self, ship_symbol: str) -> ModificationTransaction | ApiError:
        """Get the cost to repair ship in its current status."""
        response = self.request.api("GET", "/my/ships/{}/repair", path_param=ship_symbol)
        response = response.get("data", response).get("transaction", response)
        return self.response_to_class(ModificationTransaction, response)

    def repair_ship(self, ship_symbol: str) -> RepairShip | ApiError:
        """Repair Ship"""
        response = self.request.api("POST", "/my/ships/{}/repair", path_param=ship_symbol)
        return self.response_to_class(RepairShip, response)

    #############################
    # --- Systems Endpoints --- #
    #############################

    def list_systems(
        self, limit: int = 20, page: int = 1, all_systems: bool = False, confirm_all: bool = True
    ) -> ListSystems | ApiError:
        """List systems in the game. (Paginated)
        Waypoints returned are less detailed than when fetched individually."""
        query = {"limit": 20 if all_systems else limit, "page": page}
        response = self.request.api("GET", "/systems", query_params=query)

        if "error" in response:
            return self.response_to_class(ApiError, response)

        response.get("meta", {})["pages"] = math.ceil(
            response.get("meta", {}).get("total", 1) / limit
        )
        if all_systems and confirm_all and response.get("meta", {})["pages"] > 1:
            response["data"].extend(
                self.get_all_pages("/systems", response.get("meta", {})["pages"])
            )
            response.get("meta", {})["page"] = 1
            response.get("meta", {})["limit"] = len(response["data"])
        return self.response_to_class(ListSystems, response)

    def get_system(self, system_symbol: str) -> System | ApiError:
        """Get the details of a system.
        Waypoints returned are less detailed than when fetched individually."""
        response = self.request.api("GET", "/systems", path_param=system_symbol.upper())
        return self.response_to_class(System, response)

    def list_system_waypoints(
        self,
        system_symbol: str,
        limit: int = 10,
        page: int = 1,
        traits: WaypointTraitSymbol | List[WaypointTraitSymbol] | None = None,
        waypoint_type: WaypointType | None = None,
        all_waypoints: bool = False,
    ) -> ListWaypoints | ApiError:
        """List waypoints for specified system. Able to specify waypoint traits and/or waypoint type (Paginated)"""
        limit = 20 if all_waypoints else limit
        query = {
            "limit": limit,
            "page": page,
        }

        if traits:
            if isinstance(traits, WaypointTraitSymbol):
                self.logger.debug(f"Single FactionTrait: {traits.value}")
                query.update({"traits": traits.value})  # type: ignore
            elif isinstance(traits, list):
                self.logger.debug("Traits contains multiple traits")
                trait_list = []
                for trait in traits:
                    self.logger.debug(f"FactionTrait: {trait}")
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
            return self.response_to_class(ApiError, response)
        response.get("meta", {})["pages"] = math.ceil(
            response.get("meta", {}).get("total", 1) / limit
        )
        if all_waypoints and response.get("meta", {})["pages"] > 1:
            response["data"].extend(
                self.get_all_pages(
                    "/systems/{}/waypoints".format(system_symbol.upper()),
                    response.get("meta", {})["pages"],
                )
            )
            response.get("meta", {})["page"] = 1
            response.get("meta", {})["limit"] = len(response["data"])
        return self.response_to_class(ListWaypoints, response)

    def get_waypoint(self, waypoint_symbol: str) -> Waypoint | ApiError:
        """Get a single waypoint details. More detailed that what is returned when fetching a system."""
        system_symbol = "-".join(waypoint_symbol.split("-")[:-1])
        response = self.request.api(
            "GET",
            "/systems/{}/waypoints/{}",
            path_param=[system_symbol.upper(), waypoint_symbol.upper()],
        )
        return self.response_to_class(Waypoint, response)

    def get_market(self, waypoint_symbol: str) -> Market | ApiError:
        """Get waypoint's market details"""
        system_symbol = "-".join(waypoint_symbol.split("-")[:-1])
        response = self.request.api(
            "GET",
            "/systems/{}/waypoints/{}/market",
            path_param=[system_symbol.upper(), waypoint_symbol.upper()],
        )
        return self.response_to_class(Market, response)

    def get_shipyard(self, waypoint_symbol: str) -> Shipyard | ApiError:
        """Get waypoint's shipyard details"""
        system_symbol = "-".join(waypoint_symbol.split("-")[:-1])
        response = self.request.api(
            "GET",
            "/systems/{}/waypoints/{}/shipyard",
            path_param=[system_symbol.upper(), waypoint_symbol.upper()],
        )
        return self.response_to_class(Shipyard, response)

    def get_jumpgate(self, waypoint_symbol: str) -> JumpGate | ApiError:
        """Get waypoint's jumpgate details"""
        system_symbol = "-".join(waypoint_symbol.split("-")[:-1])
        response = self.request.api(
            "GET",
            "/systems/{}/waypoints/{}/jump-gate",
            path_param=[system_symbol.upper(), waypoint_symbol.upper()],
        )
        response = response.get("data", response).get("transaction", response)
        if "connections" in response and not response["connections"]:
            response["connections"] = [""]
        return self.response_to_class(JumpGate, response)

    def get_construction(self, waypoint_symbol: str) -> Construction | ApiError:
        """Get waypoint's construction details"""
        system_symbol = "-".join(waypoint_symbol.split("-")[:-1])
        response = self.request.api(
            "GET",
            "/systems/{}/waypoints/{}/construction",
            path_param=[system_symbol.upper(), waypoint_symbol.upper()],
        )
        return self.response_to_class(Construction, response)

    def supply_construction(
        self, waypoint_symbol: str, ship_symbol: str, trade_symbol: TradeSymbol, units: int
    ) -> SupplyConstruction | ApiError:
        """Supply waypoint's construction site."""
        system_symbol = "-".join(waypoint_symbol.split("-")[:-1])
        payload = {
            "shipSymbol": ship_symbol,
            "tradeSymbol": trade_symbol,
            "units": units,
        }
        response = self.request.api(
            "POST",
            "/systems/{}/waypoints/{}/construction/supply",
            path_param=[system_symbol.upper(), waypoint_symbol.upper()],
            payload=payload,
        )
        return self.response_to_class(SupplyConstruction, response)
