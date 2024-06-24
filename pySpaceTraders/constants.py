import tomllib
from typing import List
from os.path import isfile

######################
# --- VERSIONING --- #
######################
# We get the version from pyproject.toml cause fuck defining it in multiple places.

pyproject_toml_path = "./pyproject.toml"
if isfile(pyproject_toml_path):
    with open(pyproject_toml_path, "rb") as f:
        data = tomllib.load(f)
        __version__ = data["tool"]["poetry"]["version"]

######################
# --- Endpoints --- #
######################

V2_STARTRADERS_URL: str = "https://api.spacetraders.io/v2"
V2_STOPLIGHT_URL = "https://stoplight.io/mocks/spacetraders/spacetraders/96627693"

REQUEST_TYPES: List[str] = ["GET", "POST", "PATCH"]
