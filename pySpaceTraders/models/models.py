from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING

from pySpaceTraders.models.enums import *

if TYPE_CHECKING:
    from pySpaceTraders import SpaceTraderClient

###################
# --- GENERIC --- #
###################


@dataclass
class ListMeta:
    total: int
    page: int
    pages: int
    limit: int


@dataclass
class ApiError:
    error: str
    message: str


##################
# --- AGENTS --- #
##################


@dataclass
class Agent:
    symbol: str
    headquarters: str
    credits: int
    startingFaction: FactionSymbol
    shipCount: int
    accountId: Optional[str]


@dataclass
class ListAgents:
    data: List[Agent]
    meta: ListMeta


####################
# --- CONTRACT --- #
####################


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
    type: ContractType
    terms: Terms
    accepted: bool
    fulfilled: bool
    expiration: str
    deadlineToAccept: Optional[str]
    ApiInstance: Optional["SpaceTraderClient"]

    def update_contract(self, contract_in) -> None:
        for k, v in contract_in.__dict__.items():
            setattr(self, k, v)
        print("Contract Updated")


@dataclass
class ListContracts:
    """Represents a status_dict containing a list of contracts and associated metadata."""

    data: List[Contract]
    meta: ListMeta


@dataclass
class AcceptContract:
    agent: Agent
    contract: Contract


@dataclass
class DeliverCargo:
    contract: Contract
    cargo: "Cargo"


@dataclass
class FulfillContract:
    agent: Agent
    contract: Contract


####################
# --- FACTIONS --- #
####################


@dataclass
class Trait:
    symbol: FactionTraitSymbol
    name: str
    description: str


@dataclass
class Faction:
    symbol: FactionSymbol
    name: str
    description: str
    headquarters: str
    traits: List[Trait]
    isRecruiting: bool


@dataclass
class ListFactions:
    data: List[Faction]
    meta: ListMeta


#####################
# --- WAYPOINTS --- #
#####################


@dataclass
class ChartWaypoint:
    waypointSymbol: Optional[str]
    submittedBy: Optional[str]
    submittedOn: Optional[str]


@dataclass
class WaypointModifier:
    symbol: WaypointModifierSymbol
    name: str
    description: str


@dataclass
class WaypointTrait:
    symbol: WaypointTraitSymbol
    name: str
    description: str


@dataclass
class WaypointFactionSymbol:
    symbol: FactionSymbol


@dataclass
class Orbital:
    symbol: str


@dataclass
class SystemWaypoint:
    symbol: str
    type: WaypointType
    x: int
    y: int
    orbitals: List[Orbital]
    orbits: Optional[str]


@dataclass
class Waypoint(SystemWaypoint):
    systemSymbol: str
    isUnderConstruction: bool
    traits: List[WaypointTrait]
    faction: Optional[WaypointFactionSymbol]
    modifiers: Optional[List[WaypointModifier]]
    chart: Optional[ChartWaypoint]


###################
# --- Systems --- #
###################


@dataclass
class System:
    symbol: str
    sectorSymbol: str
    type: SystemType
    x: int
    y: int
    waypoints: Optional[List[SystemWaypoint]]
    factions: Optional[List[FactionSymbol]]


@dataclass
class ListSystems:
    data: List[System]
    meta: ListMeta


@dataclass
class ListWaypoints:
    data: List[Waypoint]
    meta: ListMeta


@dataclass
class MarketImportExportExchange:
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
    exports: List[MarketImportExportExchange]
    imports: List[MarketImportExportExchange]
    exchange: List[MarketImportExportExchange]
    transactions: Optional[List[MarketTransaction]]
    tradeGoods: Optional[List[MarketTradeGood]]


@dataclass
class Item:
    symbol: TradeSymbol
    name: str
    description: str
    units: int


@dataclass
class Cargo:
    capacity: int
    units: int
    inventory: List[Item]


@dataclass
class ConstructionMaterial:
    tradeSymbol: TradeSymbol
    required: int
    fulfilled: int


@dataclass
class JumpGate:
    symbol: str
    connection: List[str] | None


