from pydantic import BaseModel, StringConstraints
from typing import Annotated

Name = Annotated[
    str,
    StringConstraints(pattern=r"^[a-zA-Z0-9]+$", min_length=1, max_length=50)
]


class CreateWatchlistRequest(BaseModel):
    name: Name


class UpdateWatchlistRequest(BaseModel):
    name: Name


class WatchlistItemResponse(BaseModel):
    id: int
    title: str


class WatchlistResponse(BaseModel):
    id: int
    name: str
    items_count: int
    # items: List[WatchlistItemResponse] = []
