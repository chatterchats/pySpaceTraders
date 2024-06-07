from typing import List, Dict

from pydantic import BaseModel


class Trait(BaseModel):
    symbol: str
    name: str
    description: str


class Faction(BaseModel):
    symbol: str
    name: str
    description: str
    headquarters: str
    traits: List[Trait]
    isRecruiting: bool


class Response(BaseModel):
    data: List[Faction]


class ListResponse(BaseModel):
    data: List[Faction]
    meta: Dict[str, int]

