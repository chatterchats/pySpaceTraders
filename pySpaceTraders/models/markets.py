from dataclasses import dataclass
from typing import List, Optional

from pySpaceTraders.models.enums import TradeSymbol, ActivityLevel, SupplyLevel


# Playing Fun OP


@dataclass
class MarketExport:
    symbol: str
    name: str
    description: str

    def __post_init__(self):
        self.symbol = TradeSymbol(self.symbol)


@dataclass
class MarketImport:
    symbol: str
    name: str
    description: str

    def __post_init__(self):
        self.symbol = TradeSymbol(self.symbol)


@dataclass
class MarketExchange:
    symbol: str
    name: str
    description: str

    def __post_init__(self):
        self.symbol = TradeSymbol(self.symbol)


@dataclass
class MarketTransaction:
    waypointSymbol: str
    shipSymbol: str
    tradeSymbol: str
    type: str
    units: int
    pricePerUnit: int
    totalPrice: int
    timestamp: str

    def __post_init__(self):
        self.tradeSymbol = TradeSymbol(self.tradeSymbol)


@dataclass
class MarketTradeGood:
    symbol: str
    type: str
    tradeVolume: int
    supply: str
    activity: str
    purchasePrice: int
    sellPrice: int

    def __post_init__(self):
        self.symbol = TradeSymbol(self.symbol)
        self.supply = SupplyLevel(self.supply)
        self.activity = ActivityLevel(self.activity)


@dataclass
class Market:
    symbol: str
    exports: List[MarketExport]
    imports: List[MarketImport]
    exchange: List[MarketExchange]
    transactions: Optional[List[MarketTransaction]]
    tradeGoods: Optional[List[MarketTradeGood]]
