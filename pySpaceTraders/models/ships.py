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
    ShipConditionEventSymbol,
)


@dataclass
class ShipRequirements:
    power: Optional[int]
    crew: Optional[int]
    slots: Optional[int]


@dataclass
class ShipFrame:
    symbol: ShipFrameSymbol
    name: Optional[str]
    description: Optional[str]
    condition: Optional[float]
    integrity: Optional[float]
    moduleSlots: Optional[int]
    mountingPoints: Optional[int]
    fuelCapacity: Optional[int]
    requirements: Optional[ShipRequirements]


@dataclass
class ShipReactor:
    symbol: ShipReactorSymbol
    name: Optional[str]
    description: Optional[str]
    condition: Optional[float]
    integrity: Optional[float]
    powerOutput: Optional[int]
    requirements: Optional[ShipRequirements]


@dataclass
class ShipEngine:
    symbol: ShipEngineSymbol
    name: Optional[str]
    description: Optional[str]
    condition: Optional[float]
    integrity: Optional[float]
    speed: Optional[int]
    requirements: Optional[ShipRequirements]


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
    name: Optional[str]
    description: Optional[str]
    strength: Optional[int]
    deposits: Optional[List[DepositSymbol]]
    requirements: Optional[ShipRequirements]


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
class ShipEvent:
    symbol: ShipConditionEventSymbol
    component: str
    name: str
    description: str


@dataclass
class Survey:
    signature: str
    symbol: str
    deposits: List[ShipDeposit]
    expiration: str
    size: str


@dataclass
class ShipSiphonYields:
    symbol: TradeSymbol
    units: int


@dataclass
class ShipSiphon:
    shipSymbol: str
    yields: ShipSiphonYields


@dataclass
class Ship:
    symbol: str
    registration: ShipRegistration
    nav: ShipNav
    crew: Optional[ShipCrew]
    frame: Optional[ShipFrame]
    reactor: Optional[ShipReactor]
    engine: ShipEngine
    modules: Optional[List[ShipModule]]
    mounts: Optional[List[ShipMount]]
    cargo: Optional[Cargo]
    fuel: Optional[ShipFuel]
