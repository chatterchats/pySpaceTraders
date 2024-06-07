import logging
from typing import Optional

import requests
from ratelimit import limits, sleep_and_retry

from pySpaceTraders.constants import __version__, V2_STARTRADERS_URL, REQUEST_TYPES
# Return Models
from pySpaceTraders.models.agent import *
from pySpaceTraders.models.contract import *
from pySpaceTraders.models.factions import *
from pySpaceTraders.models.cargo import *
from pySpaceTraders.models.errors import *
from pySpaceTraders.models.status import *


@sleep_and_retry
@limits(calls=2, period=1.2)
def make_request(
        method: str, endpoint: str, token: Optional[str] = "", params: Optional[dict] = {}
):
    """
    ### Parameters
    - method: str
        - Request Method (GET, POST, PUT, DELETE)
    - endpoint: str
        - Endpoint you are trying to reach
    - *token: Optional[str] (Defaults Blank)
        - Your JWT Token, only needed for authenticated endpoints.
    - *params: Optional[dict] (Defaults Blank)
        - Any payload data.
    """
    headers = {"User-Agent": f"pySpaceTraders/{__version__}"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    method = method.upper()

    if method not in REQUEST_TYPES:
        logging.exception(f"Invalid request method: {method}")
        return None

    endpoint = V2_STARTRADERS_URL + endpoint
    if method == "GET":
        return requests.get(endpoint, headers=headers, params=params)
    elif method == "POST":
        return requests.post(endpoint, headers=headers, data=params)
    elif method == "PATCH":
        return requests.patch(endpoint, headers=headers, data=params)


def parse_error(response):
    response = response["error"]
    code = response["code"]
    error = Error(code).name
    message = response["message"]
    return {"error": error, "message": message}


def parse_contract(contract: dict) -> Contract:
    term = contract["terms"]
    payment = ContractPayment(**term["payment"])
    deliver = [ContractTermsDeliver(**deliver) for deliver in term["deliver"]]
    deadline = term["deadline"]
    contract["terms"] = ContractTerms(deadline=deadline, payment=payment, deliver=deliver)
    return Contract(**contract)


def parse_cargo(cargo: dict) -> Contract:
    cargo["inventory"] = [Item(**item) for item in cargo["inventory"]]
    data = Cargo(**cargo)
    return data


def parse_faction(faction: dict) -> Faction:
    faction["traits"] = [
        FactionTrait(**trait) for trait in faction["traits"]
    ]
    return Faction(**faction)


def parse_status(response: dict) -> Status:
    response["announcements"] = [StatusAnnouncement(**news) for news in response["announcements"]]
    response["leaderboards"]["mostCredits"] = [CreditLeaderboard(**leader) for leader in response["leaderboards"]["mostCredits"]]
    response["leaderboards"]["mostSubmittedCharts"] = [ChartLeaderboard(**leader) for leader in
                                                       response["leaderboards"]["mostSubmittedCharts"]]
    response["leaderboards"] = StatusLeaderboard(**response["leaderboards"])
    response["links"] = [StatusLink(**link) for link in response["links"]]
    response["serverResets"] = StatusReset(**response["serverResets"])
    response["stats"] = StatusStats(**response["stats"])
    return Status(**response)
