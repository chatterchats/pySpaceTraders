from dataclasses import dataclass
from typing import List, Optional

from pySpaceTraders.models.enums import FactionSymbol, WaypointType, WaypointTraitSymbol, WaypointModifierSymbol
from pySpaceTraders.models.general import ListMeta


@dataclass
class WaypointModifier:
    symbol: WaypointModifierSymbol
    name: str
    description: str


@dataclass
class WaypointTrait:
    symbol: WaypointTraitSymbol
    name: str
    description: str


@dataclass
class Chart:
    waypointSymbol: str
    submittedBy: str
    submittedOn: str


@dataclass
class Orbital:
    symbol: str


@dataclass
class SystemWaypoint:
    symbol: str
    type: WaypointType
    x: int
    y: int
    orbitals: List[Orbital]
    orbits: Optional[str]


@dataclass
class Waypoint(SystemWaypoint):
    systemSymbol: str
    faction: Optional[FactionSymbol]
    traits: List[WaypointTrait]
    modifiers: Optional[List[WaypointModifier]]
    chart: Optional[Chart]
    isUnderConstruction: bool


@dataclass
class ListResponse:
    waypoints: List[Waypoint]
    meta: ListMeta
