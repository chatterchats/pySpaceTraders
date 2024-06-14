from dataclasses import dataclass
from typing import Optional

from pySpaceTraders.models.enums import FactionSymbol


@dataclass
class Agent:
    symbol: str
    headquarters: str
    credits: int
    startingFaction: str
    shipCount: int
    accountId: Optional[str]

    def __post_init__(self):
        self.startingFaction = FactionSymbol(self.startingFaction)
