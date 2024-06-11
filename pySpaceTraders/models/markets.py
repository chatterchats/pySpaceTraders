from dataclasses import dataclass
from typing import List

from enums import TradeSymbol, ActivityLevel, SupplyLevel


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
    activity: ActivityLevel
    purchasePrice: int
    sellPrice: int


@dataclass
class MarketMarket:
    symbol: TradeSymbol
    exports: List[MarketExport]
    imports: List[MarketImport]
    exchanges: List[MarketExchange]
    transactions: List[MarketTransaction]
    tradeGoods: List[MarketTradeGood]
