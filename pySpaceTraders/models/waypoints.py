from dataclasses import dataclass
from typing import List

from pySpaceTraders.models.enums import FactionSymbol, WaypointType, WaypointTraitSymbol, WaypointModifierSymbol
from general import ListMeta


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
class Waypoint:
    symbol: str
    type: WaypointType
    systemSymbol: str
    x: int
    y: int
    orbitals: List[str]
    orbits: str
    faction: FactionSymbol
    traits: List[WaypointTrait]
    modifiers: List[WaypointModifier]
    chart: Chart
    isUnderConstruction: bool


@dataclass
class ListResponse:
    waypoints: List[Waypoint]
    meta: ListMeta
