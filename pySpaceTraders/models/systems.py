from dataclasses import dataclass
from typing import List

from pySpaceTraders.models.enums import SystemType, FactionSymbol
from general import ListMeta


@dataclass
class System:
    symbol: str
    sectorSymbol: str
    type: SystemType
    x: int
    y: int
    waypoints: List[Waypoint]
    factions: List[FactionSymbol]


@dataclass
class ListResponse:
    systems: List[System]
    meta: ListMeta
