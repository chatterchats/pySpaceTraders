"""Contract Models"""

from dataclasses import dataclass
from typing import List, Any, Optional

from pySpaceTraders.models.agents import Agent
from pySpaceTraders.models.cargo import Cargo
from pySpaceTraders.models.enums import *
from pySpaceTraders.models.errors import Error
from pySpaceTraders.models.general import ListMeta


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

    def __post_init__(self):
        self.tradeSymbol = TradeSymbol(self.tradeSymbol)


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
    deadlineToAccept: Optional[str]
    ApiInstance: Any

    def __post_init__(self):
        self.factionSymbol = FactionSymbol(self.factionSymbol)
        self.type = ContractType(self.type)

    def update_contract(self, contract_in) -> None:
        """

        :param Contract contract_in:
        :return:
        """
        for k, v in contract_in.__dict__.items():
            setattr(self, k, v)
        print("Contract Updated")

    def accept(self) -> bool:
        """
        Accepts the contract
        :return: True if accepted, False if already accepted or if API returns an error.
        """
        if self.accepted:
            return False
        else:
            response = self.ApiInstance.accept_contract(self.id)
            print(response)
            if response is ContractAgent:
                self.update_contract(response.contract)
                return True
            elif response is Error:
                print(Error)
                return False
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
                    self.ApiInstance.deliver_contract(self.id, ship_symbol, trade_symbol, units)
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
class Deliver:
    """Represents the status_dict given when cargo is delivered as part of a contract."""

    contract: Contract
    cargo: Cargo


@dataclass
class ContractAgent:
    """Represents the status_dict under the "data" key containing an agent and contract data."""

    agent: Agent
    contract: Contract


@dataclass
class ListResponse:
    """Represents a status_dict containing a list of contracts and associated metadata."""

    contracts: List[Contract]
    meta: ListMeta
