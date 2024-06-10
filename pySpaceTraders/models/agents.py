from dataclasses import dataclass
from typing import List, Optional

from pySpaceTraders.models.general import ListMeta


@dataclass
class Agent:
    symbol: str
    headquarters: str
    credits: int
    startingFaction: str
    shipCount: int
    accountId: Optional[str]


@dataclass
class ListResponse:
    agents: List[Agent]
    meta: ListMeta
