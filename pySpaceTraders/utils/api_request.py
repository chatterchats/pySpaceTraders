import logging
from typing import Optional

import requests
from ratelimit import limits, sleep_and_retry

from pySpaceTraders.constants import __version__, V2_STARTRADERS_URL, REQUEST_TYPES


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
        return requests.get(endpoint, headers=headers, params=params).json()
    elif method == "POST":
        return requests.post(endpoint, headers=headers, data=params).json()
    elif method == "PATCH":
        return requests.patch(endpoint, headers=headers, data=params).json()
