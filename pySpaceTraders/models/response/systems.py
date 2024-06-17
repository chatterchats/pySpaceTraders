"""
Response Models For
    List Systems
    List Waypoints in System
    Supply Construction Site

The following return a single object so not handled here:
    Get System
    Get Waypoint
    Get Market
    Get Shipyard
    Get Jump Gate
    Get Construction Site
"""

from dataclasses import dataclass
from typing import List

from pySpaceTraders.models.cargo import Cargo
from pySpaceTraders.models.constructionsites import ConstructionSite
from pySpaceTraders.models.response.generic import ListMeta
from pySpaceTraders.models.systems import System
from pySpaceTraders.models.waypoints import Waypoint


@dataclass
class ListSystems:
    systems: List[System]
    meta: ListMeta


@dataclass
class ListWaypoints:
    waypoints: List[Waypoint]
    meta: ListMeta


@dataclass
class SupplyConstructionSite:
    constructionSite: ConstructionSite
    cargo: Cargo
