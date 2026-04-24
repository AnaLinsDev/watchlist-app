import pytest

from app.services.watchlist_service import (
    create_watchlist,
    get_watchlists,
    get_watchlist_by_id,
    update_watchlist,
    delete_watchlist,
)
from app.models.watchlist import Watchlist
from app.core.errors import AppError, ErrorCode


# ------------------------
# CREATE WATCHLIST
# ------------------------

def test_create_watchlist_success(db_mock):
    db_mock.query.return_value.filter_by.return_value.count.return_value = 0
    db_mock.query.return_value.filter_by.return_value.first.return_value = None

    watchlist = create_watchlist(db_mock, user_id=1, name="MyList")

    assert watchlist.name == "MyList"
    assert watchlist.user_id == 1

    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once()


def test_create_watchlist_max_limit(db_mock):
    db_mock.query.return_value.filter_by.return_value.count.return_value = 4

    with pytest.raises(AppError) as err:
        create_watchlist(db_mock, user_id=1, name="MyList")

    assert err.value.code == ErrorCode.MAX_WATCHLISTS_REACHED


def test_create_watchlist_name_exists(db_mock):
    db_mock.query.return_value.filter_by.return_value.count.return_value = 0
    db_mock.query.return_value.filter_by.return_value.first.return_value = Watchlist()

    with pytest.raises(AppError) as err:
        create_watchlist(db_mock, user_id=1, name="MyList")

    assert err.value.code == ErrorCode.WATCHLIST_NAME_EXISTS


# ------------------------
# GET WATCHLISTS
# ------------------------

def test_get_watchlists(db_mock):
    fake_lists = [Watchlist(id=1), Watchlist(id=2)]

    db_mock.query.return_value.filter_by.return_value.all.return_value = fake_lists

    result = get_watchlists(db_mock, user_id=1)

    assert result == fake_lists


# ------------------------
# GET WATCHLIST BY ID
# ------------------------

def test_get_watchlist_by_id_success(db_mock):
    fake_watchlist = Watchlist(id=1, user_id=1)

    db_mock.get.return_value = fake_watchlist

    result = get_watchlist_by_id(db_mock, user_id=1, watchlist_id=1)

    assert result == fake_watchlist


def test_get_watchlist_by_id_not_found(db_mock):
    db_mock.get.return_value = None

    with pytest.raises(AppError) as err:
        get_watchlist_by_id(db_mock, user_id=1, watchlist_id=1)

    assert err.value.code == ErrorCode.WATCHLIST_NOT_FOUND


def test_get_watchlist_by_id_forbidden(db_mock):
    fake_watchlist = Watchlist(id=1, user_id=2)

    db_mock.get.return_value = fake_watchlist

    with pytest.raises(AppError) as err:
        get_watchlist_by_id(db_mock, user_id=1, watchlist_id=1)

    assert err.value.code == ErrorCode.FORBIDDEN


# ------------------------
# UPDATE WATCHLIST
# ------------------------

def test_update_watchlist_success(db_mock):
    fake_watchlist = Watchlist(id=1, user_id=1, name="Old")

    db_mock.get.return_value = fake_watchlist
    db_mock.query.return_value.filter_by.return_value.first.return_value = None

    result = update_watchlist(db_mock, user_id=1, watchlist_id=1, name="New")

    assert result.name == "New"

    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(fake_watchlist)


def test_update_watchlist_name_conflict(db_mock):
    fake_watchlist = Watchlist(id=1, user_id=1, name="Old")
    conflicting = Watchlist(id=2, user_id=1, name="New")

    db_mock.get.return_value = fake_watchlist
    db_mock.query.return_value.filter_by.return_value.first.return_value = conflicting

    with pytest.raises(AppError) as err:
        update_watchlist(db_mock, user_id=1, watchlist_id=1, name="New")

    assert err.value.code == ErrorCode.WATCHLIST_NAME_EXISTS


# ------------------------
# DELETE WATCHLIST
# ------------------------

def test_delete_watchlist_success(db_mock):
    fake_watchlist = Watchlist(id=1, user_id=1)

    db_mock.get.return_value = fake_watchlist

    delete_watchlist(db_mock, user_id=1, watchlist_id=1)

    db_mock.delete.assert_called_once_with(fake_watchlist)
    db_mock.commit.assert_called_once()
