from dataclasses import dataclass
from typing import List, Optional

from pySpaceTraders.models.enums import FactionSymbol, WaypointType, WaypointTraitSymbol, WaypointModifierSymbol
from pySpaceTraders.models.general import ListMeta


@dataclass
class WaypointModifier:
    symbol: str
    name: str
    description: str

    def __post_init__(self):
        self.symbol = WaypointModifierSymbol(self.symbol)


@dataclass
class WaypointTrait:
    symbol: str
    name: str
    description: str

    def __post_init__(self):
        self.symbol = WaypointTraitSymbol(self.symbol)


@dataclass
class Chart:
    waypointSymbol: Optional[str]
    submittedBy: Optional[str]
    submittedOn: Optional[str]


@dataclass
class Orbital:
    symbol: str


@dataclass
class WaypointFactionSymbol:
    symbol: str

    def __post_init__(self):
        self.symbol = FactionSymbol(self.symbol)


@dataclass
class SystemWaypoint:
    symbol: str
    type: str
    x: int
    y: int
    orbitals: List[Orbital]
    orbits: Optional[str]

    def __post_init__(self):
        self.type = WaypointType(self.type)


@dataclass
class Waypoint(SystemWaypoint):
    systemSymbol: str
    isUnderConstruction: bool
    traits: List[WaypointTrait]
    faction: Optional[WaypointFactionSymbol]
    modifiers: Optional[List[WaypointModifier]]
    chart: Optional[Chart]


@dataclass
class ListResponse:
    waypoints: List[Waypoint]
    meta: ListMeta
