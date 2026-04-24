from sqlalchemy.orm import Session

from app.models.watchlist import Watchlist
from app.models.watchlist_item import WatchlistItem
from app.core.errors import AppError, ErrorCode
from app.schemas.watchlist_item_schema import UpdateItemRequest


MAX_ITEMS = 10


def create_item(db: Session,
                user_id: int,
                watchlist_id: int,
                tmdb_id: int,
                title: str,
                type):
    watchlist = db.get(Watchlist, watchlist_id)

    if not watchlist:
        raise AppError(ErrorCode.WATCHLIST_NOT_FOUND)

    if watchlist.user_id != user_id:
        raise AppError(ErrorCode.FORBIDDEN)

    if watchlist.items_count >= MAX_ITEMS:
        raise AppError(ErrorCode.MAX_ITEMS_REACHED)

    existing = db.query(WatchlistItem).filter_by(
        watchlist_id=watchlist_id,
        tmdb_id=tmdb_id
    ).first()

    if existing:
        raise AppError(ErrorCode.ITEM_ALREADY_EXISTS)

    item = WatchlistItem(
        watchlist_id=watchlist_id,
        tmdb_id=tmdb_id,
        title=title,
        type=type,
        notes=None,
        rating=None
    )

    try:
        db.add(item)
        watchlist.items_count += 1
        db.commit()

        return item
    except Exception:
        db.rollback()
        raise


def get_items(db: Session, user_id: int, watchlist_id: int):
    watchlist = db.get(Watchlist, watchlist_id)

    if not watchlist:
        raise AppError(ErrorCode.WATCHLIST_NOT_FOUND)

    if watchlist.user_id != user_id:
        raise AppError(ErrorCode.FORBIDDEN)

    return db.query(WatchlistItem).filter_by(watchlist_id=watchlist_id).all()


def update_item(db: Session, user_id: int, item_id: int, data: UpdateItemRequest):
    item = db.get(WatchlistItem, item_id)

    if not item:
        raise AppError(ErrorCode.ITEM_NOT_FOUND)

    watchlist = db.get(Watchlist, item.watchlist_id)

    if watchlist.user_id != user_id:
        raise AppError(ErrorCode.FORBIDDEN)

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)

    return item


def delete_item(db: Session, user_id: int, item_id: int):
    item = db.get(WatchlistItem, item_id)

    if not item:
        raise AppError(ErrorCode.ITEM_NOT_FOUND)

    watchlist = db.get(Watchlist, item.watchlist_id)

    if watchlist.user_id != user_id:
        raise AppError(ErrorCode.FORBIDDEN)

    try:
        db.delete(item)
        watchlist.items_count = max(0, watchlist.items_count - 1)
        db.commit()
    except Exception:
        db.rollback()
        raise