@dataclass
class ConstructionSite:
    symbol: str
    materials: List[ConstructionMaterial]
    isComplete: bool


@dataclass
class SupplyConstructionSite:
    constructionSite: ConstructionSite
    cargo: Cargo


#################
# --- FLEET --- #
#################


@dataclass
class ShipRequirements:
    power: Optional[int]
    crew: Optional[int]
    slots: Optional[int]


@dataclass
class ShipFrame:
    symbol: ShipFrameSymbol
    name: Optional[str]
    description: Optional[str]
    condition: Optional[float]
    integrity: Optional[float]
    moduleSlots: Optional[int]
    mountingPoints: Optional[int]
    fuelCapacity: Optional[int]
    requirements: Optional[ShipRequirements]


@dataclass
class ShipReactor:
    symbol: ShipReactorSymbol
    name: Optional[str]
    description: Optional[str]
    condition: Optional[float]
    integrity: Optional[float]
    powerOutput: Optional[int]
    requirements: Optional[ShipRequirements]


@dataclass
class ShipEngine:
    symbol: ShipEngineSymbol
    name: Optional[str]
    description: Optional[str]
    condition: Optional[float]
    integrity: Optional[float]
    speed: Optional[int]
    requirements: Optional[ShipRequirements]


@dataclass
class ShipModule:
    symbol: ShipModuleSymbol
    name: str
    description: str
    capacity: Optional[int]
    range: Optional[int]
    requirements: ShipRequirements


@dataclass
class ShipMount:
    symbol: ShipMountSymbol
    name: Optional[str]
    description: Optional[str]
    strength: Optional[int]
    deposits: Optional[List[DepositSymbol]]
    requirements: Optional[ShipRequirements]


@dataclass
class ShipFuelConsumed:
    amount: int
    timestamp: str


@dataclass
class ShipFuel:
    current: int
    capacity: int
    consumed: Optional[ShipFuelConsumed]


@dataclass
class ShipRegistration:
    name: str
    factionSymbol: FactionSymbol
    role: ShipRole


@dataclass
class ShipNavRouteLocation:
    symbol: str
    type: WaypointType
    systemSymbol: str
    x: int
    y: int


@dataclass
class ShipNavRoute:
    destination: ShipNavRouteLocation
    origin: ShipNavRouteLocation
    departureTime: str
    arrival: str


@dataclass
class ShipNav:
    systemSymbol: str
    waypointSymbol: str
    route: ShipNavRoute
    status: ShipNavStatus
    flightMode: ShipNavFlightMode


@dataclass
class ShipCrew:
    current: int
    required: int
    capacity: int
    rotation: str
    morale: int
    wages: int


@dataclass
class ShipCooldown:
    shipSymbol: str
    totalSeconds: int
    remainingSeconds: int
    expiration: str


@dataclass
class ShipRefineIO:
    tradeSymbol: TradeSymbol
    units: int


@dataclass
class ShipExtractionYield:
    symbol: TradeSymbol
    units: int


@dataclass
class ShipExtraction:
    shipSymbol: str
    yields: ShipExtractionYield


@dataclass
class ShipDeposit:
    symbol: DepositSymbol


@dataclass
class ShipEvent:
    symbol: ShipConditionEventSymbol
    component: str
    name: str
    description: str


@dataclass
class Survey:
    signature: str
    symbol: str
    deposits: List[ShipDeposit]
    expiration: str
    size: str


@dataclass
class ShipSiphonYields:
    symbol: TradeSymbol
    units: int


@dataclass
class ShipSiphon:
    shipSymbol: str
    yields: ShipSiphonYields


@dataclass
class Ship:
    symbol: str
    registration: ShipRegistration
    nav: ShipNav
    crew: Optional[ShipCrew]
    frame: Optional[ShipFrame]
    reactor: Optional[ShipReactor]
    engine: ShipEngine
    modules: Optional[List[ShipModule]]
    mounts: Optional[List[ShipMount]]
    cargo: Optional[Cargo]
    fuel: Optional[ShipFuel]


