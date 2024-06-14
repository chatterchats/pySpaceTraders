from dataclasses import dataclass
from typing import List, Optional

from pySpaceTraders.models.cargo import Cargo
from pySpaceTraders.models.enums import (
    FactionSymbol,
    ShipEngineSymbol,
    ShipFrameSymbol,
    ShipModuleSymbol,
    ShipMountSymbol,
    ShipNavStatus,
    ShipNavFlightMode,
    ShipReactorSymbol,
    ShipRole,
    TradeSymbol,
    DepositSymbol,
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
    symbol: ShipFrameSymbol
    name: str
    description: str
    condition: float
    integrity: float
    moduleSlots: int
    mountingPoints: int
    fuelCapacity: int
    requirements: ShipRequirements


@dataclass
class ShipReactor:
    symbol: ShipReactorSymbol
    name: str
    description: str
    condition: Optional[float]
    integrity: float
    powerOutput: int
    requirements: ShipRequirements


@dataclass
class ShipEngine:
    symbol: ShipEngineSymbol
    name: str
    description: str
    condition: Optional[float]
    integrity: float
    speed: int
    requirements: ShipRequirements


@dataclass
class ShipModule:
    symbol: ShipModuleSymbol
    name: str
    description: str
    capacity: Optional[int]
    range: Optional[int]
    requirements: ShipRequirements


@dataclass
class ShipMount:
    symbol: ShipMountSymbol
    name: str
    description: Optional[str]
    strength: Optional[int]
    deposits: Optional[List[DepositSymbol]]
    requirements: ShipRequirements


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
    factionSymbol: FactionSymbol
    role: ShipRole


@dataclass
class ShipNavRouteLocation:
    symbol: str
    type: WaypointType
    systemSymbol: str
    x: int
    y: int


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
    status: ShipNavStatus
    flightMode: ShipNavFlightMode


@dataclass
class ShipCrew:
    current: int
    required: int
    capacity: int
    rotation: str
    morale: int
    wages: int


@dataclass
class ShipCooldown:
    shipSymbol: str
    totalSeconds: int
    remainingSeconds: int
    expiration: str


@dataclass
class ShipRefineIO:
    tradeSymbol: TradeSymbol
    units: int


@dataclass
class ShipExtractionYield:
    symbol: TradeSymbol
    units: int


@dataclass
class ShipExtraction:
    shipSymbol: str
    amount: ShipExtractionYield


@dataclass
class ShipDeposit:
    symbol: DepositSymbol


@dataclass
class Survey:
    signature: str
    symbol: str
    deposits: List[ShipDeposit]
    expiration: str
    size: str


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
class ShipList:
    data: List[Ship]
    meta: ListMeta
