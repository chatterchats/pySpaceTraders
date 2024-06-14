from dataclasses import dataclass
from typing import List, Dict

from pySpaceTraders.models.enums import FactionSymbol, FactionTraitSymbol
from pySpaceTraders.models.general import ListMeta


@dataclass
class Trait:
    symbol: FactionTraitSymbol
    name: str
    description: str


@dataclass
class Faction:
    symbol: FactionSymbol
    name: str
    description: str
    headquarters: str
    traits: List[Trait]
    isRecruiting: bool


@dataclass
class FactionList:
    data: List[Faction]
    meta: ListMeta
