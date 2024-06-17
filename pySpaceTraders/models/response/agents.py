"""
Response Models For
    List Agents

The following return a single object so not handled here:
    Get Agent
    Get Public Agent

"""

from dataclasses import dataclass
from typing import List

from pySpaceTraders.models.agents import Agent
from pySpaceTraders.models.response.generic import ListMeta


@dataclass
class ListAgents:
    data: List[Agent]
    meta: ListMeta
