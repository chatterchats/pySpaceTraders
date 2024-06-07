from typing import List, Dict

from pydantic import BaseModel


class Agent(BaseModel):
    symbol: str
    headquarters: str
    credits: int
    startingFaction: str
    shipCount: int


class MyAgent(Agent):
    accountId: str


class ListResponse(BaseModel):
    data: List[Agent]
    meta: Dict[str, int]
