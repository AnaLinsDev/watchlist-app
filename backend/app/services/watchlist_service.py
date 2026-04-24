from sqlalchemy.orm import Session
from app.models.watchlist import Watchlist
from app.core.errors import AppError, ErrorCode


MAX_WATCHLISTS = 4


def create_watchlist(db: Session, user_id: int, name: str):
    count = db.query(Watchlist).filter_by(user_id=user_id).count()
    if count >= MAX_WATCHLISTS:
        raise AppError(ErrorCode.MAX_WATCHLISTS_REACHED)

    existing = db.query(Watchlist).filter_by(user_id=user_id, name=name).first()
    if existing:
        raise AppError(ErrorCode.WATCHLIST_NAME_EXISTS)

    watchlist = Watchlist(name=name, user_id=user_id)

    db.add(watchlist)
    db.commit()
    db.refresh(watchlist)

    return watchlist


def get_watchlists(db: Session, user_id: int):
    return db.query(Watchlist).filter_by(user_id=user_id).all()


def get_watchlist_by_id(db: Session, user_id: int, watchlist_id: int):
    watchlist = db.get(Watchlist, watchlist_id)

    if not watchlist:
        raise AppError(ErrorCode.WATCHLIST_NOT_FOUND)

    if watchlist.user_id != user_id:
        raise AppError(ErrorCode.FORBIDDEN)

    return watchlist


def update_watchlist(db: Session, user_id: int, watchlist_id: int, name: str):
    watchlist = get_watchlist_by_id(db, user_id, watchlist_id)

    existing = db.query(Watchlist).filter_by(user_id=user_id, name=name).first()
    if existing and existing.id != watchlist_id:
        raise AppError(ErrorCode.WATCHLIST_NAME_EXISTS)

    watchlist.name = name

    db.commit()
    db.refresh(watchlist)

    return watchlist


def delete_watchlist(db: Session, user_id: int, watchlist_id: int):
    watchlist = get_watchlist_by_id(db, user_id, watchlist_id)

    db.delete(watchlist)
    db.commit()