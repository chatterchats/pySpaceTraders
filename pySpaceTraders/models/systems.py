from dataclasses import dataclass
from typing import List

from pySpaceTraders.models.enums import SystemType, FactionSymbol
from pySpaceTraders.models.waypoints import SystemWaypoint


@dataclass
class System:
    symbol: str
    sectorSymbol: str
    type: SystemType
    x: int
    y: int
    waypoints: List[SystemWaypoint]
    factions: List[FactionSymbol]
