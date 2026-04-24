import pytest

from app.services.watchlist_item_service import (
    create_item,
    get_items,
    update_item,
    delete_item,
    MAX_ITEMS
)
from app.core.errors import AppError, ErrorCode
from app.models.watchlist import Watchlist
from app.models.watchlist_item import WatchlistItem
from app.schemas.watchlist_item_schema import UpdateItemRequest


# ------------------------
# CREATE ITEM
# ------------------------

def test_create_item_success(db_mock):
    watchlist = Watchlist(id=1, user_id=1, items_count=0)
    db_mock.get.return_value = watchlist
    db_mock.query().filter_by().first.return_value = None

    item = create_item(db_mock, 1, 1, 100, "Movie", "movie")

    assert item.watchlist_id == 1
    assert watchlist.items_count == 1

    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()


def test_create_item_watchlist_not_found(db_mock):
    db_mock.get.return_value = None

    with pytest.raises(AppError) as err:
        create_item(db_mock, 1, 1, 100, "Movie", "movie")

    assert err.value.code == ErrorCode.WATCHLIST_NOT_FOUND


def test_create_item_forbidden(db_mock):
    watchlist = Watchlist(id=1, user_id=2, items_count=0)
    db_mock.get.return_value = watchlist

    with pytest.raises(AppError) as err:
        create_item(db_mock, 1, 1, 100, "Movie", "movie")

    assert err.value.code == ErrorCode.FORBIDDEN


def test_create_item_max_reached(db_mock):
    watchlist = Watchlist(id=1, user_id=1, items_count=MAX_ITEMS)
    db_mock.get.return_value = watchlist

    with pytest.raises(AppError) as err:
        create_item(db_mock, 1, 1, 100, "Movie", "movie")

    assert err.value.code == ErrorCode.MAX_ITEMS_REACHED


def test_create_item_duplicate(db_mock):
    watchlist = Watchlist(id=1, user_id=1, items_count=0)
    db_mock.get.return_value = watchlist

    db_mock.query().filter_by().first.return_value = WatchlistItem()

    with pytest.raises(AppError) as err:
        create_item(db_mock, 1, 1, 100, "Movie", "movie")

    assert err.value.code == ErrorCode.ITEM_ALREADY_EXISTS


# ------------------------
# GET ITEMS
# ------------------------

def test_get_items_success(db_mock):
    watchlist = Watchlist(id=1, user_id=1)
    db_mock.get.return_value = watchlist

    fake_items = [WatchlistItem(id=1), WatchlistItem(id=2)]
    db_mock.query().filter_by().all.return_value = fake_items

    result = get_items(db_mock, 1, 1)

    assert result == fake_items


def test_get_items_watchlist_not_found(db_mock):
    db_mock.get.return_value = None

    with pytest.raises(AppError) as err:
        get_items(db_mock, 1, 1)

    assert err.value.code == ErrorCode.WATCHLIST_NOT_FOUND


def test_get_items_forbidden(db_mock):
    watchlist = Watchlist(id=1, user_id=2)
    db_mock.get.return_value = watchlist

    with pytest.raises(AppError) as err:
        get_items(db_mock, 1, 1)

    assert err.value.code == ErrorCode.FORBIDDEN


# ------------------------
# UPDATE ITEM
# ------------------------

def test_update_item_success(db_mock):
    item = WatchlistItem(id=1, watchlist_id=1, notes=None, rating=None)
    watchlist = Watchlist(id=1, user_id=1)

    db_mock.get.side_effect = [item, watchlist]

    data = UpdateItemRequest(notes="Good", rating=8)

    result = update_item(db_mock, 1, 1, data)

    assert result.notes == "Good"
    assert result.rating == 8

    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(item)


def test_update_item_not_found(db_mock):
    db_mock.get.return_value = None

    data = UpdateItemRequest(notes="Good", rating=8)

    with pytest.raises(AppError) as err:
        update_item(db_mock, 1, 1, data)

    assert err.value.code == ErrorCode.ITEM_NOT_FOUND


def test_update_item_forbidden(db_mock):
    item = WatchlistItem(id=1, watchlist_id=1)
    watchlist = Watchlist(id=1, user_id=2)

    db_mock.get.side_effect = [item, watchlist]

    data = UpdateItemRequest(notes="Good", rating=8)

    with pytest.raises(AppError) as err:
        update_item(db_mock, 1, 1, data)

    assert err.value.code == ErrorCode.FORBIDDEN


# ------------------------
# DELETE ITEM
# ------------------------

def test_delete_item_success(db_mock):
    item = WatchlistItem(id=1, watchlist_id=1)
    watchlist = Watchlist(id=1, user_id=1, items_count=2)

    db_mock.get.side_effect = [item, watchlist]

    delete_item(db_mock, 1, 1)

    db_mock.delete.assert_called_once_with(item)
    db_mock.commit.assert_called_once()
    assert watchlist.items_count == 1


def test_delete_item_not_found(db_mock):
    db_mock.get.return_value = None

    with pytest.raises(AppError) as err:
        delete_item(db_mock, 1, 1)

    assert err.value.code == ErrorCode.ITEM_NOT_FOUND


def test_delete_item_forbidden(db_mock):
    item = WatchlistItem(id=1, watchlist_id=1)
    watchlist = Watchlist(id=1, user_id=2)

    db_mock.get.side_effect = [item, watchlist]

    with pytest.raises(AppError) as err:
        delete_item(db_mock, 1, 1)

    assert err.value.code == ErrorCode.FORBIDDEN
