from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Agent:
    symbol: str
    headquarters: str
    credits: int
    startingFaction: str
    shipCount: int


@dataclass
class MyAgent(Agent):
    accountId: str


@dataclass
class ListResponse:
    data: List[Agent]
    meta: Dict[str, int]
