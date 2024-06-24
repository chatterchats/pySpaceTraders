from typing import List, Literal

######################
# --- VERSIONING --- #
######################

__MAJOR__: int = 0
__MINOR__: int = 5
__PATCH__: int = 0
__SEGMENT__: Literal["a"] | Literal["b"] | Literal["rc"] | Literal["dev"] | Literal[""] = ""
"""Identifies Alpha, Beta, or Release Candidate pre-release segments"""
__SEGNUM__: int | Literal[""] = ""
"""Identifies Alpha, Beta, or Release Candidate pre-release segment number"""

__version__ = f"{__MAJOR__}.{__MINOR__}.{__PATCH__}{__SEGMENT__}{__SEGNUM__ if __SEGMENT__ else ""}"

######################
# --- Endpoints --- #
######################

V2_STARTRADERS_URL: str = "https://api.spacetraders.io/v2"
V2_STOPLIGHT_URL = "https://stoplight.io/mocks/spacetraders/spacetraders/96627693"

REQUEST_TYPES: List[str] = ["GET", "POST", "PATCH"]
