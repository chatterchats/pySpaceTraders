from dataclasses import dataclass
from typing import List, Optional

from pySpaceTraders.models.enums import SystemType, FactionSymbol
from pySpaceTraders.models.waypoints import SystemWaypoint


@dataclass
class System:
    symbol: str
    sectorSymbol: str
    type: SystemType
    x: int
    y: int
    waypoints: Optional[List[SystemWaypoint]]
    factions: Optional[List[FactionSymbol]]
