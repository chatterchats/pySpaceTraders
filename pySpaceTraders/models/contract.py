from typing import List, Dict
from dataclasses import dataclass

from pydantic import BaseModel

from pySpaceTraders.models.agent import Agent
from pySpaceTraders.models.cargo import Cargo


@dataclass
class PaymentTerm:
    """Represents the payment terms of a contract."""
    onAccepted: int
    onFulfilled: int


@dataclass
class DeliverTerms:
    """Represents the delivery requirements of a contract."""
    tradeSymbol: str
    destinationSymbol: str
    unitsRequired: int
    unitsFulfilled: int

@dataclass
class Terms:
    """Represents the specific terms and conditions of a contract."""
    deadline: str
    payment: PaymentTerm
    deliver: List[DeliverTerms]


@dataclass
class Contract:
    """Base Contract Class, represents a single contract."""
    id: str
    factionSymbol: str
    type: str
    terms: Terms
    accepted: bool
    fulfilled: bool
    expiration: str
    deadlineToAccept: str


@dataclass
class Response:
    """Represents the response containing contract data."""
    data: Contract


@dataclass
class Deliver:
    """Represents the response given when cargo is delivered as part of a contract."""
    contract: Contract
    cargo: Cargo


@dataclass
class ContractAgent:
    """Represents the response under the "data" key containing an agent and contract data."""
    agent: Agent
    contract: Contract


@dataclass
class ListResponse:
    """Represents a response containing a list of contracts and associated metadata."""
    data: List[Contract]
    meta: Dict[str, int]


# Response Models
@dataclass
class ContractAgentResponse:
    """Represents a response containing contract agent data."""
    data: ContractAgent


@dataclass
class DeliverResponse:
    """Represents a response containing delivery cargo data."""
    data: Deliver
