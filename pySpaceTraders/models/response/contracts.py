"""
Response Models For
    List Contracts
    Accept Contract
    Deliver Cargo to Contract
    Fulfill Contract

The following return a single object so not handled here:
    Get Contract
"""

from dataclasses import dataclass
from typing import List

from pySpaceTraders.models.contracts import Contract
from pySpaceTraders.models.agents import Agent
from pySpaceTraders.models.cargo import Cargo
from pySpaceTraders.models.response.generic import ListMeta


@dataclass
class ListContracts:
    """Represents a status_dict containing a list of contracts and associated metadata."""

    data: List[Contract]
    meta: ListMeta


@dataclass
class AcceptContract:
    agent: Agent
    contract: Contract


@dataclass
class DeliverCargoToContract:
    contract: Contract
    cargo: Cargo


@dataclass
class FulfillContract:
    agent: Agent
    contract: Contract
