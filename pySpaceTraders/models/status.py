from typing import List

from pydantic import BaseModel


class StatusAnnouncement(BaseModel):
    title: str
    body: str


class CreditLeaderboard(BaseModel):
    agentSymbol: str
    credits: int


class ChartLeaderboard(BaseModel):
    agentSymbol: str
    chartCount: int


class StatusLeaderboard(BaseModel):
    mostCredits: List[CreditLeaderboard]
    mostSubmittedCharts: List[ChartLeaderboard]


class StatusLink(BaseModel):
    name: str
    url: str


class StatusReset(BaseModel):
    frequency: str
    next: str


class StatusStats(BaseModel):
    agents: int
    ships: int
    systems: int
    waypoints: int


class Status(BaseModel):
    announcements: List[StatusAnnouncement]
    description: str
    leaderboards: StatusLeaderboard
    links: List[StatusLink]
    resetDate: str
    serverResets: StatusReset
    stats: StatusStats
    status: str
    version: str
