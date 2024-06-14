from dataclasses import dataclass
from typing import List, Optional

from pySpaceTraders.models.enums import FactionSymbol
from pySpaceTraders.models.general import ListMeta


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


@dataclass
class ListResponse:
    agents: List[Agent]
    meta: ListMeta
