"""
:Date: 10 JUN 2024
:version: 0.1.0
:Authors: ChatterChats
"""

from dataclasses import dataclass
from typing import Any

from pySpaceTraders.models import errors, cargo, factions, status, contracts, agents
from pySpaceTraders.models.enums import FactionSymbol, TradeSymbol

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
