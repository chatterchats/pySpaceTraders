from dataclasses import dataclass
from typing import List


@dataclass
class Item:
    symbol: str
    name: str
    description: str
    units: int


@dataclass
class Cargo:
    capacity: int
    units: int
    inventory: List[Item]
