from pydantic import BaseModel, StringConstraints, Field
from typing import Annotated, Optional

from app.models.watchlist_item import MediaType


Title = Annotated[
    str,
    StringConstraints(min_length=1, max_length=150)
]

Notes = Annotated[
    str,
    StringConstraints(max_length=500)
]


class CreateItemRequest(BaseModel):
    watchlist_id: int
    tmdb_id: int
    type: MediaType
    title: Title


class UpdateItemRequest(BaseModel):
    notes: Optional[Notes] = None
    rating: Optional[int] = Field(default=None, ge=0, le=10)


class ItemResponse(BaseModel):
    id: int
    watchlist_id: int
    tmdb_id: int

    title: str
    type: MediaType

    notes: Optional[str] = None
    rating: Optional[int] = None
