"""
Response Models For
    List Factions

The following return a single object so not handled here:
    Get Faction
"""

from dataclasses import dataclass
from typing import List

from pySpaceTraders.models.factions import Faction
from pySpaceTraders.models.response.generic import ListMeta


@dataclass
class ListFactions:
    data: List[Faction]
    meta: ListMeta
