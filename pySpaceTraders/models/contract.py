from datetime import datetime
from typing import List, Dict

from pydantic import BaseModel

from pySpaceTraders.models.agent import Agent
from pySpaceTraders.models.cargo import Cargo


class ContractPayment(BaseModel):
    onAccepted: int
    onFulfilled: int


class ContractTermsDeliver(BaseModel):
    tradeSymbol: str
    destinationSymbol: str
    unitsRequired: int
    unitsFulfilled: int


class ContractTerms(BaseModel):
    deadline: str
    payment: ContractPayment
    deliver: List[ContractTermsDeliver]


class Contract(BaseModel):
    id: str
    factionSymbol: str
    type: str
    terms: ContractTerms
    accepted: bool
    fulfilled: bool
    expiration: str
    deadlineToAccept: str


class ContractResponse(BaseModel):
    data: Contract


class ContractsListResponse(BaseModel):
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
