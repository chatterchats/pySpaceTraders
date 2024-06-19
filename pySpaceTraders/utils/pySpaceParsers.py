"""
:Date: 10 JUN 2024
:version: 0.1.0
:Authors: ChatterChats

The parser for any endpoint that is not a List <Thing> endpoint, that has the following format
{
    "data": {
        "x": Any,
        "y": Any,
        "z": Any
    }
}
Should be only parse the dict inside data, instead of parsing with data like so:
{
    "x": Any,
    "y": Any,
    "z": Any
}

Easily done with:
some_dict = some_dict["data"] if "data" in some_dict else some_dict
"""

from typing import TYPE_CHECKING
from dacite import from_dict, Config

from pySpaceTraders.models.models import *

if TYPE_CHECKING:
    from pySpaceTraders import SpaceTraderClient


@dataclass
class PySpaceParser:
    ApiInstance: "SpaceTraderClient"
    config: Optional[Config] | None = None

    def __post_init__(self):
        self.config = Config(
            cast=[
                ActivityLevel,
                ContractType,
                DepositSymbol,
                FactionTraitSymbol,
                FactionSymbol,
                RefinedGoodSymbol,
                ShipConditionEventSymbol,
                ShipEngineSymbol,
                ShipFrameSymbol,
                ShipModuleSymbol,
                ShipMountSymbol,
                ShipNavStatus,
                ShipNavFlightMode,
                ShipReactorSymbol,
                ShipRole,
                ShipType,
                SupplyLevel,
                SystemType,
                TradeSymbol,
                WaypointModifierSymbol,
                WaypointTraitSymbol,
                WaypointType,
            ]
        )

    @staticmethod
    def rename_yield_attr(response_dict: dict) -> dict:
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

    def response_to_class(self, obj_class, response_dict: dict):
        return from_dict(obj_class, self.rename_yield_attr(response_dict), config=self.config)

    #############################
    # --- General Endpoints --- #
    #############################

    def status(self, status_dict: dict) -> Status:
        status_dict = status_dict["data"] if "data" in status_dict else status_dict

        return self.response_to_class(Status, status_dict)

    def register(self, register_dict: dict) -> RegisterNewAgent:
        register_dict = register_dict["data"] if "data" in register_dict else register_dict

        return self.response_to_class(RegisterNewAgent, register_dict)

    ############################
    # --- Agents Endpoints --- #
    ############################

    def get_agents(self, agent_dict: dict) -> Agent:
        agent_dict = agent_dict["data"] if "data" in agent_dict else agent_dict

        return self.response_to_class(Agent, agent_dict)

    def agent_list(self, agent_meta_dict: dict) -> ListAgents:
        return self.response_to_class(ListAgents, agent_meta_dict)

    ###############################
    # --- Contracts Endpoints --- #
    ###############################

    def list_contracts(self, contract_meta_dict: dict) -> ListContracts:
        for contract in contract_meta_dict["data"]:
            contract["ApiInstance"] = self.ApiInstance
        return self.response_to_class(ListContracts, contract_meta_dict)

    def get_contract(self, contract_dict: dict) -> Contract:
        contract_dict = contract_dict["data"] if "data" in contract_dict else contract_dict
        contract_dict["ApiInstance"] = self.ApiInstance

        return self.response_to_class(Contract, contract_dict)

    def accept_contract(self, accept_contract_dict: dict) -> AcceptContract:
        accept_contract_dict = (
            accept_contract_dict["data"] if "data" in accept_contract_dict else accept_contract_dict
        )
        accept_contract_dict.update({"ApiInstance": self.ApiInstance})
        return self.response_to_class(AcceptContract, accept_contract_dict)

    def deliver_cargo(self, deliver_contract_dict: dict) -> DeliverCargo:
        deliver_contract_dict = (
            deliver_contract_dict["data"]
            if "data" in deliver_contract_dict
            else deliver_contract_dict
        )
        return self.response_to_class(DeliverCargo, deliver_contract_dict)

    def fulfill_contract(self, fulfill_contract_dict: dict) -> FulfillContract:
        fulfill_contract_dict = (
            fulfill_contract_dict["data"]
            if "data" in fulfill_contract_dict
            else fulfill_contract_dict
        )
        return self.response_to_class(FulfillContract, fulfill_contract_dict)

    ##############################
    # --- Factions Endpoints --- #
    ##############################

    def list_factions(self, faction_dict: dict) -> ListFactions:
        return self.response_to_class(ListFactions, faction_dict)

    def get_faction(self, faction_dict: dict) -> Faction:
        faction_dict = faction_dict["data"] if "data" in faction_dict else faction_dict

        return self.response_to_class(Faction, faction_dict)

    ###########################
    # --- Fleet Endpoints --- #
    ###########################

    def list_ships(self, ships_meta_dict: dict) -> ListShips:
        return self.response_to_class(ListShips, ships_meta_dict)

    def purchase_ship(self, purchase_ship_dict) -> PurchaseShip:
        purchase_ship_dict = (
            purchase_ship_dict["data"] if "data" in purchase_ship_dict else purchase_ship_dict
        )
        return self.response_to_class(PurchaseShip, purchase_ship_dict)

    def get_ship(self, ship_dict: dict) -> Ship:
        ship_dict = ship_dict["data"] if "data" in ship_dict else ship_dict

        return self.response_to_class(Ship, ship_dict)

    def get_ship_cargo(self, cargo_dict: dict) -> Cargo:
        cargo_dict = cargo_dict["data"] if "data" in cargo_dict else cargo_dict

        return self.response_to_class(Cargo, cargo_dict)

    def orbit_dock_ship(self, navigation_dict: dict) -> ShipNav:
        navigation_dict = (
            navigation_dict["data"]["nav"]
            if "data" in navigation_dict and "nav" in navigation_dict.get("data", {})
            else navigation_dict
        )

        return self.response_to_class(ShipNav, navigation_dict)

    def ship_refine(self, ship_refine_dict: dict) -> ShipRefine:
        ship_refine_dict = (
            ship_refine_dict["data"] if "data" in ship_refine_dict else ship_refine_dict
        )

        return self.response_to_class(ShipRefine, ship_refine_dict)

    def create_chart(self, chart_dict: dict) -> CreateChart:
        chart_dict = chart_dict["data"] if "data" in chart_dict else chart_dict

        return self.response_to_class(CreateChart, chart_dict)

    def get_ship_cooldown(self, cooldown_dict: dict) -> ShipCooldown:
        cooldown_dict = cooldown_dict["data"] if "data" in cooldown_dict else cooldown_dict

        return self.response_to_class(ShipCooldown, cooldown_dict)

    def create_survey(self, survey_dict: dict) -> CreateSurvey:
        survey_dict = survey_dict["data"] if "data" in survey_dict else survey_dict

        return self.response_to_class(CreateSurvey, survey_dict)

    def extract_resources(self, extract_dict: dict) -> ExtractResources:  # survey_extract_resources
        extract_dict = extract_dict["data"] if "data" in extract_dict else extract_dict

        return self.response_to_class(ExtractResources, extract_dict)

    def siphon_resources(self, siphon_dict: dict) -> SiphonResources:
        siphon_dict = siphon_dict["data"] if "data" in siphon_dict else siphon_dict

        return self.response_to_class(SiphonResources, siphon_dict)

    def transfer_jettison_cargo(self, cargo_dict: dict) -> Cargo:
        cargo_dict = (
            cargo_dict["data"]["cargo"]
            if "data" in cargo_dict and "cargo" in cargo_dict.get("data", {})
            else cargo_dict
        )

        return self.response_to_class(Cargo, cargo_dict)

    def navigate_jump_warp_ship(self, navigate_dict: dict) -> NavigateShip:
        navigate_dict = navigate_dict["data"] if "data" in navigate_dict else navigate_dict

        return self.response_to_class(NavigateShip, navigate_dict)

    def get_patch_ship_nav(self, ship_nav_dict: dict) -> ShipNav:
        ship_nav_dict = ship_nav_dict["data"] if "data" in ship_nav_dict else ship_nav_dict

        return self.response_to_class(ShipNav, ship_nav_dict)

    def buy_sell_cargo(self, cargo_dict: dict) -> BuySellCargo:
        cargo_dict = cargo_dict["data"] if "data" in cargo_dict else cargo_dict

        return self.response_to_class(BuySellCargo, cargo_dict)

    def scan_systems(self, systems_dict: dict) -> ScanSystems:
        systems_dict = systems_dict["data"] if "data" in systems_dict else systems_dict
        return self.response_to_class(ScanSystems, systems_dict)

    def scan_waypoints(self, waypoints_dict: dict) -> ScanWaypoints:
        waypoints_dict = waypoints_dict["data"] if "data" in waypoints_dict else waypoints_dict

        return self.response_to_class(ScanWaypoints, waypoints_dict)

    def scan_ships(self, ships_dict: dict) -> ScanShips:
        ships_dict = ships_dict["data"] if "data" in ships_dict else ships_dict

        return self.response_to_class(ScanShips, ships_dict)

    def refuel_ship(self, refuel_dict: dict) -> RefuelShip:
        refuel_dict = refuel_dict["data"] if "data" in refuel_dict else refuel_dict

        return self.response_to_class(RefuelShip, refuel_dict)

    def negotiate_contract(self, contract_dict: dict) -> Contract:
        contract_dict = contract_dict["data"] if "data" in contract_dict else contract_dict

        return self.response_to_class(Contract, contract_dict)

    def get_mounts(self, mounts_dict: dict) -> GetMounts:
        return self.response_to_class(GetMounts, mounts_dict)

    def install_remove_mount(self, mount_dict: dict) -> InstallRemoveMount:
        mount_dict = mount_dict["data"] if "data" in mount_dict else mount_dict

        return self.response_to_class(InstallRemoveMount, mount_dict)

    def get_scrap_ship(self, scrap_ship_dict: dict) -> MountScrapRepairTransaction:
        scrap_ship_dict = scrap_ship_dict["data"] if "data" in scrap_ship_dict else scrap_ship_dict
        scrap_ship_dict = (
            scrap_ship_dict["transaction"] if "transaction" in scrap_ship_dict else scrap_ship_dict
        )

        return self.response_to_class(MountScrapRepairTransaction, scrap_ship_dict)

    def scrap_ship(self, scrap_ship_dict: dict) -> ScrapShip:
        scrap_ship_dict = scrap_ship_dict["data"] if "data" in scrap_ship_dict else scrap_ship_dict

        return self.response_to_class(ScrapShip, scrap_ship_dict)

    def get_repair_ship(self, repair_ship_dict: dict) -> MountScrapRepairTransaction:
        repair_ship_dict = (
            repair_ship_dict["data"] if "data" in repair_ship_dict else repair_ship_dict
        )
        repair_ship_dict = (
            repair_ship_dict["transaction"]
            if "transaction" in repair_ship_dict
            else repair_ship_dict
        )
        return self.response_to_class(MountScrapRepairTransaction, repair_ship_dict)

    def repair_ship(self, repair_ship_dict: dict) -> RepairShip:
        repair_ship_dict = (
            repair_ship_dict["data"] if "data" in repair_ship_dict else repair_ship_dict
        )

        return self.response_to_class(RepairShip, repair_ship_dict)

    #############################
    # --- Systems Endpoints --- #
    #############################

    def list_systems(self, system_meta_dict: dict) -> ListSystems:
        return self.response_to_class(ListSystems, system_meta_dict)

    def get_system(self, system_dict: dict) -> System:
        system_dict = system_dict["data"] if "data" in system_dict else system_dict

        return self.response_to_class(System, system_dict)

    def list_waypoints_in_system(self, list_waypoints_dict: dict) -> ListWaypoints:
        return self.response_to_class(ListWaypoints, list_waypoints_dict)

    def get_waypoint(self, waypoint_dict: dict) -> Waypoint:
        waypoint_dict = waypoint_dict["data"] if "data" in waypoint_dict else waypoint_dict

        return self.response_to_class(Waypoint, waypoint_dict)

    def get_market(self, market_dict: dict) -> Market:
        market_dict = market_dict["data"] if "data" in market_dict else market_dict

        return self.response_to_class(Market, market_dict)

    def get_shipyard(self, shipyard_dict: dict) -> Shipyard:
        shipyard_dict = shipyard_dict["data"] if "data" in shipyard_dict else shipyard_dict

        return self.response_to_class(Shipyard, shipyard_dict)

    def get_jump_gate(self, jumpgate_dict: dict) -> JumpGate:
        jumpgate_dict = jumpgate_dict["data"] if "data" in jumpgate_dict else jumpgate_dict
        if "connections" in jumpgate_dict and not jumpgate_dict["connections"]:
            jumpgate_dict["connections"] = [""]

        return self.response_to_class(JumpGate, jumpgate_dict)

    def get_construction_site(self, cons_site_dict: dict) -> ConstructionSite:
        cons_site_dict = cons_site_dict["data"] if "data" in cons_site_dict else cons_site_dict

        return self.response_to_class(ConstructionSite, cons_site_dict)

    def supply_construction_site(self, cons_cargo_dict: dict) -> SupplyConstructionSite:
        cons_cargo_dict = cons_cargo_dict["data"] if "data" in cons_cargo_dict else cons_cargo_dict

        return self.response_to_class(SupplyConstructionSite, cons_cargo_dict)

    #########################
    # --- Misc. Parsers --- #
    #########################

    def error(self, error_dict: dict) -> ApiError:
        error_dict = error_dict["error"]
        error = Codes(error_dict["code"]).name
        message = error_dict["message"]
        return self.response_to_class(ApiError, {"error": error, "message": message})
