from dataclasses import dataclass
from typing import List, Dict

from pySpaceTraders.models.enums import FactionSymbol, FactionTraitSymbol


@dataclass
class Trait:
    symbol: str
    name: str
    description: str

    def __post_init__(self):
        self.symbol = FactionTraitSymbol[self.symbol]


@dataclass
class Faction:
    symbol: str
    name: str
    description: str
    headquarters: str
    traits: List[Trait]
    isRecruiting: bool

    def __post_init__(self):
        self.symbol = FactionSymbol(self.symbol)


@dataclass
class ListResponse:
    factions: List[Faction]
    meta: Dict[str, int]
