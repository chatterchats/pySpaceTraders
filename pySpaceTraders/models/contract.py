"""Contract Models"""

from dataclasses import dataclass
from typing import List, Dict, Any

from pySpaceTraders.models.agent import Agent
from pySpaceTraders.models.cargo import Cargo
from pySpaceTraders.models.enums import *


@dataclass
class PaymentTerm:
    """Represents the payment terms of a contract."""

    onAccepted: int
    onFulfilled: int


@dataclass
class DeliverTerms:
    """Represents the delivery requirements of a contract."""

    tradeSymbol: TradeSymbol
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
    factionSymbol: FactionSymbol
    type: str
    terms: Terms
    accepted: bool
    fulfilled: bool
    expiration: str
    deadlineToAccept: str
    ApiInstance: Any

    def update_contract(self, contract_in) -> None:
        """

        :param Contract contract_in:
        :return:
        """
        for k, v in contract_in.__dict__.items():
            setattr(self, k, v)

    def accept(self) -> bool:
        """
        Accepts the contract
        :return: True if accepted, False if already accepted or if API returns an error.
        """
        if self.accepted:
            return False
        else:
            response = self.ApiInstance.accept_contract(self.id)
            if response is ContractAgent:
                self.update_contract(response.contract)
                return True
            elif "error" in response:
                return False

    def deliver(self, ship_symbol: str, trade_symbol: TradeSymbol, units: int) -> bool:
        """
        Delivers the trade good for the contract. Will automatically lower amount to the amount required for the delivery if specified
        amount is more than required.
        :param str ship_symbol:
        :param TradeSymbol trade_symbol:
        :param int units:
        :return: True if delivery made, False if invalid trade_symbol,
        :raises: ValueError if invalid trade_symbol.

        """
        for delivery in self.terms.deliver:
            if delivery.tradeSymbol == trade_symbol:
                remaining = delivery.unitsRequired - delivery.unitsFulfilled
                if remaining > 0:
                    if units > remaining:
                        units = remaining
                    self.ApiInstance.deliver_contract(
                        self.id, ship_symbol, trade_symbol, units
                    )
                elif remaining == 0:
                    return False
        raise ValueError(f"Invalid trade_symbol {trade_symbol} for contract {self.id}")

    def fulfill(self):
        if self.fulfilled:
            pass
        else:
            response = self.ApiInstance.fulfill_contract(self.id)
            if response is ContractAgent:
                self.update_contract(response.contract)


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
