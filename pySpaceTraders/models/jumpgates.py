from dataclasses import dataclass
from typing import List


@dataclass
class JumpGate:
    symbol: str
    connection: List[str] | None
