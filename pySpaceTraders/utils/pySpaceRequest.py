"""
:Date: 8 JUN 2024
:version: 1.0
:Authors: ChatterChats
"""

import httpx
from datetime import datetime

from pySpaceTraders.constants import (
    V2_STARTRADERS_URL,
    V2_STOPLIGHT_URL,
    __version__,
    REQUEST_TYPES,
)
from pySpaceTraders.utils.pySpaceLimiter import BurstyLimiter, Limiter


class PySpaceRequest:
    """
    A class to manage HTTP requests to the PySpaceTraders API.

    This class handles the creation and configuration of HTTP requests to interact with the PySpaceTraders API.
    It manages session headers, including authentication, and provides rate limiting for API requests.

    :method:`request`

    :param logging.Logger logger: A logging object used to log information and exceptions.
    :param str server_url: The base URL for the PySpaceTraders API.


    """

    def __init__(self, logger, testing: bool = False):
        """
        Initializes the PySpaceRequest instance with the provided logger, token, and server URL.

        :param PySpaceLogger logger: A logging object used to log information and exceptions.
        :param bool testing: Whether launched in testing mode, uses Stoplight api.
        """
        server_url = V2_STARTRADERS_URL if not testing else V2_STOPLIGHT_URL

        self.logger = logger if logger is not None else None
        self.class_id: str = f"pySpaceTraders/{__version__}"
        self.session = httpx.Client(base_url=server_url)
        self.token = ""
        self.session.headers.update(
            {
                "User-Agent": self.class_id,
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def set_token(self, token: str):
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})

    @BurstyLimiter(Limiter(2, 1.2), Limiter(30, 60.6))
    def api(
        self,
        method: str,
        endpoint: str,
        path_param: str | list | None = None,
        query_params: dict | None = None,
        payload: dict | None = None,
    ) -> dict | str:
        """
        Makes an HTTP request to the SpaceTraders specified endpoint.

        :param str method: `REQUEST_TYPES`
        :param str endpoint:
        :param str path_param:
        :param dict query_params:
        :param dict payload:

        :return dict:
        """
        if path_param:
            if "{}" in endpoint:
                if isinstance(path_param, str):
                    endpoint = endpoint.format(*[path_param])
                else:
                    endpoint = endpoint.format(*path_param)

            else:
                endpoint = f"{endpoint}/{path_param}"

        if method not in REQUEST_TYPES:
            return {"405": f"Invalid request method: {method}"}
        else:
            response = self.session.request(
                method=method, url=endpoint, params=query_params, json=payload if payload else None
            )

            if self.logger:
                self.logger.debug(f"Method: {method} | Endpoint: {endpoint}")
                self.logger.debug(
                    f"Path Param: {path_param} | "
                    f"Query Param: {str(query_params)} | "
                    f"Payload: {payload}"
                )
                self.logger.debug(
                    f"Constructed URL: {response.url} | Response: {response.status_code}"
                )

            if "application/json" in response.headers.get("Content-Type", ""):
                return response.json()
            elif "cooldown" in str(response.url):
                now = datetime.now()
                return {
                    "shipSymbol": path_param,
                    "totalSeconds": 0,
                    "remainingSeconds": 0,
                    "expiration": now.strftime("%Y-%m-%dT%H:%M:%S.")
                    + f"{(now.microsecond // 1000):03d}Z",
                }
            else:
                return response.text
