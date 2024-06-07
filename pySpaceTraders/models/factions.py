from typing import List, Dict

from pydantic import BaseModel


class Factions:
    VALID = [
        "COSMIC",
        "VOID",
        "GALACTIC",
        "QUANTUM",
        "DOMINION",
        "ASTRO",
        "CORSAIRS",
        "OBSIDIAN",
        "AEGIS",
        "UNITED",
        "SOLITARY",
        "COBALT",
        "OMEGA",
        "ECHO",
        "LORDS",
        "CULT",
        "ANCIENTS",
        "SHADOW",
        "ETHEREAL",
    ]
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
