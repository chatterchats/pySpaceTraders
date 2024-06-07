import logging
from typing import Optional

import requests
from ratelimit import limits, sleep_and_retry

from pySpaceTraders.constants import __version__, V2_STARTRADERS_URL, REQUEST_TYPES
from pySpaceTraders.models import agent, cargo, contract, enums, errors, factions, status


@sleep_and_retry
@limits(calls=2, period=1.2)
def make_request(
        method: str, endpoint: str, token: Optional[str] = "", params: Optional[dict] = ""
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
    error = errors.Codes(code).name
    message = response["message"]
    return {"error": error, "message": message}


def parse_contract(contract_in: dict) -> contract.Contract:
    term = contract_in["terms"]
    payment = contract.Payment(**term["payment"])
    deliver = [contract.DeliverTerms(**deliver) for deliver in term["deliver"]]
    deadline = term["deadline"]
    contract_in["terms"] = contract.Terms(deadline=deadline, payment=payment, deliver=deliver)
    return contract.Contract(**contract_in)


def parse_cargo(cargo_in: dict) -> contract.Contract:
    cargo_in["inventory"] = [cargo.Item(**item) for item in cargo_in["inventory"]]
    data = cargo.Cargo(**cargo_in)
    return data


def parse_faction(faction: dict) -> factions.Faction:
    faction["traits"] = [
        factions.Trait(**trait) for trait in faction["traits"]
    ]
    return factions.Faction(**faction)


def parse_status(response: dict) -> status.Status:
    response["announcements"] = [status.Announcement(**news) for news in response["announcements"]]
    response["leaderboards"]["mostCredits"] = [status.CreditEntry(**leader) for leader in response["leaderboards"]["mostCredits"]]
    response["leaderboards"]["mostSubmittedCharts"] = [status.ChartEntry(**leader) for leader in
                                                       response["leaderboards"]["mostSubmittedCharts"]]
    response["leaderboards"] = status.Leaderboard(**response["leaderboards"])
    response["links"] = [status.Link(**link) for link in response["links"]]
    response["serverResets"] = status.ServerReset(**response["serverResets"])
    response["stats"] = status.Stats(**response["stats"])
    return status.Status(**response)
