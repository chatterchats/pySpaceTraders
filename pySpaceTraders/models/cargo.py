from dataclasses import dataclass
from typing import List

from pySpaceTraders.models.enums import TradeSymbol


@dataclass
class Item:
    symbol: str
    name: str
    description: str
    units: int

    def __post_init__(self):
        self.symbol = TradeSymbol(self.symbol)


@dataclass
class Cargo:
    capacity: int
    units: int
    inventory: List[Item]
