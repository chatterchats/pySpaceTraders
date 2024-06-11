from dataclasses import dataclass


@dataclass
class ListMeta:
    total: int
    page: int
    limit: int
