"""
:Date: 10 JUN 2024
:version: 0.1.0
:Authors: ChatterChats
"""

from dataclasses import dataclass
from typing import Any, Optional

from dacite import from_dict, Config

from pySpaceTraders.models.agents import Agent
from pySpaceTraders.models.cargo import Cargo
from pySpaceTraders.models.constructionsites import ConstructionSite
from pySpaceTraders.models.contracts import Contract
from pySpaceTraders.models.enums import (
    ActivityLevel,
    ContractType,
    DepositSymbol,
    FactionTraitSymbol,
    FactionSymbol,
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
)
from pySpaceTraders.models.errors import Codes
from pySpaceTraders.models.factions import Faction
from pySpaceTraders.models.jumpgates import JumpGate
from pySpaceTraders.models.markets import Market
from pySpaceTraders.models.responses import (
    ContractDeliver,
    ContractAgent,
    ConstructionSiteSupplyResponse,
    ContractList,
    FactionList,
    AgentList,
    SystemList,
    WaypointList,
    ShipList,
    Error,
    PurchaseShip,
    CreateChart,
    CreateSurvey,
    ShipExtract,
)
from pySpaceTraders.models.ships import (
    Ship,
    ShipNav,
    ShipCooldown,
    ShipSiphon,
)
from pySpaceTraders.models.shipyards import Shipyard
from pySpaceTraders.models.status import Status
from pySpaceTraders.models.systems import System
from pySpaceTraders.models.waypoints import Waypoint


