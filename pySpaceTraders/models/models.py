from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING, Any

from pySpaceTraders.models.enums import *

if TYPE_CHECKING:
    from pySpaceTraders import SpaceTraderClient

###################
# --- GENERIC --- #
###################


@dataclass
class Meta:
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
    meta: Meta


####################
# --- CONTRACT --- #
####################


@dataclass
class ContractPayment:
    """Represents the payment terms of a contract."""

    onAccepted: int
    onFulfilled: int


@dataclass
class ContractDeliverGood:
    """Represents the delivery requirements of a contract."""

    tradeSymbol: TradeSymbol
    destinationSymbol: str
    unitsRequired: int
    unitsFulfilled: int


@dataclass
class ContractTerms:
    """Represents the specific terms and conditions of a contract."""

    deadline: str
    payment: ContractPayment
    deliver: List[ContractDeliverGood]


@dataclass
class Contract:
    """Base Contract Class, represents a single contract."""

    id: str
    factionSymbol: FactionSymbol
    type: ContractType
    terms: ContractTerms
    accepted: bool
    fulfilled: bool
    expiration: str
    deadlineToAccept: Optional[str]
    ApiInstance: Optional[Any]

    def update_contract(self, contract_in) -> None:
        for k, v in contract_in.__dict__.items():
            setattr(self, k, v)
        print("Contract Updated")


@dataclass
class ListContracts:
    """Represents a status_dict containing a list of contracts and associated metadata."""

    data: List[Contract]
    meta: Meta


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
class FactionTrait:
    symbol: FactionTraitSymbol
    name: str
    description: str


@dataclass
class Faction:
    symbol: FactionSymbol
    name: str
    description: str
    headquarters: str
    traits: List[FactionTrait]
    isRecruiting: bool


@dataclass
class ListFactions:
    data: List[Faction]
    meta: Meta


#####################
# --- WAYPOINTS --- #
#####################


@dataclass
class Chart:
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
class WaypointFaction:
    symbol: FactionSymbol


@dataclass
class WaypointOrbital:
    symbol: str


@dataclass
class Waypoint:
    symbol: str
    type: WaypointType
    systemSymbol: Optional[str]
    x: int
    y: int
    orbitals: List[WaypointOrbital]
    traits: Optional[List[WaypointTrait]]
    isUnderConstruction: Optional[bool]
    orbits: Optional[str]
    faction: Optional[WaypointFaction]
    modifiers: Optional[List[WaypointModifier]]
    chart: Optional[Chart]


###################
# --- Systems --- #
###################


@dataclass
class SystemFaction:
    symbol: FactionSymbol


@dataclass
class System:
    symbol: str
    sectorSymbol: str
    type: SystemType
    x: int
    y: int
    waypoints: Optional[List[Waypoint]]
    factions: Optional[List[SystemFaction]]
    distance: Optional[int]


@dataclass
class ListSystems:
    data: List[System]
    meta: Meta


@dataclass
class ListWaypoints:
    data: List[Waypoint]
    meta: Meta


##################
# --- MARKET --- #
##################


@dataclass
class TradeGood:
    symbol: TradeSymbol
    name: str
    description: str


@dataclass
class MarketTransaction:
    waypointSymbol: str
    shipSymbol: str
    tradeSymbol: TradeSymbol
    type: MarketTransactionType
    units: int
    pricePerUnit: int
    totalPrice: int
    timestamp: str


@dataclass
class MarketTradeGood:
    symbol: TradeSymbol
    type: MarketTradeGoodType
    tradeVolume: int
    supply: SupplyLevel
    purchasePrice: int
    sellPrice: int
    activity: Optional[ActivityLevel]


@dataclass
class Market:
    symbol: str
    exports: List[TradeGood]
    imports: List[TradeGood]
    exchange: List[TradeGood]
    transactions: Optional[List[MarketTransaction]]
    tradeGoods: Optional[List[MarketTradeGood]]


@dataclass
class CargoItem:
    symbol: TradeSymbol
    name: str
    description: str
    units: int


@dataclass
class Cargo:
    capacity: int
    units: int
    inventory: List[CargoItem]


