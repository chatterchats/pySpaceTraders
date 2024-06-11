"""
:Date: 8 JUN 2024
:version: 1.0
:Authors: ChatterChats
"""

import json

import httpx

from pySpaceTraders.constants import V2_STARTRADERS_URL, __version__, REQUEST_TYPES
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

    def __init__(self, logger, server_url: str = V2_STARTRADERS_URL):
        """
        Initializes the PySpaceRequest instance with the provided logger, token, and server URL.

        :param PySpaceLogger logger: A logging object used to log information and exceptions.
        :param str server_url: The base URL for the PySpaceTraders API.
        """

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

    @BurstyLimiter(Limiter(2, 1.2), Limiter(10, 10.5))
    def api(
        self,
        method: str,
        endpoint: str,
        path_param: str = "",
        query_params: dict | None = None,
        payload: dict | None = None,
    ) -> dict:
        """
        Makes an HTTP request to the SpaceTraders specified endpoint.

        :param str method:
        :param str endpoint:
        :param str path_param:
        :param dict query_params:
        :param dict payload:

        :return dict:
        """
        if path_param:
            endpoint = f"{endpoint}/{path_param}"
        if method not in REQUEST_TYPES:
            return {"405": f"Invalid request method: {method}"}
        else:
            return self.session.request(
                method=method, url=endpoint, params=query_params, data=payload if payload else None
            ).json()
