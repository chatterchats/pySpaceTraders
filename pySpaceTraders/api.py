import json
import os.path

from pySpaceTraders.models import enums, agent, contract
from pySpaceTraders.utils.api_request import *
from pySpaceTraders.utils.parsers import *


class Client:
    """SpaceTraders API Client Handler"""

    def __init__(self):
        self.token: str = ""

    @staticmethod
    def status():
        """Server Status and Announcements."""
        response = make_request("GET", "/")
        return parse_status(response)

    def register(
            self, symbol: str, faction: enums.FactionSymbol = enums.FactionSymbol.COSMIC, email: Optional[str] = ""
    ):
        """Register a New Agent."""

        payload = {"symbol": symbol, "faction": faction.value}

        if email:
            payload["email"] = email

        if os.path.isfile("./token.json"):
            f = open("token.json")
            self.token = json.load(f)["token"]
            f.close()
            return self.token
        else:
            response = make_request("POST", "/register", params=payload)
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
        """Fetch your agent's details"""
        response = make_request("GET", "/my/agent", self.token)
        if "error" in response.keys():
            return parse_error(response)
        return agent.MyAgent(**response["data"])

    def list_agents(self, limit: int = 10, page: int = 1) -> agent.ListResponse:
        """List all agents. (Paginated)"""
        # token optional for get_agent
        response = make_request(
            "GET", f"/agents?limit={limit}&page={page}", self.token
        )
        if "error" in response.keys():
            return parse_error(response)
        response["data"] = [agent.Agent(**agent_token) for agent_token in response["data"]]

        return agent.ListResponse(**response)

    def get_agent(self, symbol: str = "CHATS") -> agent.Agent:
        """Fetch single agent details."""
        # token optional for get_agent
        response = make_request("GET", f"/agents/{symbol}", self.token)
        if "error" in response.keys():
            return parse_error(response)
        return agent.Agent(**response["data"])

    # Contracts Endpoints #
    def list_contracts(self, limit: int = 10, page: int = 1):
        """Paginated list all of your contracts. (Paginated)"""
        response = make_request(
            "GET", f"/my/contracts?limit={limit}&page={page}", self.token
        )
        if "error" in response.keys():
            return parse_error(response)
        response["contracts"] = [
            parse_contract({**single_contract, "ApiInstance": self}) for single_contract in response["data"]
        ]
        response.pop("data")
        return response

    def get_contract(self, contract_id: str) -> contract.Contract:
        """Fetch single contract details"""
        # token optional for get_agent

        response = make_request(
            "GET", f"/my/contracts/{contract_id}", self.token
        )
        if "error" in response.keys():
            return parse_error(response)
        return parse_contract({**response["data"], "ApiInstance": self})

    def accept_contract(self, contract_id: str) -> contract.ContractAgentResponse:
        """Accept a contract."""
        response = make_request(
            "POST", f"/my/contracts/{contract_id}/accept", self.token
        )

        if "error" in response.keys():
            return parse_error(response)
        if "data" in response.keys():
            response = response["data"]
            return contract.ContractAgentResponse(**{
                "agent": agent.MyAgent(**response["agent"]),
                "contract": parse_contract(response["contract"])
            })

    def deliver_contract_cargo(self, contract_id: str, ship_symbol: str, trade_symbol: str, units: int) -> contract.DeliverResponse:
        """ Deliver cargo for a given contract."""
        payload = {
            "shipSymbol": ship_symbol,
            "tradeSymbol": trade_symbol,
            "units": units,
        }
        response = make_request(
            "POST", f"/my/contracts/{contract_id}/deliver", self.token, params=payload
        )
        if "error" in response.keys():
            return parse_error(response)
        return contract.DeliverResponse(**{
            "contract": parse_contract(response["data"]["contract"]),
            "cargo": parse_cargo(response["data"]["cargo"]),
        })

    def fulfill_contract(self, contract_id: str) -> contract.ContractAgentResponse:
        """Fulfill (complete) a contract."""
        response = make_request(
            "POST", f"/my/contracts/{contract_id}/fulfill", self.token
        )
        if "error" in response.keys():
            return parse_error(response)
        return contract.ContractAgentResponse(**{
            "agent": agent.Agent(**response["data"]["agent"]),
            "contract": parse_contract(response["data"]["contract"])
        })

    # Faction Endpoints #
    def list_factions(self, limit: int = 10, page: int = 1) -> factions.ListResponse:
        """List all discovered factions in the game. (Paginated)"""
        response = make_request(
            "GET", f"/factions?limit={limit}&page={page}", self.token
        )
        response["data"] = [
            parse_faction(faction) for faction in response["data"]
        ]
        if "error" in response.keys():
            return parse_error(response)
        return response

    def get_faction(self, faction_symbol: enums.FactionSymbol) -> factions.Faction | dict[str, str | int]:
        """View the details of a faction."""
        if faction_symbol in enums.FactionSymbol:
            response = make_request(
                "GET", f"/factions/{faction_symbol}", self.token
            )
            return parse_faction(response["data"])
        else:
            return {"code": 404, "message": "Faction not found"}
