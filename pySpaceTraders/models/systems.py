from dataclasses import dataclass
from typing import List

from pySpaceTraders.models.enums import SystemType, FactionSymbol
from pySpaceTraders.models.general import ListMeta
from pySpaceTraders.models.waypoints import SystemWaypoint


@dataclass
class System:
    symbol: str
    sectorSymbol: str
    type: str
    x: int
    y: int
    waypoints: List[SystemWaypoint]
    factions: List[str]

    def __post_init__(self):
        self.type = SystemType(self.type)
        self.factions = [FactionSymbol(faction) for faction in self.factions]


@dataclass
class ListResponse:
    systems: List[System]
    meta: ListMeta
