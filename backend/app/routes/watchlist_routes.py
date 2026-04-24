# app/routes/watchlist_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.watchlist_schema import (
    CreateWatchlistRequest,
    UpdateWatchlistRequest,
    WatchlistResponse
)
from app.services.watchlist_service import (
    create_watchlist,
    get_watchlists,
    get_watchlist_by_id,
    update_watchlist,
    delete_watchlist
)

router = APIRouter(prefix="/watchlists")


@router.post("", response_model=WatchlistResponse)
def create(data: CreateWatchlistRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_watchlist(db, user.id, data.name)


@router.get("", response_model=list[WatchlistResponse])
def list_all(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_watchlists(db, user.id)


@router.get("/{watchlist_id}", response_model=WatchlistResponse)
def get_one(watchlist_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_watchlist_by_id(db, user.id, watchlist_id)


@router.patch("/{watchlist_id}", response_model=WatchlistResponse)
def update(watchlist_id: int, data: UpdateWatchlistRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return update_watchlist(db, user.id, watchlist_id, data.name)


@router.delete("/{watchlist_id}")
def delete(watchlist_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    delete_watchlist(db, user.id, watchlist_id)
    return {"message": "deleted"}