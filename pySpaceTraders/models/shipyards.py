from dataclasses import dataclass
from typing import List, Optional

from pySpaceTraders.models.enums import ShipType, SupplyLevel, ActivityLevel
from pySpaceTraders.models.ships import ShipFrame, ShipReactor, ShipModule, ShipMount


@dataclass
class ShipyardTransaction:
    waypointSymbol: str
    shipSymbol: ShipType  # TODO: Make parser remove this as it is deprecated but still returned
    shipType: ShipType
    price: int
    agentSymbol: str
    timestamp: str


@dataclass
class ShipyardShip:
    type: ShipType
    name: str
    description: str
    supply: SupplyLevel
    activity: ActivityLevel
    purchasePrice: int
    frame: ShipFrame
    reactor: ShipReactor
    modules: List[ShipModule]
    mounts: List[ShipMount]


@dataclass
class ShipyardShipType:
    type: ShipType


@dataclass
class Shipyard:
    symbol: str
    shipTypes: List[ShipyardShipType]
    transactions: Optional[List[ShipyardTransaction]]
    ships: Optional[List[ShipyardShip]]
    modificationsFee: int
