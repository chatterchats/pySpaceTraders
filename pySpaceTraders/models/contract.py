from typing import List, Dict

from pydantic import BaseModel

from pySpaceTraders.models.agent import Agent
from pySpaceTraders.models.cargo import Cargo


class Payment(BaseModel):
    onAccepted: int
    onFulfilled: int


class DeliverTerms(BaseModel):
    tradeSymbol: str
    destinationSymbol: str
    unitsRequired: int
    unitsFulfilled: int


class Terms(BaseModel):
    deadline: str
    payment: Payment
    deliver: List[DeliverTerms]


class Contract(BaseModel):
    id: str
    factionSymbol: str
    type: str
    terms: Terms
    accepted: bool
    fulfilled: bool
    expiration: str
    deadlineToAccept: str


class Response(BaseModel):
    data: Contract


class ListResponse(BaseModel):
    data: List[Contract]
    meta: Dict[str, int]


class DeliverCargo(BaseModel):
    contract: Contract
    cargo: Cargo


class ContractAgentResponse(BaseModel):
    agent: Agent
    contract: Contract


class DeliverCargoResponse(BaseModel):
    data: DeliverCargo
