import inspect
import json
import math
import os.path

from pySpaceTraders.models.models import *
from pySpaceTraders.utils.pySpaceLogger import PySpaceLogger
from pySpaceTraders.utils.pySpaceParsers import PySpaceParser
from pySpaceTraders.utils.pySpaceRequest import PySpaceRequest


class DeliverCargoToContract:
    pass


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

        response = self.request.api("POST", "/register", payload=json_data)
        if "error" in response:
            self.logger.error(f"Error with {inspect.stack()[0][0]}. {self.parser.error(response)}")
            return self.parser.error(response)

        if "data" in response.keys():
            self.logger.debug("Register Successful")
            self.token = response["data"]["token"]
            data = {}
            if os.path.isfile("tokens.json"):
                with open("tokens.json", "r") as f:
                    self.logger.debug("Reading tokens.json")
                    data = json.load(f)
            with open("tokens.json", "w", encoding="utf-8") as f:
                self.logger.debug("Writing new token to tokens.json")
                data[self.agent_symbol] = {"token": self.token}
                json.dump(data, f, indent=4, ensure_ascii=False)

    def get_all_pages(self, endpoint: str, pages: int) -> list:
        data = []
        for page in range(2, pages + 1):
            data.extend(
                self.request.api("GET", endpoint, query_params={"limit": 20, "page": page})["data"]
            )

        return data

    #############################
    # --- General Endpoints --- #
    #############################

    def status(self):
        """Server Status and Announcements."""
        response = self.request.api("GET", "/")
        if "error" in response:
            self.logger.error(f"Error with {inspect.stack()[0][0]}. {self.parser.error(response)}")
            return self.parser.error(response)
        return self.parser.status(response)

    ############################
    # --- Agents Endpoints --- #
    ############################

    def my_agent(self) -> Agent | ApiError:
        """Fetch your agent's details"""
        response = self.request.api("GET", "/my/agent")
        if "error" in response:
            self.logger.error(f"Error with {inspect.stack()[0][0]}. {self.parser.error(response)}")
            return self.parser.error(response)
        return self.parser.get_agents(response)

    def list_agents(
        self, limit: int = 20, page: int = 1, all_agents: bool = False
    ) -> ListAgents | ApiError:
        """List all_factions  (Paginated)"""
        # token optional for get_agent
        query = {"limit": 20 if all_agents else limit, "page": page}
        response = self.request.api("GET", "/agents", query_params=query)

        response["meta"]["pages"] = math.ceil(response["meta"]["total"] / limit)
        if "error" in response:
            self.logger.error(f"Error with {inspect.stack()[0][0]}. {self.parser.error(response)}")
            return self.parser.error(response)

        if all_agents and response["meta"]["pages"] > 1:
            response["data"].extend(self.get_all_pages("/agents", response["meta"]["pages"]))
            response["meta"]["page"] = 1
            response["meta"]["limit"] = len(response["data"])

        return self.parser.agent_list(response)

    def get_agent(self, symbol: str = "CHATS") -> Agent | ApiError:
        """Fetch single agent details."""
        # token optional for get_agent
        response = self.request.api(
            "GET",
            f"/agents",
            path_param=symbol,
        )
        if "error" in response:
            self.logger.error(f"Error with {inspect.stack()[0][0]}. {self.parser.error(response)}")
            return self.parser.error(response)
        return self.parser.get_agents(response)

    ###############################
    # --- Contracts Endpoints --- #
    ###############################

    def list_contracts(
        self, limit: int = 20, page: int = 1, all_contracts: bool = False
    ) -> ListContracts | ApiError:
        """Paginated list all contracts agent has (Paginated)"""
        query = {"limit": 20 if all_contracts else limit, "page": page}
        response = self.request.api("GET", "/my/contracts", query_params=query)
        if "error" in response:
            self.logger.error(f"Error with {inspect.stack()[0][0]}. {self.parser.error(response)}")
            return self.parser.error(response)

        response["meta"]["pages"] = math.ceil(response["meta"]["total"] / limit)

        if all_contracts and response["meta"]["pages"] > 1:
            response["data"].extend(self.get_all_pages("/my/contracts", response["meta"]["pages"]))
            response["meta"]["page"] = 1
            response["meta"]["limit"] = len(response["data"])

        return self.parser.list_contracts(response)

    def get_contract(self, contract_id: str) -> Contract | ApiError:
        """Fetch single contract details"""
        # token optional for get_agent

        response = self.request.api("GET", "/my/contracts", path_param=contract_id)
        if "error" in response:
            self.logger.error(f"Error with {inspect.stack()[0][0]}. {self.parser.error(response)}")
            return self.parser.error(response)
        return self.parser.get_contract(response)

    def accept_contract(self, contract_id: str) -> AcceptContract | ApiError:
        """Accept a contract."""

        response = self.request.api("POST", "/my/contracts/{}/accept", path_param=[contract_id])

        if "error" in response:
            self.logger.error(f"Error with {inspect.stack()[0][0]}. {self.parser.error(response)}")
            return self.parser.error(response)

        return self.parser.accept_contract(response)

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
        if "error" in response:
            return self.parser.error(response)

        return self.parser.deliver_cargo(response)

    def fulfill_contract(self, contract_id: str) -> AcceptContract | ApiError:
        """Fulfill (complete) a contract."""
        response = self.request.api("POST", "/my/contracts/{}/fulfill", path_param=contract_id)
        if "error" in response:
            return self.parser.error(response)

        return self.parser.accept_contract(response)

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
            return self.parser.error(response)
        response["meta"]["pages"] = math.ceil(response["meta"]["total"] / limit)
        if all_factions and response["meta"]["pages"] > 1:
            response["data"].extend(self.get_all_pages("/factions", response["meta"]["pages"]))
            response["meta"]["page"] = 1
            response["meta"]["limit"] = len(response["data"])

        return self.parser.list_factions(response)

    def get_faction(self, faction_symbol: FactionSymbol) -> Faction | ApiError:
        """View the details of a faction."""
        response = self.request.api("GET", "/factions", path_param=faction_symbol)
        if "error" in response:
            return self.parser.error(response)

        return self.parser.get_faction(response)

    ###########################
    # --- Fleet Endpoints --- #
    ###########################

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

        return self.parser.list_ships(response)

    def purchase_ship(self, ship_type: ShipType, waypoint_symbol: str) -> PurchaseShip | ApiError:

        payload = {"shipType": ship_type.value, "waypointSymbol": waypoint_symbol}
        response = self.request.api("POST", "/my/ships", payload=payload)
        if "error" in response:
            return self.parser.error(response)
        return self.parser.purchase_ship(response)

    def get_ship(self, ship_symbol: str) -> Ship | ApiError:
        response = self.request.api("GET", "/my/ships", path_param=ship_symbol)
        if "error" in response:
            return self.parser.error(response)
        return self.parser.get_ship(response)

    def get_ship_cargo(self, ship_symbol: str) -> Cargo | ApiError:
        response = self.request.api("GET", "/my/ships/{}/cargo", path_param=ship_symbol)
        if "error" in response:
            return self.parser.error(response)
        return self.parser.get_ship_cargo(response)

    def orbit_ship(self, ship_symbol: str) -> ShipNav | ApiError:
        response = self.request.api("POST", "/my/ships/{}/orbit", path_param=ship_symbol)
        if "error" in response:
            return self.parser.error(response)
        return self.parser.orbit_dock_ship(response)

    def ship_refine(
        self, ship_symbol: str, refined_symbol: RefinedGoodSymbol
    ) -> ShipRefine | ApiError:
        payload = {"produce": refined_symbol.value}
        response = self.request.api(
            "POST", "/my/ships/{}/refine", path_param=ship_symbol, payload=payload
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.ship_refine(response)

    def create_chart(self, ship_symbol: str) -> CreateChart | ApiError:
        response = self.request.api("POST", "/my/ships/{}/chart", path_param=ship_symbol)
        if "error" in response:
            return self.parser.error(response)
        return self.parser.create_chart(response)

    def get_ship_cooldown(self, ship_symbol: str) -> ShipCooldown | ApiError:
        response = self.request.api("GET", "/my/ships/{}/cooldown", path_param=ship_symbol)
        if "error" in response:
            return self.parser.error(response)
        return self.parser.get_ship_cooldown(response)

    def dock_ship(self, ship_symbol: str) -> ShipNav | ApiError:
        response = self.request.api("POST", "/my/ships/{}/dock", path_param=ship_symbol)
        if "error" in response:
            return self.parser.error(response)
        return self.parser.orbit_dock_ship(response)

    def create_survey(self, ship_symbol: str) -> CreateSurvey | ApiError:
        response = self.request.api("POST", "/my/ships/{}/survey", path_param=ship_symbol)
        if "error" in response:
            return self.parser.error(response)
        return self.parser.create_survey(response)

    def extract_resources(
        self, ship_symbol: str, survey: Survey | dict | None = None
    ) -> ExtractResources | ApiError:
        endpoint = "/my/ships/{}/extract"
        if survey:
            endpoint += "/survey"
            payload = survey.get_payload() if isinstance(survey, Survey) else survey
            response = self.request.api("POST", endpoint, path_param=ship_symbol, payload=payload)
        else:
            response = self.request.api("POST", endpoint, path_param=ship_symbol)
        if "error" in response:
            return self.parser.error(response)
        return self.parser.extract_resources(response)

    def siphon_resources(self, ship_symbol: str) -> ExtractResources | ApiError:
        response = self.request.api("POST", "/my/ships/{}/extract", path_param=ship_symbol)
        if "error" in response:
            return self.parser.error(response)
        return self.parser.extract_resources(response)

    def jettison_cargo(
        self, ship_symbol: str, trade_symbol: TradeSymbol, units: int
    ) -> Cargo | ApiError:
        payload = {"symbol": trade_symbol.value, "units": units}
        response = self.request.api(
            "POST", "/my/ships/{}/jettison", path_param=ship_symbol, payload=payload
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.transfer_jettison_cargo(response)

    def jump_ship(self, ship_symbol: str, waypoint_symbol: str) -> NavigateShip | ApiError:
        payload = {"waypointSymbol": waypoint_symbol}
        response = self.request.api(
            "POST", "/my/ships/{}/jump", path_param=ship_symbol, payload=payload
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.navigate_jump_warp_ship(response)

    def navigate_ship(self, ship_symbol: str, waypoint_symbol: str) -> NavigateShip | ApiError:
        payload = {"waypointSymbol": waypoint_symbol}
        response = self.request.api(
            "POST", "/my/ships/{}/navigate", path_param=ship_symbol, payload=payload
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.navigate_jump_warp_ship(response)

    def patch_ship_nav(
        self, ship_symbol: str, flight_mode: ShipNavFlightMode
    ) -> ShipNav | ApiError:
        payload = {"flightMode": flight_mode.value}
        response = self.request.api(
            "PATCH", "/my/ships/{}/nav", path_param=ship_symbol, payload=payload
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.get_patch_ship_nav(response)

    def get_ship_nav(self, ship_symbol: str) -> ShipNav | ApiError:
        response = self.request.api("GET", "/my/ships/{}/nav", path_param=ship_symbol)
        if "error" in response:
            return self.parser.error(response)
        return self.parser.get_patch_ship_nav(response)

    def warp_ship(self, ship_symbol: str, waypoint_symbol: str) -> NavigateShip | ApiError:
        payload = {"waypointSymbol": waypoint_symbol}
        response = self.request.api(
            "POST", "/my/ships/{}/warp", path_param=ship_symbol, payload=payload
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.navigate_jump_warp_ship(response)

    def sell_cargo(
        self, ship_symbol: str, trade_symbol: TradeSymbol, units: int
    ) -> BuySellCargo | ApiError:
        payload = {"symbol": trade_symbol.value, "units": units}
        response = self.request.api(
            "POST", "/my/ships/{}/sell", path_param=ship_symbol, payload=payload
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.buy_sell_cargo(response)

    def scan_systems(self, ship_symbol: str) -> ScanSystems | ApiError:
        response = self.request.api("POST", "/my/ships/{}/scan/systems", path_param=ship_symbol)
        if "error" in response:
            return self.parser.error(response)
        return self.parser.scan_systems(response)

    def scan_waypoints(self, ship_symbol: str) -> ScanWaypoints | ApiError:
        response = self.request.api("POST", "/my/ships/{}/scan/waypoints", path_param=ship_symbol)
        if "error" in response:
            return self.parser.error(response)
        return self.parser.scan_waypoints(response)

    def scan_ships(self, ship_symbol: str) -> ScanShips | ApiError:
        response = self.request.api("POST", "/my/ships/{}/scan/ships", path_param=ship_symbol)
        if "error" in response:
            return self.parser.error(response)
        return self.parser.scan_ships(response)

    def refuel_ship(
        self, ship_symbol: str, fuel_units: Optional[int], from_cargo: bool = False
    ) -> RefuelShip | ApiError:
        """
        Refuel your ship by buying fuel from the local market.
        Requires the ship to be docked in a waypoint that has the Marketplace trait, and the market
        must be selling fuel in order to refuel. Each fuel bought from the market replenishes 100
        units in your ship's fuel. Ships will always be refueled to their frame's maximum fuel
        capacity when using this action.
        """
        payload = {"fuelUnits": fuel_units, "fromCargo": from_cargo}
        response = self.request.api(
            "POST", "/my/ships/{}/refuel", path_param=ship_symbol, payload=payload
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.refuel_ship(response)

    def purchase_cargo(
        self, ship_symbol: str, trade_symbol: TradeSymbol, units: int
    ) -> BuySellCargo | ApiError:
        payload = {"symbol": trade_symbol.value, "units": units}
        response = self.request.api(
            "POST", "/my/ships/{}/purchase", path_param=ship_symbol, payload=payload
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.buy_sell_cargo(response)

    def transfer_cargo(
        self, from_ship_symbol: str, trade_symbol: TradeSymbol, units: int, to_ship_symbol: str
    ) -> Cargo | ApiError:
        payload = {"tradeSymbol": trade_symbol.value, "units": units, "shipSymbol": to_ship_symbol}
        response = self.request.api(
            "POST", "/my/ships/{}/transfer", path_param=from_ship_symbol, payload=payload
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.transfer_jettison_cargo(response)

    def negotiate_contract(self, ship_symbol: str) -> Contract | ApiError:
        response = self.request.api(
            "POST", "/my/ships/{}/negotiate/contract", path_param=ship_symbol
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.negotiate_contract(response)

    def get_mounts(self, ship_symbol: str) -> GetMounts | ApiError:
        response = self.request.api("GET", "/my/ships/{}/mounts", path_param=ship_symbol)
        if "error" in response:
            return self.parser.error(response)
        return self.parser.get_mounts(response)

    def install_mount(self, ship_symbol: str, mount_symbol: str) -> InstallRemoveMount | ApiError:
        payload = {"symbol": mount_symbol}
        response = self.request.api(
            "POST", "/my/ships/{}/mounts/install", path_param=ship_symbol, payload=payload
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.install_remove_mount(response)

    def remove_mount(self, ship_symbol: str, mount_symbol: str) -> InstallRemoveMount | ApiError:
        payload = {"symbol": mount_symbol}
        response = self.request.api(
            "POST", "/my/ships/{}/mounts/remove", path_param=ship_symbol, payload=payload
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.install_remove_mount(response)

    def get_ship_scrap_value(self, ship_symbol: str) -> MountScrapRepairTransaction | ApiError:
        response = self.request.api("GET", "/my/ships/{}/scrap", path_param=ship_symbol)
        if "error" in response:
            return self.parser.error(response)
        return self.parser.get_scrap_ship(response)

    def scrap_ship(self, ship_symbol: str) -> ScrapShip | ApiError:
        response = self.request.api("POST", "/my/ships/{}/scrap", path_param=ship_symbol)
        if "error" in response:
            return self.parser.error(response)
        return self.parser.scrap_ship(response)

    def get_repair_ship_cost(self, ship_symbol: str) -> MountScrapRepairTransaction | ApiError:
        response = self.request.api("GET", "/my/ships/{}/repair", path_param=ship_symbol)
        if "error" in response:
            return self.parser.error(response)
        return self.parser.get_repair_ship(response)

    def repair_ship(self, ship_symbol: str) -> RepairShip | ApiError:
        response = self.request.api("POST", "/my/ships/{}/repair", path_param=ship_symbol)
        if "error" in response:
            return self.parser.error(response)
        return self.parser.repair_ship(response)

    #############################
    # --- Systems Endpoints --- #
    #############################

    def list_systems(
        self, limit: int = 20, page: int = 1, all_systems: bool = False, confirm_all: bool = True
    ) -> ListSystems | ApiError:
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
        return self.parser.list_systems(response)

    def get_system(self, system_symbol: str) -> System | ApiError:
        """Get the details of a system."""
        response = self.request.api("GET", "/systems", path_param=system_symbol.upper())
        if "error" in response:
            return self.parser.error(response)
        return self.parser.get_system(response)

    def list_system_waypoints(
        self,
        system_symbol: str,
        limit: int = 10,
        page: int = 1,
        traits: WaypointTraitSymbol | List[WaypointTraitSymbol] | None = None,
        waypoint_type: WaypointType | None = None,
        all_waypoints: bool = False,
    ) -> ListWaypoints | ApiError:
        """List waypoints for specified system. (Paginated)"""
        limit = 20 if all_waypoints else limit
        query = {
            "limit": limit,
            "page": page,
        }

        if traits:
            if isinstance(traits, WaypointTraitSymbol):
                self.logger.debug(f"Single Trait: {traits.value}")
                query.update({"traits": traits.value})  # type: ignore
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
                self.get_all_pages(
                    "/systems/{}/waypoints".format(system_symbol.upper()), response["meta"]["pages"]
                )
            )
            response["meta"]["page"] = 1
            response["meta"]["limit"] = len(response["data"])
        return self.parser.list_waypoints_in_system(response)

    def get_waypoint(self, waypoint_symbol: str) -> Waypoint | ApiError:
        """Get single waypoint_symbol details"""
        system_symbol = "-".join(waypoint_symbol.split("-")[:-1])
        response = self.request.api(
            "GET",
            "/systems/{}/waypoints/{}",
            path_param=[system_symbol.upper(), waypoint_symbol.upper()],
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.get_waypoint(response)

    def get_market(self, waypoint_symbol: str) -> Market | ApiError:
        """Get waypoint_symbol market details"""
        system_symbol = "-".join(waypoint_symbol.split("-")[:-1])
        response = self.request.api(
            "GET",
            "/systems/{}/waypoints/{}/market",
            path_param=[system_symbol.upper(), waypoint_symbol.upper()],
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.get_market(response)

    def get_shipyard(self, waypoint_symbol: str) -> Shipyard | ApiError:
        """Get waypoint_symbol shipyard details"""
        system_symbol = "-".join(waypoint_symbol.split("-")[:-1])
        response = self.request.api(
            "GET",
            "/systems/{}/waypoints/{}/shipyard",
            path_param=[system_symbol.upper(), waypoint_symbol.upper()],
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.get_shipyard(response)

    def get_jumpgate(self, waypoint_symbol: str) -> JumpGate | ApiError:
        """Get waypoint_symbol jumpgate details"""
        system_symbol = "-".join(waypoint_symbol.split("-")[:-1])
        response = self.request.api(
            "GET",
            "/systems/{}/waypoints/{}/jump-gate",
            path_param=[system_symbol.upper(), waypoint_symbol.upper()],
        )
        if "error" in response:
            return self.parser.error(response)
        return self.parser.get_jump_gate(response)

    def get_construction(self, waypoint_symbol: str) -> ConstructionSite | ApiError:
        """Get waypoint_symbol construction details"""
        system_symbol = "-".join(waypoint_symbol.split("-")[:-1])
        response = self.request.api(
            "GET",
            "/systems/{}/waypoints/{}/construction",
            path_param=[system_symbol.upper(), waypoint_symbol.upper()],
        )

        if "error" in response:
            return self.parser.error(response)
        return self.parser.get_construction_site(response)

    def supply_construction(
        self, waypoint_symbol: str, ship_symbol: str, trade_symbol: TradeSymbol, units: int
    ) -> SupplyConstructionSite | ApiError:
        """Supply waypoint_symbol construction site."""
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
        return self.parser.supply_construction_site(response)
