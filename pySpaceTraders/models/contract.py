from typing import List, Dict

from pydantic import BaseModel

from pySpaceTraders.models.agent import Agent
from pySpaceTraders.models.cargo import Cargo


class ContractTermsPayment(BaseModel):
    onAccepted: int
    onFulfilled: int


class ContractTermsDeliver(BaseModel):
    tradeSymbol: str
    destinationSymbol: str
    unitsRequired: int
    unitFulfilled: int


class ContractTerms(BaseModel):
    deadline: str
    payment: ContractTermsPayment
    deliver: ContractTermsDeliver


class Contract(BaseModel):
    id: str
    factionSymbol: str
    type: str
    terms: ContractTerms
    accepted: bool
    fulfilled: bool
    expiration: str
    deadlineToAccept: str


class ContractAccept(BaseModel):
    agent: Agent
    contract: Contract


class ContractResponse(BaseModel):
    data: Contract


class ContractsListResponse(BaseModel):
    data: List[Contract]
    meta: Dict[str, int]


class DeliverCargo(BaseModel):
    contract: Contract
    cargo: Cargo


class ContractAcceptResponse(BaseModel):
    data: ContractAccept


class DeliverCargoResponse(BaseModel):
    data: DeliverCargo


class ContractFulfillResponse(BaseModel):
    data: ContractAccept
