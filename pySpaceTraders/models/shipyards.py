from dataclasses import dataclass
from typing import List, Optional

from pySpaceTraders.models.enums import ShipType, SupplyLevel, ActivityLevel
from pySpaceTraders.models.ships import ShipFrame, ShipReactor, ShipModule, ShipMount


@dataclass
class ShipyardTransaction:
    waypointSymbol: str
    shipSymbol: str
    shipType: str
    price: int
    agentSymbol: str
    timestamp: str

    def __post_init__(self):
        self.shipSymbol = ShipType(self.shipType)  # Assigned Same as ShipSymbol is Deprecated, but is same data as shipType
        self.shipType = ShipType(self.shipType)

@dataclass
class ShipyardShip:
    type: str
    name: str
    description: str
    supply: str
    activity: str
    purchasePrice: int
    frame: ShipFrame
    reactor: ShipReactor
    modules: List[ShipModule]
    mounts: List[ShipMount]

    def __post_init__(self):
        self.type = ShipType(self.type)
        self.supply = SupplyLevel(self.supply)
        self.activity = ActivityLevel(self.activity)



@dataclass
class ShipyardShipType:
    type: str

    def __post_init__(self):
        self.type = ShipType(self.type)


@dataclass
class Shipyard:
    symbol: str
    shipTypes: List[ShipyardShipType]
    transactions: Optional[List[ShipyardTransaction]]
    ships: Optional[List[ShipyardShip]]
    modificationsFee: int