@dataclass
class PySpaceParser:
    ApiInstance: Any
    config: Optional[Config] | None = None

    def __post_init__(self):
        self.config = Config(
            cast=[
                ActivityLevel,
                ContractType,
                DepositSymbol,
                FactionTraitSymbol,
                FactionSymbol,
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
        return response_dict

    def response_to_class(self, obj_class, response_dict: dict):
        return from_dict(obj_class, self.rename_yield_attr(response_dict), config=self.config)

    ##############################
    # --- Multi Dict Parsers --- #
    ##############################

    def contract_cargo(self, contract_cargo_dict: dict) -> ContractDeliver:
        contract_cargo_dict = contract_cargo_dict["data"] if "data" in contract_cargo_dict else contract_cargo_dict

        return self.response_to_class(ContractDeliver, contract_cargo_dict)

    def contract_agent(self, contract_agent_dict: dict) -> ContractAgent:
        contract_agent_dict = contract_agent_dict["data"] if "data" in contract_agent_dict else contract_agent_dict

        return self.response_to_class(ContractAgent, contract_agent_dict)

    def construction_supply(self, cons_cargo_dict: dict) -> ConstructionSiteSupplyResponse:
        cons_cargo_dict = cons_cargo_dict["data"] if "data" in cons_cargo_dict else cons_cargo_dict

        return self.response_to_class(ConstructionSiteSupplyResponse, cons_cargo_dict)

    ########################
    # --- List Parsers --- #
    ########################

    def contract_list(self, contract_meta_dict: dict) -> ContractList:
        for contract in contract_meta_dict["data"]:
            contract["ApiInstance"] = self.ApiInstance
        return self.response_to_class(ContractList, contract_meta_dict)

    def faction_list(self, faction_dict: dict) -> FactionList:
        return self.response_to_class(FactionList, faction_dict)

    def agent_list(self, agent_meta_dict: dict) -> AgentList:
        return self.response_to_class(AgentList, agent_meta_dict)

    def system_list(self, system_meta_dict: dict) -> SystemList:
        return self.response_to_class(SystemList, system_meta_dict)

    def system_waypoints_list(self, system_waypoint_meta_dict: dict) -> WaypointList:
        return self.response_to_class(WaypointList, system_waypoint_meta_dict)

    def ship_list(self, ships_meta_dict: dict) -> ShipList:
        return self.response_to_class(ShipList, ships_meta_dict)

    ###############################
    # --- Single Dict Parsers --- #
    ###############################

    def error(self, error_dict: dict) -> Error:
        error_dict = error_dict["error"]
        error = Codes(error_dict["code"]).name
        message = error_dict["message"]
        return self.response_to_class(Error, {"error": error, "message": message})

    def contract(self, contract_dict: dict) -> Contract:
        contract_dict = contract_dict["data"] if "data" in contract_dict else contract_dict
        contract_dict["ApiInstance"] = self.ApiInstance

        return self.response_to_class(Contract, contract_dict)

    def cargo(self, cargo_dict: dict) -> Cargo:
        cargo_dict = cargo_dict["data"] if "data" in cargo_dict else cargo_dict

        return self.response_to_class(Cargo, cargo_dict)

    def faction(self, faction_dict: dict) -> Faction:
        faction_dict = faction_dict["data"] if "data" in faction_dict else faction_dict

        return self.response_to_class(Faction, faction_dict)

    def status(self, status_dict: dict) -> Status:
        status_dict = status_dict["data"] if "data" in status_dict else status_dict

        return self.response_to_class(Status, status_dict)

    def agent(self, agent_dict: dict) -> Agent:
        agent_dict = agent_dict["data"] if "data" in agent_dict else agent_dict

        return self.response_to_class(Agent, agent_dict)

    def system(self, system_dict: dict) -> System:
        system_dict = system_dict["data"] if "data" in system_dict else system_dict

        return self.response_to_class(System, system_dict)

    def waypoint(self, waypoint_dict: dict) -> Waypoint:
        waypoint_dict = waypoint_dict["data"] if "data" in waypoint_dict else waypoint_dict

        return self.response_to_class(Waypoint, waypoint_dict)

    def market(self, market_dict: dict) -> Market:
        market_dict = market_dict["data"] if "data" in market_dict else market_dict

        return self.response_to_class(Market, market_dict)

    def shipyard(self, shipyard_dict: dict) -> Shipyard:
        shipyard_dict = shipyard_dict["data"] if "data" in shipyard_dict else shipyard_dict

        return self.response_to_class(Shipyard, shipyard_dict)

    def jumpgate(self, jumpgate_dict: dict) -> JumpGate:
        jumpgate_dict = jumpgate_dict["data"] if "data" in jumpgate_dict else jumpgate_dict
        if "connections" in jumpgate_dict and not jumpgate_dict["connections"]:
            jumpgate_dict["connections"] = [""]

        return self.response_to_class(JumpGate, jumpgate_dict)

    def construction_site(self, cons_site_dict: dict) -> ConstructionSite:
        cons_site_dict = cons_site_dict["data"] if "data" in cons_site_dict else cons_site_dict

        return self.response_to_class(ConstructionSite, cons_site_dict)

    def ship(self, ship_dict: dict) -> Ship:
        ship_dict = ship_dict["data"] if "data" in ship_dict else ship_dict

        return self.response_to_class(Ship, ship_dict)

    def purchase_ship(self, purchase_ship_dict) -> PurchaseShip:
        purchase_ship_dict = purchase_ship_dict["data"] if "data" in purchase_ship_dict else purchase_ship_dict
        return self.response_to_class(PurchaseShip, purchase_ship_dict)

    def navigation(self, navigation_dict: dict) -> ShipNav:
        navigation_dict = (
            navigation_dict["data"]["nav"]
            if "data" in navigation_dict and "nav" in navigation_dict.get("Nav", {})
            else navigation_dict
        )

        return self.response_to_class(ShipNav, navigation_dict)

    def create_chart(self, chart_dict: dict) -> CreateChart:
        chart_dict = chart_dict["data"] if "data" in chart_dict else chart_dict

        return self.response_to_class(CreateChart, chart_dict)

    def cooldown(self, cooldown_dict: dict) -> ShipCooldown:
        cooldown_dict = cooldown_dict["data"] if "data" in cooldown_dict else cooldown_dict

        return self.response_to_class(ShipCooldown, cooldown_dict)

    def create_survey(self, survey_dict: dict) -> CreateSurvey:
        survey_dict = survey_dict["data"] if "data" in survey_dict else survey_dict
        return self.response_to_class(CreateSurvey, survey_dict)

    def extract_resources(self, extract_dict: dict) -> ShipExtract:  # survey_extract_resources
        extract_dict = extract_dict["data"] if "data" in extract_dict else extract_dict

        return self.response_to_class(ShipExtract, extract_dict)

    def siphon_resources(self, siphon_dict: dict) -> ShipSiphon:
        siphon_dict = siphon_dict["data"] if "data" in siphon_dict else siphon_dict

        return self.response_to_class(ShipSiphon, siphon_dict)
