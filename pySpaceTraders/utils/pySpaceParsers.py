"""
:Date: 10 JUN 2024
:version: 0.1.0
:Authors: ChatterChats
"""

from pySpaceTraders.models import errors, cargo, factions, status, contract
from pySpaceTraders.models.enums import FactionSymbol, TradeSymbol

from dacite import from_dict


def parse_error(response):
    response = response["error"]
    code = response["code"]
    error = errors.Codes(code).name
    message = response["message"]
    return {"error": error, "message": message}


def parse_contract(contract_in: dict) -> contract.Contract:
    """

    :param dict contract_in: Dictionary of contract data
    :return: Instance of Contract data class
    """
    # Convert str factionSymbol to FactionSymbol enum
    contract_in["factionSymbol"] = FactionSymbol(contract_in["factionSymbol"])

    # Convert each delivery tradeSymbol to TradeSymbol enum
    for delivery in contract_in["terms"]["deliver"]:
        if "tradeSymbol" in delivery:
            delivery["tradeSymbol"] = TradeSymbol(delivery["tradeSymbol"])

    return from_dict(contract.Contract, contract_in)


def parse_cargo(cargo_in: dict) -> cargo.Cargo:
    # Convert item symbol to TradeSymbol enum
    for item in cargo_in["inventory"]:
        item["symbol"] = TradeSymbol(item["symbol"])
    # Parse Inventory
    return from_dict(cargo.Cargo, cargo_in)


def parse_faction(faction: dict) -> factions.Faction:
    faction["symbol"] = FactionSymbol(faction["symbol"])
    return from_dict(factions.Faction, faction)


def parse_status(response: dict) -> status.Status:
    return from_dict(status.Status, response)
