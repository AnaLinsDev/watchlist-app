from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.watchlist_item_schema import (
    CreateItemRequest,
    ItemResponse,
    UpdateItemRequest,
)

from app.services.watchlist_item_service import (
    create_item,
    delete_item,
    get_items,
    update_item,
)


router = APIRouter(prefix="/items")


# ------------------------
# CREATE ITEM
# ------------------------

@router.post("", response_model=ItemResponse)
def create(
    data: CreateItemRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return create_item(
        db=db,
        user_id=user.id,
        watchlist_id=data.watchlist_id,
        tmdb_id=data.tmdb_id,
        title=data.title,
        type=data.type
    )


# ------------------------
# LIST ITEMS
# ------------------------

@router.get("", response_model=list[ItemResponse])
def list_all(
    watchlistId: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return get_items(db, user.id, watchlistId)


# ------------------------
# UPDATE ITEM (notes, rating)
# ------------------------

@router.patch("/{item_id}", response_model=ItemResponse)
def update(
    item_id: int,
    data: UpdateItemRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return update_item(db, user.id, item_id, data)


# ------------------------
# DELETE ITEM
# ------------------------

@router.delete("/{item_id}")
def delete(
    item_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    delete_item(db, user.id, item_id)
    return {"message": "Item deleted successfully"}
