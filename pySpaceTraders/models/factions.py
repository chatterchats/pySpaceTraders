from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Trait:
    symbol: str
    name: str
    description: str


@dataclass
class Faction:
    symbol: str
    name: str
    description: str
    headquarters: str
    traits: List[Trait]
    isRecruiting: bool


@dataclass
class Response:
    data: List[Faction]


@dataclass
class ListResponse:
    data: List[Faction]
    meta: Dict[str, int]
