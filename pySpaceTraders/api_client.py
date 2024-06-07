import json
import os.path
from typing import Optional
from pySpaceTraders.utils import make_request
from pySpaceTraders.models import enums

# Return Models
from pySpaceTraders.models.agent import AgentResponse, AgentListResponse


class SpaceTraders:
    def __init__(self):
        self.token: str = ""

    def status(self):
        response = make_request("GET", "")
        return response

    def register(
            self, callsign: str, faction: enums.FactionSymbol = enums.FactionSymbol.COSMIC, email: Optional[str] = ""
    ):
        """Creates a new agent and ties it to an account. The agent symbol must consist of a 3-14 character string, and will be used to represent your agent. This symbol will prefix the symbol of every ship you own. Agent symbols will be cast to all uppercase characters.

        This new agent will be tied to a starting faction of your choice, which determines your starting location, and will be granted an authorization token, a contract with their starting faction, a command ship that can fly across space with advanced capabilities, a small probe ship that can be used for reconnaissance, and 150,000 credits.

        If you are new to SpaceTraders, It is recommended to register with the COSMIC faction, a faction that is well connected to the rest of the universe. After registering, you should try our interactive quickstart guide which will walk you through basic API requests in just a few minutes.

        ### Parameters
        - callsign: Str
            - Your desired agent symbol. This will be a unique name used to represent your agent, and will be the prefix for your ships. >= 3 characters<= 14 characters Example: "BADGER"
        - *faction: FactionSymbol, (Defaults FactionSymbol.COSMIC)
            - The symbol of the faction. >= 1 characters
        - *email: Optional[str] (Defaults Blank)
            - Your email address. This is used if you reserved your call sign between resets.

        ### Returns
        - Dict
            - Contains JWT Token to authenticate with other endpoints.
        """
        method = "POST"
        endpoint = "register"
        faction = faction.value
        payload = {"symbol": callsign, "faction": faction}
        if email:
            payload["email"] = email

        if os.path.isfile("./token.json"):
            f = open("token.json")
            response = json.load(f)
            f.close()
        else:
            response = make_request(method, endpoint, params=payload).json()
            with open("token.json", "w", encoding="utf-8") as f:
                json.dump(response, f, indent=4, ensure_ascii=False)

        self.token = response["data"]["token"]
        return response

    def my_agent(self) -> AgentResponse:
        """Fetch single agent details.
        ### Parameters
        - None
        ### Returns
        - Dict
            - accountId: Optional[str] | Only if own agent.
            - symbol: str
            - headquarters: str
            - credits: int
            - startingFaction: str
            - shipCount: int
        """
        return make_request("GET", "my/agent", self.token).json()

    def list_agents(self, limit: int = 10, page: int = 1) -> AgentListResponse:
        """Fetch single agent details.
        ### Parameters
        - limit: int (Defaults 10)
            - How many entries to return per page
            - >= 1 and <= 20
        - page: int (Defaults 1)
            - What entry offset to request
            - >= 1
        ### Returns
        - List of Dicts
            - accountId: Optional[str] | Only if own agent.
            - symbol: str
            - headquarters: str
            - credits: int
            - startingFaction: str
            - shipCount: int
        - Dict[str, int]
        """
        # token optional for get_agent
        return make_request(
            "GET", f"/agents?limit={limit}&page={page}", self.token
        ).json()

    def get_agent(self, symbol: str = "FEBA66"):
        """Fetch single agent details.
        ### Parameters
        - symbol: Str (Defaults FEBA66)
            - The agent symbol
        ### Returns
        - Dict
            - accountId: Optional[str] | Only if own agent.
            - symbol: str
            - headquarters: str
            - credits: int
            - startingFaction: str
            - shipCount: int

        """
        # token optional for get_agent
        return make_request("GET", f"/agents/{symbol}", self.token).json()
