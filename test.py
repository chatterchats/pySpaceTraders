# TODO: Implement Testing
import string
import random

from pySpaceTraders import SpaceTraderClient
from pySpaceTraders.models.models import *


TEST_NAME = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
client = SpaceTraderClient(TEST_NAME, testing=True, log=True, debug=True)
assert isinstance(client, SpaceTraderClient), "client is not a SpaceTraderClient Class"

status = client.status()
assert isinstance(status, Status), "client is not a Status Class"

agent = client.my_agent()
assert isinstance(agent, Agent), "agent is not a Agent Class"

agent_list = client.list_agents()
assert isinstance(agent_list, ListAgents), "agent list is not a ListAgents Class"

other_agent = client.get_agent("CHATTERCHATS")
assert isinstance(other_agent, Agent), "other_agent is not a Agent Class"

contracts = client.list_contracts()
assert isinstance(contracts, ListContracts), "contracts is not a ListContracts Class"

contract = client.get_contract("CHATTERCHATS")
assert isinstance(contract, Contract), "contract is not a Contract Class"

negotiated_contract = client.negotiate_contract("CHATTERCHATS")
assert isinstance(negotiated_contract, Contract), "negotiated_contract is not a Contract Class"

accept_contract = client.accept_contract("CHATTERCHATS")
assert isinstance(accept_contract, AcceptContract), "accept_contract is not a AcceptContract Class"

deliver_cargo = client.deliver_contract_cargo("ContractID", "ShipID", TradeSymbol.COPPER_ORE, 5)
assert isinstance(deliver_cargo, DeliverCargo), "deliver_cargo is not a DeliverCargo Class"

fulfill_contract = client.fulfill_contract("CHATTERCHATS")
assert isinstance(
    fulfill_contract, FulfillContract
), "fulfill_contract is not a FulfillContract Class"

list_factions = client.list_factions()
assert isinstance(list_factions, ListFactions), "list_factions is not a ListFactions Class"

get_faction = client.get_faction(FactionSymbol.COSMIC)
assert isinstance(get_faction, Faction), "get_faction is not a Faction Class"

list_systems = client.list_systems()
assert isinstance(list_systems, ListSystems), "list_systems is not a ListSystems Class"

get_system = client.get_system("CHATTER-CHATS")
assert isinstance(get_system, System), "get_system is not a System Class"

list_system_waypoints = client.list_system_waypoints("CHATTER-CHATS")
assert isinstance(list_system_waypoints, ListWaypoints)

get_waypoint = client.get_waypoint("CHATTER-CHATS-A1")
assert isinstance(get_waypoint, Waypoint), "get_waypoint is not a Waypoint Class"

get_market = client.get_market("CHATTER-CHATS-A1")
assert isinstance(get_market, Market), "get_market is not a Market Class"

get_shipyard = client.get_shipyard("CHATTER-CHATS-A1")
assert isinstance(get_shipyard, Shipyard), "get_shipyard is not a Shipyard Class"

get_jumpgate = client.get_jumpgate("CHATTER-CHATS-A1")
assert isinstance(get_jumpgate, JumpGate), "get_jumpgate is not a JumpGate Class"

get_construction = client.get_construction("CHATTER-CHATS-A1")
assert isinstance(get_construction, Construction), "get_construction is not a Construction Class"

supply_construction = client.supply_construction(
    "CHATTER-CHATS-A1", "CHATTERCHATS", TradeSymbol.COPPER_ORE, 5
)
assert isinstance(
    supply_construction, SupplyConstruction
), "supply_construction is not a SupplyConstruction Class"
