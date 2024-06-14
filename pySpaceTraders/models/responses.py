from dataclasses import dataclass
from typing import List

from pySpaceTraders.models.agents import Agent
from pySpaceTraders.models.cargo import Cargo
from pySpaceTraders.models.constructionsites import ConstructionSite
from pySpaceTraders.models.contracts import Contract
from pySpaceTraders.models.factions import Faction
from pySpaceTraders.models.markets import MarketTransaction
from pySpaceTraders.models.ships import (
    Ship,
    ShipMount,
    ShipFuel,
    ShipCooldown,
    ShipEvent,
    ShipNav,
    ShipExtraction,
    Survey,
)
from pySpaceTraders.models.systems import System
from pySpaceTraders.models.waypoints import Waypoint, Chart


@dataclass
class ListMeta:
    total: int
    page: int
    pages: int
    limit: int


@dataclass
class Error:
    error: str
    message: str


@dataclass
class AgentList:
    data: List[Agent]
    meta: ListMeta


@dataclass
class ContractDeliver:
    """Represents the status_dict given when cargo is delivered as part of a contract."""

    contract: Contract
    cargo: Cargo


@dataclass
class ContractAgent:
    """Represents the status_dict under the "data" key containing an agent and contract data."""

    agent: Agent
    contract: Contract


@dataclass
class ContractList:
    """Represents a status_dict containing a list of contracts and associated metadata."""

    data: List[Contract]
    meta: ListMeta


@dataclass
class FactionList:
    data: List[Faction]
    meta: ListMeta


@dataclass
class ShipList:
    data: List[Ship]
    meta: ListMeta


@dataclass
class PurchaseShip:
    agent: Agent
    ship: Ship
    transaction: MarketTransaction


@dataclass
class CreateSurvey:
    cooldown: ShipCooldown
    surveys: List[Survey]


@dataclass
class ShipExtract:
    cooldown: ShipCooldown
    extraction: ShipExtraction
    cargo: Cargo
    events: List[ShipEvent]


@dataclass
class ShipJump:
    nav: ShipNav
    cooldown: ShipCooldown
    transaction: MarketTransaction
    agent: Agent


@dataclass
class ShipNavigate:
    fuel: ShipFuel
    nav: ShipNav
    events: List[ShipEvent]


@dataclass
class ShipWarp:
    fuel: ShipFuel
    nav: ShipNavigate


@dataclass
class ShipSellCargo:
    agent: Agent
    cargo: Cargo
    transaction: MarketTransaction


@dataclass
class ShipScanSystems:
    cooldown: ShipCooldown
    systems: List[System]


@dataclass
class ShipScanWaypoints:
    cooldown: ShipCooldown
    waypoints: List[Waypoint]


@dataclass
class ShipScanShips:
    cooldown: ShipCooldown
    ships: List[Ship]


@dataclass
class ShipRefuel:
    agent: Agent
    fuel: ShipFuel
    transaction: MarketTransaction


@dataclass
class ShipPurchaseCargo:
    agent: Agent
    cargo: Cargo
    transaction: MarketTransaction


@dataclass
class ShipGetMounts:
    data: List[ShipMount]


@dataclass
class ShipUnInstallMount:
    agent: Agent
    mounts: List[ShipMount]
    cargo: Cargo
    transaction: MarketTransaction


@dataclass
class ShipGetScrapShip:
    transaction: MarketTransaction


@dataclass
class ShipScrapShip:
    agent: Agent
    transaction: MarketTransaction


@dataclass
class ShipGetRepairShip:
    transaction: MarketTransaction


@dataclass
class ShipRepairShip:
    agent: Agent
    ship: Ship
    transaction: MarketTransaction


@dataclass
class SystemList:
    systems: List[System]
    meta: ListMeta


@dataclass
class WaypointList:
    waypoints: List[Waypoint]
    meta: ListMeta


@dataclass
class CreateChart:
    chart: Chart
    waypoint: Waypoint


@dataclass
class ConstructionSiteSupplyResponse:
    constructionSite: ConstructionSite
    cargo: Cargo