@dataclass
class ListShips:
    data: List[Ship]
    meta: ListMeta


@dataclass
class ShipRefine:
    cargo: Cargo
    cooldown: ShipCooldown
    produced: ShipRefineIO
    consumed: ShipRefineIO


@dataclass
class CreateSurvey:
    cooldown: ShipCooldown
    surveys: List[Survey]


@dataclass
class ExtractResources:
    cooldown: ShipCooldown
    extraction: ShipExtraction
    cargo: Cargo
    events: List[ShipEvent]


@dataclass
class SiphonResources:
    cooldown: ShipCooldown
    siphon: ShipSiphon
    cargo: Cargo
    events: List[ShipEvent]


@dataclass
class NavigateShip:
    fuel: ShipFuel
    cooldown: Optional[ShipCooldown]
    nav: ShipNav
    events: List[ShipEvent]


@dataclass
class BuySellCargo:
    agent: Agent
    cargo: Cargo
    transaction: MarketTransaction


@dataclass
class ScanShips:
    cooldown: ShipCooldown
    ships: List[Ship]


@dataclass
class RefuelShip:
    agent: Agent
    fuel: ShipFuel
    transaction: MarketTransaction


@dataclass
class GetMounts:
    data: List[ShipMount]


@dataclass
class MountScrapRepairTransaction:
    waypointSymbol: str
    shipSymbol: str
    tradeSymbol: Optional[TradeSymbol]
    totalPrice: int
    timestamp: str


@dataclass
class InstallRemoveMount:
    """Returned when Installing or Removing a Mount"""

    agent: Agent
    mounts: List[ShipMount]
    cargo: Cargo
    transaction: MountScrapRepairTransaction


@dataclass
class ScrapShip:
    agent: Agent
    transaction: MountScrapRepairTransaction


@dataclass
class RepairShip:
    agent: Agent
    ship: Ship
    transaction: MountScrapRepairTransaction


@dataclass
class PurchaseShip:
    agent: Agent
    ship: Ship
    transaction: "ShipyardTransaction"


@dataclass
class Announcement:
    title: str
    body: str


@dataclass
class CreditEntry:
    agentSymbol: str
    credits: int


@dataclass
class ChartEntry:
    agentSymbol: str
    chartCount: int


@dataclass
class Leaderboard:
    mostCredits: List[CreditEntry]
    mostSubmittedCharts: List[ChartEntry]


@dataclass
class Link:
    name: str
    url: str


@dataclass
class ServerReset:
    frequency: str
    next: str


@dataclass
class Stats:
    agents: int
    ships: int
    systems: int
    waypoints: int


@dataclass
class Status:
    announcements: List[Announcement]
    description: str
    leaderboards: Leaderboard
    links: List[Link]
    resetDate: str
    serverResets: ServerReset
    stats: Stats
    status: str
    version: str


@dataclass
class ScanSystems:
    cooldown: ShipCooldown
    systems: List[System]


@dataclass
class ScanWaypoints:
    cooldown: ShipCooldown
    waypoints: List[Waypoint]


class RegisterNewAgent:
    agent: Agent
    contract: Contract
    faction: Faction
    ship: Ship
    token: str


@dataclass
class CreateChart:
    chart: ChartWaypoint
    waypoint: Waypoint


####################
# --- SHIPYARD --- #
####################


@dataclass
class ShipyardShip:
    type: ShipType
    name: str
    description: str
    supply: SupplyLevel
    activity: ActivityLevel
    purchasePrice: int
    frame: ShipFrame
    reactor: ShipReactor
    modules: List[ShipModule]
    mounts: List[ShipMount]


@dataclass
class ShipyardShipType:
    type: ShipType


@dataclass
class ShipyardTransaction:
    waypointSymbol: str
    shipSymbol: ShipType
    shipType: ShipType
    price: int
    agentSymbol: str
    timestamp: str


@dataclass
class Shipyard:
    symbol: str
    shipTypes: List[ShipyardShipType]
    transactions: Optional[List[ShipyardTransaction]]
    ships: Optional[List[ShipyardShip]]
    modificationsFee: int
