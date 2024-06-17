"""
Response Models for Status and Register New Agent endpoints
"""

from dataclasses import dataclass
from typing import List

from pySpaceTraders.models.agents import Agent
from pySpaceTraders.models.contracts import Contract
from pySpaceTraders.models.factions import Faction
from pySpaceTraders.models.ships import Ship
from pySpaceTraders.models.status import Announcement, Leaderboard, Link, ServerReset, Stats


@dataclass
class Status:
    announcements: List[Announcement]
    description: str
    leaderboards: Leaderboard
    links: List[Link]
    resetDate: str
    serverResets: ServerReset
    stats: Stats
    status: str
    version: str


@dataclass
class RegisterNewAgent:
    agent: Agent
    contract: Contract
    faction: Faction
    ship: Ship
    token: str
