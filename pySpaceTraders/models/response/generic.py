from dataclasses import dataclass


@dataclass
class ListMeta:
    total: int
    page: int
    pages: int
    limit: int


@dataclass
class ApiError:
    error: str
    message: str
