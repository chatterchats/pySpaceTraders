from typing import List

from pydantic import BaseModel


class Item(BaseModel):
    symbol: str
    name: str
    description: str
    units: int


class Cargo(BaseModel):
    capacity: int
    units: int
    inventory: List[Item]
