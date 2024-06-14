"""
:Date: 10 JUN 2024
:version: 0.1.0
:Authors: ChatterChats
"""

from dataclasses import dataclass
from typing import Any

from dacite import from_dict

from pySpaceTraders.models import (
    errors,
    cargo,
    factions,
    status,
    contracts,
    agents,
    systems,
    waypoints,
    markets,
    shipyards,
    jumpgates,
    constructionsites,
    ships,
)
from pySpaceTraders.models.enums import (
    FactionSymbol,
    TradeSymbol,
    SystemType,
    WaypointType,
    SupplyLevel,
    ShipType,
    ActivityLevel,
    ShipFrameSymbol,
    ShipEngineSymbol,
    ShipModuleSymbol,
    ShipMountSymbol,
    ShipReactorSymbol,
    DepositSymbol,
)


@dataclass
class PySpaceParser:
    ApiInstance: Any

    ##############################
    # --- Multi Dict Parsers --- #
    ##############################

    def contract_cargo(self, contract_cargo_dict: dict) -> contracts.Deliver:
        contract_cargo_dict = contract_cargo_dict["data"] if "data" in contract_cargo_dict else contract_cargo_dict
        contract_cargo_dict["contract"] = self.contract(contract_cargo_dict["contract"])
        contract_cargo_dict["cargo"] = self.cargo(contract_cargo_dict["cargo"])
        return from_dict(contracts.Deliver, contract_cargo_dict)

    def contract_agent(self, contract_agent_dict: dict) -> contracts.ContractAgent:
        contract_agent_dict = contract_agent_dict["data"] if "data" in contract_agent_dict else contract_agent_dict

        contract_agent_dict["agent"] = self.agent(contract_agent_dict["agent"])
        contract_agent_dict["contract"] = self.contract(contract_agent_dict["contract"])
        return from_dict(contracts.ContractAgent, contract_agent_dict)

    def construction_supply(self, construction_cargo_dict: dict) -> constructionsites.ConstructionSiteSupplyResponse:
        construction_cargo_dict = (
            construction_cargo_dict["data"] if "data" in construction_cargo_dict else construction_cargo_dict
        )

        return from_dict(constructionsites.ConstructionSiteSupplyResponse, construction_cargo_dict)

    ########################
    # --- List Parsers --- #
    ########################

    def contract_list(self, contract_meta_dict: dict) -> contracts.ListResponse:
        for contract in contract_meta_dict["data"]:
            contract["ApiInstance"] = self.ApiInstance
        return from_dict(
            contracts.ListResponse,
            {
                "contracts": contract_meta_dict["data"],
                "meta": contract_meta_dict["meta"],
            },
        )

    @staticmethod
    def faction_list(faction_dict: dict) -> factions.ListResponse:
        return from_dict(
            factions.ListResponse,
            {"factions": faction_dict["data"], "meta": faction_dict["meta"]},
        )

    @staticmethod
    def agent_list(agent_meta_dict: dict) -> agents.ListResponse:
        return from_dict(
            agents.ListResponse,
            {"agents": agent_meta_dict["data"], "meta": agent_meta_dict["meta"]},
        )

    @staticmethod
    def system_list(system_meta_dict: dict) -> systems.ListResponse:
        return from_dict(
            systems.ListResponse,
            {"systems": system_meta_dict["data"], "meta": system_meta_dict["meta"]},
        )

    @staticmethod
    def system_waypoints_list(system_waypoint_meta_dict: dict) -> waypoints.ListResponse:
        return from_dict(
            waypoints.ListResponse,
            {"waypoints": system_waypoint_meta_dict["data"], "meta": system_waypoint_meta_dict["meta"]},
        )

    @staticmethod
    def ship_list(ship_list_dict: dict) -> ships.ListResponse:

        return from_dict(ships.ListResponse, {"ships": ship_list_dict["data"], "meta": ship_list_dict["meta"]})

    ###############################
    # --- Single Dict Parsers --- #
    ###############################

    @staticmethod
    def error(error_dict: dict) -> errors.Error:
        error_dict = error_dict["error"]
        code = error_dict["code"]
        error = errors.Codes(code).name
        message = error_dict["message"]
        return from_dict(errors.Error, {"error": error, "message": message})

    def contract(self, contract_dict: dict) -> contracts.Contract:
        contract_dict = contract_dict["data"] if "data" in contract_dict else contract_dict
        contract_dict["ApiInstance"] = self.ApiInstance

        return from_dict(contracts.Contract, contract_dict)

    @staticmethod
    def cargo(cargo_dict: dict) -> cargo.Cargo:
        cargo_dict = cargo_dict["data"] if "data" in cargo_dict else cargo_dict

        return from_dict(cargo.Cargo, cargo_dict)

    @staticmethod
    def faction(faction_dict: dict) -> factions.Faction:
        faction_dict = faction_dict["data"] if "data" in faction_dict else faction_dict

        return from_dict(factions.Faction, faction_dict)

    @staticmethod
    def status(status_dict: dict) -> status.Status:
        status_dict = status_dict["data"] if "data" in status_dict else status_dict

        return from_dict(status.Status, status_dict)

    @staticmethod
    def agent(agent_dict: dict) -> agents.Agent:
        agent_dict = agent_dict["data"] if "data" in agent_dict else agent_dict

        return from_dict(agents.Agent, agent_dict)

    @staticmethod
    def system(system_dict: dict) -> systems.System:
        system_dict = system_dict["data"] if "data" in system_dict else system_dict

        return from_dict(systems.System, system_dict)

    @staticmethod
    def waypoint(waypoint_dict: dict) -> waypoints.Waypoint:
        waypoint_dict = waypoint_dict["data"] if "data" in waypoint_dict else waypoint_dict

        return from_dict(waypoints.Waypoint, waypoint_dict)

    @staticmethod
    def market(market_dict: dict) -> markets.Market:
        market_dict = market_dict["data"] if "data" in market_dict else market_dict

        return from_dict(markets.Market, market_dict)

    @staticmethod
    def shipyard(shipyard_dict: dict) -> shipyards.Shipyard:
        shipyard_dict = shipyard_dict["data"] if "data" in shipyard_dict else shipyard_dict

        return from_dict(shipyards.Shipyard, shipyard_dict)

    @staticmethod
    def jumpgate(jumpgate_dict: dict) -> jumpgates.JumpGate:
        jumpgate_dict = jumpgate_dict["data"] if "data" in jumpgate_dict else jumpgate_dict
        if "connections" in jumpgate_dict and not jumpgate_dict["connections"]:
            jumpgate_dict["connections"] = [""]

        return from_dict(jumpgates.JumpGate, jumpgate_dict)

    @staticmethod
    def construction_site(construction_site_dict: dict) -> constructionsites.ConstructionSite:
        construction_site_dict = (
            construction_site_dict["data"] if "data" in construction_site_dict else construction_site_dict
        )

        return from_dict(constructionsites.ConstructionSite, construction_site_dict)
