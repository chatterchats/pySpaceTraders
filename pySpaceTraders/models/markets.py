from dataclasses import dataclass
from typing import List, Optional

from pySpaceTraders.models.enums import TradeSymbol, ActivityLevel, SupplyLevel


# Playing Fun OP


@dataclass
class MarketExport:
    symbol: TradeSymbol
    name: str
    description: str


@dataclass
class MarketImport:
    symbol: TradeSymbol
    name: str
    description: str


@dataclass
class MarketExchange:
    symbol: TradeSymbol
    name: str
    description: str


@dataclass
class MarketTransaction:
    waypointSymbol: str
    shipSymbol: str
    tradeSymbol: TradeSymbol
    type: str
    units: int
    pricePerUnit: int
    totalPrice: int
    timestamp: str


@dataclass
class MarketTradeGood:
    symbol: TradeSymbol
    type: str
    tradeVolume: int
    supply: SupplyLevel
    activity: Optional[ActivityLevel]
    purchasePrice: int
    sellPrice: int


@dataclass
class Market:
    symbol: str
    exports: List[MarketExport]
    imports: List[MarketImport]
    exchange: List[MarketExchange]
    transactions: Optional[List[MarketTransaction]]
    tradeGoods: Optional[List[MarketTradeGood]]
