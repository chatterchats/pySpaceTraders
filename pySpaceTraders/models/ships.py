from dataclasses import dataclass
from typing import List, Optional

from pySpaceTraders.models.cargo import Cargo
from pySpaceTraders.models.enums import (
    ShipFrameSymbol,
    ShipReactorSymbol,
    ShipEngineSymbol,
    ShipModuleSymbol,
    ShipMountSymbol,
    DepositSymbol,
    FactionSymbol,
    ShipRole,
    ShipNavStatus,
    ShipNavFlightMode,
    WaypointType,
)
from pySpaceTraders.models.general import ListMeta


@dataclass
class ShipRequirements:
    power: Optional[int]
    crew: Optional[int]
    slots: Optional[int]


@dataclass
class ShipFrame:
    symbol: str
    name: str
    description: str
    condition: float
    integrity: float
    moduleSlots: int
    mountingPoints: int
    fuelCapacity: int
    requirements: ShipRequirements

    def __post_init__(self):
        self.symbol = ShipFrameSymbol(self.symbol)


@dataclass
class ShipReactor:
    symbol: str
    name: str
    description: str
    condition: Optional[float]
    integrity: float
    powerOutput: int
    requirements: ShipRequirements

    def __post_init__(self):
        self.symbol = ShipReactorSymbol(self.symbol)


@dataclass
class ShipEngine:
    symbol: str
    name: str
    description: str
    condition: Optional[float]
    integrity: float
    speed: int
    requirements: ShipRequirements

    def __post_init__(self):
        self.symbol = ShipEngineSymbol(self.symbol)


@dataclass
class ShipModule:
    symbol: str
    name: str
    description: str
    capacity: Optional[int]
    range: Optional[int]
    requirements: ShipRequirements

    def __post_init__(self):
        self.symbol = ShipModuleSymbol(self.symbol)


@dataclass
class ShipMount:
    symbol: str
    name: str
    description: Optional[str]
    strength: Optional[int]
    deposits: Optional[List[str]]
    requirements: ShipRequirements

    def __post_init__(self):
        self.symbol = ShipMountSymbol(self.symbol)
        if self.deposits is not None:
            self.desposits = [DepositSymbol(deposit) for deposit in self.deposits]


@dataclass
class ShipFuelConsumed:
    amount: int
    timestamp: str


@dataclass
class ShipFuel:
    current: int
    capacity: int
    consumed: Optional[ShipFuelConsumed]


@dataclass
class ShipRegistration:
    name: str
    factionSymbol: str
    role: str

    def __post_init__(self):
        self.factionSymbol = FactionSymbol(self.factionSymbol)
        self.role = ShipRole(self.role)


@dataclass
class ShipNavRouteLocation:
    symbol: str
    type: str
    systemSymbol: str
    x: int
    y: int

    def __post_init__(self):
        self.type = WaypointType(self.type)


@dataclass
class ShipNavRoute:
    destination: ShipNavRouteLocation
    origin: ShipNavRouteLocation
    departureTime: str
    arrival: str


@dataclass
class ShipNav:
    systemSymbol: str
    waypointSymbol: str
    route: ShipNavRoute
    status: str
    flightMode: str

    def __post_init__(self):
        self.status = ShipNavStatus(self.status)
        self.flightMode = ShipNavFlightMode(self.flightMode)


@dataclass
class ShipCrew:
    current: int
    required: int
    capacity: int
    rotation: str
    morale: int
    wages: int


@dataclass
class Ship:
    symbol: str
    registration: ShipRegistration
    nav: ShipNav
    crew: ShipCrew
    frame: ShipFrame
    reactor: ShipReactor
    engine: ShipEngine
    modules: List[ShipModule]
    mounts: List[ShipMount]
    cargo: Cargo
    fuel: ShipFuel


@dataclass
class ListResponse:
    ships: List[Ship]
    meta: ListMeta
