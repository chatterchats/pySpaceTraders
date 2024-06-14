from dataclasses import dataclass
from typing import List

from pySpaceTraders.models.enums import TradeSymbol


@dataclass
class Item:
    symbol: TradeSymbol
    name: str
    description: str
    units: int


@dataclass
class Cargo:
    capacity: int
    units: int
    inventory: List[Item]
