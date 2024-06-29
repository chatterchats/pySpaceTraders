from typing import List
from dacite import Config
from pySpaceTraders.models.enums import *

######################
# --- VERSIONING --- #
######################
# We get the version from pyproject.toml cause fuck defining it in multiple places.

__version__ = "0.5.0"

######################
# --- Endpoints --- #
######################

V2_STARTRADERS_URL: str = "https://api.spacetraders.io/v2"
V2_STOPLIGHT_URL = "https://stoplight.io/mocks/spacetraders/spacetraders/96627693"

REQUEST_TYPES: List[str] = ["GET", "POST", "PATCH"]

##################
# --- Dacite --- #
##################

DACITE_CONFIG = Config(
    cast=[
        ActivityLevel,
        ContractType,
        CrewRotation,
        DepositSymbol,
        FactionTraitSymbol,
        FactionSymbol,
        RefinedGoodSymbol,
        EventSymbol,
        MarketTradeGoodType,
        MarketTransactionType,
        ShipComponent,
        ShipEngineSymbol,
        ShipFrameSymbol,
        ShipModuleSymbol,
        ShipMountSymbol,
        ShipNavStatus,
        ShipNavFlightMode,
        ShipReactorSymbol,
        ShipRole,
        ShipType,
        SupplyLevel,
        SystemType,
        TradeSymbol,
        WaypointModifierSymbol,
        WaypointTraitSymbol,
        WaypointType,
    ]
)
