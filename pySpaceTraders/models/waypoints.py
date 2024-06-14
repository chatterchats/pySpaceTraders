from dataclasses import dataclass
from typing import List, Optional

from pySpaceTraders.models.enums import FactionSymbol, WaypointType, WaypointTraitSymbol, WaypointModifierSymbol


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
    waypointSymbol: Optional[str]
    submittedBy: Optional[str]
    submittedOn: Optional[str]


@dataclass
class Orbital:
    symbol: str


@dataclass
class WaypointFactionSymbol:
    symbol: FactionSymbol


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
    isUnderConstruction: bool
    traits: List[WaypointTrait]
    faction: Optional[WaypointFactionSymbol]
    modifiers: Optional[List[WaypointModifier]]
    chart: Optional[Chart]
