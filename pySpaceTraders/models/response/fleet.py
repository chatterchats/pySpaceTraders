"""
Response Models For
    List Ships
    Purchase Ship
    Ship Refine
    Create Chart
    Create Survey
    Extract Resources ( and Extract Resources with Survey )
    Siphon Resources
    Jump Ship ( and Navigate Ship and Warp Ship)
    Sell Cargo
    Scan Systems
    Scan Waypoints
    Scan Ships
    Refuel Ship
    Purchase Cargo
    Get Mounts
    Install Mount ( and Remove Mount )
    Scrap Ship
    Repair Ship



The following return a single object so not handled here:
    Get Ship
    Get Ship Cargo
    Orbit Ship
    Get Ship Cooldown
    Dock Ship
    Jettison Cargo
    Patch Ship Nav
    Get Ship Nav
    Transfer Cargo
    Negotiate Contract
    Get Scrap Ship
    Get Repair Ship
"""

from dataclasses import dataclass
from typing import List, Optional

from pySpaceTraders.models.agents import Agent
from pySpaceTraders.models.cargo import Cargo
from pySpaceTraders.models.markets import MarketTransaction
from pySpaceTraders.models.response.generic import ListMeta
from pySpaceTraders.models.ships import (
    Ship,
    ShipMount,
    ShipFuel,
    ShipCooldown,
    ShipEvent,
    ShipNav,
    ShipSiphon,
    ShipExtraction,
    Survey,
    ShipRefineIO,
)
from pySpaceTraders.models.shipyards import MountScrapRepairTransaction, ShipyardTransaction
from pySpaceTraders.models.systems import System
from pySpaceTraders.models.waypoints import Waypoint, Chart


@dataclass
class ListShips:
    data: List[Ship]
    meta: ListMeta


@dataclass
class PurchaseShip:
    agent: Agent
    ship: Ship
    transaction: ShipyardTransaction


@dataclass
class ShipRefine:
    cargo: Cargo
    cooldown: ShipCooldown
    produced: ShipRefineIO
    consumed: ShipRefineIO


@dataclass
class CreateChart:
    chart: Chart
    waypoint: Waypoint


@dataclass
class CreateSurvey:
    cooldown: ShipCooldown
    surveys: List[Survey]


@dataclass
class ExtractResources:
    cooldown: ShipCooldown
    extraction: ShipExtraction
    cargo: Cargo
    events: List[ShipEvent]


@dataclass
class SiphonResources:
    cooldown: ShipCooldown
    siphon: ShipSiphon
    cargo: Cargo
    events: List[ShipEvent]


@dataclass
class NavigateShip:
    fuel: ShipFuel
    cooldown: Optional[ShipCooldown]
    nav: ShipNav
    events: List[ShipEvent]


@dataclass
class BuySellCargo:
    agent: Agent
    cargo: Cargo
    transaction: MarketTransaction


@dataclass
class ScanSystems:
    cooldown: ShipCooldown
    systems: List[System]


@dataclass
class ScanWaypoints:
    cooldown: ShipCooldown
    waypoints: List[Waypoint]


@dataclass
class ScanShips:
    cooldown: ShipCooldown
    ships: List[Ship]


@dataclass
class RefuelShip:
    agent: Agent
    fuel: ShipFuel
    transaction: MarketTransaction


@dataclass
class GetMounts:
    data: List[ShipMount]


@dataclass
class InstallRemoveMount:
    """Returned when Installing or Removing a Mount"""

    agent: Agent
    mounts: List[ShipMount]
    cargo: Cargo
    transaction: MountScrapRepairTransaction


@dataclass
class ScrapShip:
    agent: Agent
    transaction: MountScrapRepairTransaction


@dataclass
class RepairShip:
    agent: Agent
    ship: Ship
    transaction: MountScrapRepairTransaction
