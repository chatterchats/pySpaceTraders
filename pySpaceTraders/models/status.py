from typing import List

from pydantic import BaseModel


class Announcement(BaseModel):
    title: str
    body: str


class CreditEntry(BaseModel):
    agentSymbol: str
    credits: int


class ChartEntry(BaseModel):
    agentSymbol: str
    chartCount: int


class Leaderboard(BaseModel):
    mostCredits: List[CreditEntry]
    mostSubmittedCharts: List[ChartEntry]


class Link(BaseModel):
    name: str
    url: str


class ServerReset(BaseModel):
    frequency: str
    next: str


class Stats(BaseModel):
    agents: int
    ships: int
    systems: int
    waypoints: int


class Status(BaseModel):
    announcements: List[Announcement]
    description: str
    leaderboards: Leaderboard
    links: List[Link]
    resetDate: str
    serverResets: ServerReset
    stats: Stats
    status: str
    version: str
