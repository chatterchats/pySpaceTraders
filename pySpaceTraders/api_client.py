import json
import os.path
from pySpaceTraders.utils import *


class SpaceTraders:
    def __init__(self):
        self.token: str = ""

    @staticmethod
    def status():
        """GET request to acquire server status and announcements."""
        response = make_request("GET", "/").json()
        return parse_status(response)

    def register(
            self, symbol: str, faction: enums.FactionSymbol = enums.FactionSymbol.COSMIC, email: Optional[str] = ""
    ):
        """Creates a new agent and ties it to an account.
        The agent symbol must consist of a 3-14 character string, and will be used to represent your agent.
        This new agent will be tied to a starting faction of your choice, which determines your starting location.
        You will be granted an authorization token.
        You will start with a contract, a command ship, and a small probe ship for reconnaissance, and 150,000 credits.

        New to SpaceTraders? It is recommended to register with the COSMIC faction, as it is well-connected to the rest of the universe.

        ### Parameters
        - callsign: Str
            - Your desired agent symbol. This will be a unique name used to represent your agent, and will be the prefix for your ships.
            - >= 3 characters<= 14 characters Example: "BADGER"
        - *faction: FactionSymbol, (Defaults FactionSymbol.COSMIC)
            - The symbol of the faction. >= 1 characters
        - *email: Optional[str] (Defaults Blank)
            - Your email address. This is used if you reserved your call sign between resets.
        """
        payload = {"symbol": symbol, "faction": faction.value}
        if email:
            payload["email"] = email

        if os.path.isfile("./token.json") and False:
            f = open("token.json")
            self.token = json.load(f)["token"]
            f.close()
            return self.token
        else:
            response = make_request("POST", "/register", params=payload).json()
            if "data" in response.keys():
                token = {"token": response["data"]["token"]}
                self.token = token["token"]
                with open("token.json", "w", encoding="utf-8") as f:
                    json.dump(token, f, indent=4, ensure_ascii=False)
                return self.token
            elif "error" in response.keys():
                return parse_error(response)

    # Agent Endpoints #
    def my_agent(self) -> agent.MyAgent:
        """Fetch single agent details.
        ### Parameters
        - None
        """
        response = make_request("GET", "/my/agent", self.token).json()
        if "error" in response.keys():
            return parse_error(response)
        return agent.MyAgent(**response["data"])

    def list_agents(self, limit: int = 10, page: int = 1) -> agent.ListResponse:
        """Fetch <limit> agents per page, on page <page>.
        ### Parameters
        - limit: int (Defaults 10)
            - How many entries to return per page
            - >= 1 and <= 20
        - page: int (Defaults 1)
            - What entry offset to request
            - >= 1
        """
        # token optional for get_agent
        response = make_request(
            "GET", f"/agents?limit={limit}&page={page}", self.token
        ).json()
        if "error" in response.keys():
            return parse_error(response)
        response["data"] = [agent.Agent(**agent_token) for agent_token in response["data"]]

        return agent.ListResponse(**response)

    def get_agent(self, symbol: str = "CHATS") -> agent.Agent:
        """Fetch single agent details.
        ### Parameters
        - symbol: Str (Defaults FEBA66)
            - The agent symbol
        """
        # token optional for get_agent
        response = make_request("GET", f"/agents/{symbol}", self.token).json()
        if "error" in response.keys():
            return parse_error(response)
        return agent.Agent(**response["data"])

    # Contracts Endpoints #

    def list_contracts(self, limit: int = 10, page: int = 1) -> contract.ListResponse:
        """Fetch <limit> number of contracts on <page> number.
        ### Parameters
        - limit: int (Defaults 10)
            - How many entries to return per page
            - >= 1 and <= 20
        - page: int (Defaults 1)
            - What entry offset to request
            - >= 1
        """
        response = make_request(
            "GET", f"/my/contracts?limit={limit}&page={page}", self.token
        ).json()
        if "error" in response.keys():
            return parse_error(response)
        response["data"] = [
            parse_contract(single_contract) for single_contract in response["data"]
        ]
        return contract.ListResponse(**response)

    def get_contract(self, contract_id: str) -> contract.Contract:
        """Fetch single agent details.
        ### Parameters
        - contract_id: str
            - The unique contract id
        """
        # token optional for get_agent

        response = make_request(
            "GET", f"/my/contracts/{contract_id}", self.token
        ).json()
        if "error" in response.keys():
            return parse_error(response)
        return parse_contract(response["data"])

    def accept_contract(self, contract_id: str) -> contract.ContractAgentResponse:
        """POST request to accept a contract.
        ### Parameters
        - contract_id: str
            - The unique contract id
        """
        response = make_request(
            "POST", f"/my/contracts/{contract_id}/accept", self.token
        ).json()

        if "error" in response.keys():
            return parse_error(response)
        if "data" in response.keys():
            response = response["data"]
            return contract.ContractAgentResponse(**{
                "agent": agent.MyAgent(**response["agent"]),
                "contract": parse_contract(response["contract"])
            })

    def deliver_contract_cargo(self, contract_id: str, ship_symbol: str, trade_symbol: str, units: int) -> contract.DeliverCargoResponse:
        """POST request to accept a contract.
        ### Parameters
        - contract_id: str
            - The unique contract id
        - ship_symbol: str
            - Ship Identifier
        - trade_symbol: str
            - Trade Identifier
        - units: int
            - How many units to deliver
        """
        payload = {
            "shipSymbol": ship_symbol,
            "tradeSymbol": trade_symbol,
            "units": units,
        }
        response = make_request(
            "POST", f"/my/contracts/{contract_id}/deliver", self.token, params=payload
        ).json()
        if "error" in response.keys():
            return parse_error(response)
        return contract.DeliverCargoResponse(**{
            "contract": parse_contract(response["data"]["contract"]),
            "cargo": parse_cargo(response["data"]["cargo"]),
        })

    def fulfill_contract(self, contract_id: str) -> contract.ContractAgentResponse:
        """POST request to complete a contract.
        ### Parameters
        - contract_id: str
            - The unique contract id
        """
        response = make_request(
            "POST", f"/my/contracts/{contract_id}/fulfill", self.token
        ).json()
        if "error" in response.keys():
            return parse_error(response)
        return contract.ContractAgentResponse(**{
            "agent": agent.Agent(**response["data"]["agent"]),
            "contract": parse_contract(response["data"]["contract"])
        })

    # Faction Endpoints #
    def list_factions(self, limit: int = 10, page: int = 1) -> factions.ListResponse:
        """Fetch <limit> number of factions on <page> number.
        ### Parameters
        - limit: int (Defaults 10)
            - How many entries to return per page
            - >= 1 and <= 20
        - page: int (Defaults 1)
            - What entry offset to request
            - >= 1
        """
        response = make_request(
            "GET", f"/factions?limit={limit}&page={page}", self.token
        ).json()
        response["data"] = [
            parse_faction(faction) for faction in response["data"]
        ]
        if "error" in response.keys():
            return parse_error(response)
        return response

    def get_faction(self, faction_symbol: enums.FactionSymbol) -> factions.Faction:
        """GET request to get <faction_symbol> faction's details..
        ### Parameters
        - faction_symbol: str
            - The unique contract id
        """
        if faction_symbol in enums.FactionSymbol:
            response = make_request(
                "GET", f"/factions/{faction_symbol}", self.token
            ).json()
            return parse_faction(response["data"])
        else:
            return {"code": 404, "message": "Faction not found"}