@dataclass
class JumpGate:
    symbol: str
    connection: List[str] | None


@dataclass
class ConstructionMaterial:
    tradeSymbol: TradeSymbol
    required: int
    fulfilled: int


@dataclass
class Construction:
    symbol: str
    materials: List[ConstructionMaterial]
    isComplete: bool


@dataclass
class SupplyConstruction:
    construction: Construction
    cargo: Cargo


#################
# --- FLEET --- #
#################


@dataclass
class ShipCrew:
    current: int
    required: int
    capacity: int
    rotation: CrewRotation
    morale: int
    wages: int


@dataclass
class ShipRequirements:
    power: Optional[int]
    crew: Optional[int]
    slots: Optional[int]


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
class Cooldown:
    shipSymbol: str
    totalSeconds: int
    remainingSeconds: int
    expiration: str


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
class FuelConsumed:
    amount: int
    timestamp: str


@dataclass
class ShipFuel:
    current: int
    capacity: int
    consumed: Optional[FuelConsumed]


@dataclass
class ShipRegistration:
    name: str
    factionSymbol: FactionSymbol
    role: ShipRole


@dataclass
class ShipNavRouteWaypoint:
    symbol: str
    type: WaypointType
    systemSymbol: str
    x: int
    y: int


@dataclass
class ShipNavRoute:
    destination: ShipNavRouteWaypoint
    origin: ShipNavRouteWaypoint
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
class ShipRefineIO:
    tradeSymbol: TradeSymbol
    units: int


@dataclass
class ExtractionYield:
    symbol: TradeSymbol
    units: int


@dataclass
class Extraction:
    shipSymbol: str
    yields: ExtractionYield


@dataclass
class Siphon:
    shipSymbol: str
    yields: ExtractionYield


@dataclass
class ShipEvent:
    symbol: EventSymbol
    component: ShipComponent
    name: str
    description: str


@dataclass
class ListShips:
    data: List[Ship]
    meta: Meta


@dataclass
class ShipRefine:
    cargo: Cargo
    cooldown: Cooldown
    produced: List[ShipRefineIO]
    consumed: List[ShipRefineIO]


@dataclass
class ExtractResources:
    cooldown: Cooldown
    extraction: Extraction
    cargo: Cargo
    events: List[ShipEvent]


@dataclass
class SiphonResources:
    cooldown: Cooldown
    siphon: Siphon
    cargo: Cargo
    events: List[ShipEvent]


@dataclass
class NavigateShip:
    fuel: Optional[ShipFuel]
    nav: ShipNav
    cooldown: Optional[Cooldown]
    transaction: Optional[MarketTransaction]
    agent: Optional[Agent]
    events: Optional[List[ShipEvent]]


@dataclass
class BuySellCargo:
    agent: Agent
    cargo: Cargo
    transaction: MarketTransaction


@dataclass
class ScanShips:
    cooldown: Cooldown
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
class ModificationTransaction:
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
    transaction: ModificationTransaction


@dataclass
class ScrapShip:
    agent: Agent
    transaction: ModificationTransaction


@dataclass
class RepairShip:
    agent: Agent
    ship: Ship
    transaction: ModificationTransaction


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
    cooldown: Cooldown
    systems: List[System]


@dataclass
class ScanWaypoints:
    cooldown: Cooldown
    waypoints: List[Waypoint]


class RegisterNewAgent:
    agent: Agent
    contract: Contract
    faction: Faction
    ship: Ship
    token: str


@dataclass
class CreateChart:
    chart: Chart
    waypoint: Waypoint


##################
# --- SURVEY --- #
##################


@dataclass
class SurveyDeposit:
    symbol: DepositSymbol


@dataclass
class Survey:
    signature: str
    symbol: str
    deposits: List[SurveyDeposit]
    expiration: str
    size: SurveySize


@dataclass
class CreateSurvey:
    cooldown: Cooldown
    surveys: List[Survey]


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
class ShipTypeModel:
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
    shipTypes: List[ShipTypeModel]
    modificationsFee: int
    transactions: Optional[List[ShipyardTransaction]]
    ships: Optional[List[ShipyardShip]]
