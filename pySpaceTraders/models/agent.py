from typing import Optional, List, Dict

from pydantic import BaseModel


class Agent(BaseModel):
    accountId: Optional[str]
    symbol: str
    headquarters: str
    credits: int
    startingFaction: str
    shipCount: int


class AgentResponse(BaseModel):
    data: Agent


class AgentListResponse(BaseModel):
    data: List[Agent]
    meta: Dict[str, int]
