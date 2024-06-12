"""
:Date: 10 JUN 2024
:version: 0.1.0
:Authors: ChatterChats
"""

from dataclasses import dataclass
from typing import Any

from pySpaceTraders.models import errors, cargo, factions, status, contracts, agents, systems, waypoints
from pySpaceTraders.models.enums import FactionSymbol, TradeSymbol, SystemType, WaypointType

from dacite import from_dict


@dataclass
class PySpaceParser:
    ApiInstance: Any

    def contract(self, contract_dict: dict) -> contracts.Contract:
        """

        :param dict contract_dict: Dictionary of contract data
        :return: Instance of Contract data class
        """
        # Convert str factionSymbol to FactionSymbol enum
        if "data" in contract_dict:
            contract_dict = contract_dict["data"]
        contract_dict["factionSymbol"] = FactionSymbol(contract_dict["factionSymbol"])
        contract_dict["ApiInstance"] = self.ApiInstance
        # Convert each delivery tradeSymbol to TradeSymbol enum
        for delivery in contract_dict["terms"]["deliver"]:
            if "tradeSymbol" in delivery:
                delivery["tradeSymbol"] = TradeSymbol(delivery["tradeSymbol"])

        return from_dict(contracts.Contract, contract_dict)

    def contract_cargo(self, contract_cargo_dict: dict) -> contracts.Deliver:
        contract_cargo_dict = contract_cargo_dict["data"]
        contract_cargo_dict["contract"] = self.contract(contract_cargo_dict["contract"])
        contract_cargo_dict["cargo"] = self.cargo(contract_cargo_dict["cargo"])
        return from_dict(contracts.Deliver, contract_cargo_dict)

    def contract_agent(self, contract_agent_dict: dict) -> contracts.ContractAgent:
        contract_agent_dict = contract_agent_dict["data"]
        pass

    def contract_list(self, contract_meta_dict: dict) -> contracts.ListResponse:
        contract_meta_dict["data"] = [self.contract(contract) for contract in contract_meta_dict["data"]]
        return from_dict(
            contracts.ListResponse,
            {
                "contracts": contract_meta_dict["data"],
                "meta": contract_meta_dict["meta"],
            },
        )

    def faction_list(self, faction_dict: dict) -> factions.ListResponse:
        faction_dict["data"] = [self.faction(faction) for faction in faction_dict["data"]]
        return from_dict(
            factions.ListResponse,
            {"factions": faction_dict["data"], "meta": faction_dict["meta"]},
        )

    def agent_list(self, agent_meta_dict: dict) -> agents.ListResponse:
        agent_meta_dict["data"] = [self.agent(agent_dict) for agent_dict in agent_meta_dict["data"]]
        return from_dict(
            agents.ListResponse,
            {"agents": agent_meta_dict["data"], "meta": agent_meta_dict["meta"]},
        )

    def system_list(self, system_meta_dict: dict) -> systems.ListResponse:
        system_meta_dict["data"] = [self.system(system_dict) for system_dict in system_meta_dict["data"]]
        return from_dict(
            systems.ListResponse,
            {"systems": system_meta_dict["data"], "meta": system_meta_dict["meta"]},
        )

    def system_waypoints_list(self, system_waypoint_meta_dict: dict) -> waypoints.ListResponse:
        for waypoint in system_waypoint_meta_dict["data"]:
            waypoint = self.waypoint(waypoint)
        return from_dict(
            waypoints.ListResponse,
            {"waypoints": system_waypoint_meta_dict["data"], "meta": system_waypoint_meta_dict["meta"]},
        )

    @staticmethod
    def error(error_dict: dict) -> errors.Error:
        error_dict = error_dict["error"]
        code = error_dict["code"]
        error = errors.Codes(code).name
        message = error_dict["message"]
        return from_dict(errors.Error, {"error": error, "message": message})

    @staticmethod
    def cargo(cargo_dict: dict) -> cargo.Cargo:
        # Convert item symbol to TradeSymbol enum
        for item in cargo_dict["inventory"]:
            item["symbol"] = TradeSymbol(item["symbol"])
        # Parse Inventory
        return from_dict(cargo.Cargo, cargo_dict)

    @staticmethod
    def faction(faction_dict: dict) -> factions.Faction:
        if "data" in faction_dict:
            faction_dict = faction_dict["data"]
        faction_dict["symbol"] = FactionSymbol(faction_dict["symbol"])
        return from_dict(factions.Faction, faction_dict)

    @staticmethod
    def status(status_dict: dict) -> status.Status:
        return from_dict(status.Status, status_dict)

    @staticmethod
    def agent(agent_dict: dict) -> agents.Agent:
        if "data" in agent_dict:
            agent_dict = agent_dict["data"]
        return from_dict(agents.Agent, agent_dict)

    @staticmethod
    def system(system_dict: dict) -> systems.System:
        system_dict = system_dict["data"] if "data" in system_dict else system_dict
        system_dict["type"] = SystemType(system_dict["type"])
        for waypoint in system_dict["waypoints"]:
            waypoint["type"] = WaypointType(waypoint["type"])
        for faction in system_dict["factions"]:
            faction = FactionSymbol(faction["symbol"])
        return from_dict(systems.System, system_dict)

    @staticmethod
    def waypoint(waypoint_dict: dict) -> waypoints.Waypoint:
        waypoint_dict = waypoint_dict["data"] if "data" in waypoint_dict else waypoint_dict
        waypoint_dict["type"] = WaypointType(waypoint_dict["type"])
        if "faction" in waypoint_dict:
            waypoint_dict["faction"] = [FactionSymbol(faction) for faction in waypoint_dict["faction"]]
        for trait in waypoint_dict["traits"]:
            trait["symbol"] = waypoints.WaypointTraitSymbol(trait["symbol"])
        for modifier in waypoint_dict["modifiers"]:
            modifier["symbol"] = waypoints.WaypointModifierSymbol(modifier["symbol"])
        return from_dict(waypoints.Waypoint, waypoint_dict)
