import pytest
from unittest.mock import MagicMock
from fastapi import Response
from sqlalchemy.exc import IntegrityError

from app.services.auth_service import register_user, login_user, logout_user
from app.core.errors import AppError, ErrorCode
from app.models.user import User


# ------------------------
# REGISTER
# ------------------------

def test_register_user_success(mocker):
    db = MagicMock()

    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()

    user = register_user(db, "test@test.com", "test", "123456")

    assert user.email == "test@test.com"
    db.add.assert_called_once()
    db.commit.assert_called_once()


def test_register_user_integrity_error(mocker):
    db = MagicMock()

    db.commit.side_effect = IntegrityError("", "", "")

    with pytest.raises(AppError) as err:
        register_user(db, "test@test.com", "test", "123456")

    assert err.value.code == ErrorCode.USER_ALREADY_EXISTS


# ------------------------
# LOGIN
# ------------------------

def test_login_user_success(mocker):
    db = MagicMock()
    response = Response()

    fake_user = User(id=1, email="test@test.com", password="hashed")

    db.query().filter().first.return_value = fake_user

    mocker.patch("app.services.auth_service.verify_password", return_value=True)
    mocker.patch("app.services.auth_service.create_access_token", return_value="token")

    user = login_user(db, response, "test@test.com", "123456")

    assert user == fake_user
    assert "access_token" in response.headers.get("set-cookie").lower()


def test_login_user_invalid_credentials(mocker):
    db = MagicMock()
    response = Response()

    db.query().filter().first.return_value = None

    with pytest.raises(AppError) as err:
        login_user(db, response, "test@test.com", "wrong")

    assert err.value.code == ErrorCode.INVALID_CREDENTIALS


# ------------------------
# LOGOUT
# ------------------------

def test_logout_user():
    response = Response()

    logout_user(response)

    cookies = response.headers.get("set-cookie", "")
    assert "access_token" in cookies.lower()
