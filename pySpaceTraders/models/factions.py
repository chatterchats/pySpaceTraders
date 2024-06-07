from typing import List, Dict
from enum import StrEnum
from pydantic import BaseModel


class Factions(StrEnum):
    COSMIC = "COSMIC"
    VOID = "VOID"
    GALACTIC = "GALACTIC"
    QUANTUM = "QUANTUM"
    DOMINION = "DOMINION"
    ASTRO = "ASTRO"
    CORSAIRS = "CORSAIRS"
    OBSIDIAN = "OBSIDIAN"
    AEGIS = "AEGIS"
    UNITED = "UNITED"
    SOLITARY = "SOLITARY"
    COBALT = "COBALT"
    OMEGA = "OMEGA"
    ECHO = "ECHO"
    LORDS = "LORDS"
    CULT = "CULT"
    ANCIENTS = "ANCIENTS"
    SHADOW = "SHADOW"
    ETHEREAL = "ETHEREAL"


class FactionTrait(BaseModel):
    symbol: str
    name: str
    description: str


class Faction(BaseModel):
    symbol: str
    name: str
    description: str
    headquarters: str
    traits: List[FactionTrait]
    isRecruiting: bool


class FactionResponse(BaseModel):
    data: List[Faction]


class FactionListResponse(BaseModel):
    data: List[Faction]
    meta: Dict[str, int]
