from typing import Optional, List, Dict

from pydantic import BaseModel


class Agent(BaseModel):
    symbol: str
    headquarters: str
    credits: int
    startingFaction: str
    shipCount: int


class MyAgent(Agent):
    accountId: str


class AgentListResponse(BaseModel):
    data: List[Agent]
    meta: Dict[str, int]
