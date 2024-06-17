from dataclasses import dataclass
from typing import List

from pySpaceTraders.models.enums import FactionSymbol, FactionTraitSymbol


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
