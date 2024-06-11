from dataclasses import dataclass
from typing import List, Optional

from pySpaceTraders.models.enums import (
    ShipFrameSymbol,
    ShipReactorSymbol,
    ShipEngineSymbol,
    ShipModuleSymbol,
    ShipMountSymbol,
    DepositSymbol,
)


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
    deposits: List[List[DepositSymbol]]
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
