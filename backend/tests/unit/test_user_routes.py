import pytest
from fastapi import Response
from unittest.mock import MagicMock
from jose import JWTError

from app.schemas.user_schema import UpdateUserRequest
from app.core.errors import AppError, ErrorCode
from app.services.user_service import delete_user, update_user
from app.dependencies.auth import get_current_user
from app.models.user import User
from sqlalchemy.exc import IntegrityError

# ------------------------
# GET USER
# ------------------------


def test_get_current_user_success(mocker, db_mock):
    fake_user = User(id=1, email="test@test.com", password="hashed")

    # mock JWT
    mocker.patch(
        "app.core.security.jwt.decode",
        return_value={"sub": 1}
    )

    # mock repository
    mocker.patch(
        "app.dependencies.auth.get_user_by_id",
        return_value=fake_user
    )

    user = get_current_user(
        access_token="valid_token",
        db=db_mock
    )

    assert user == fake_user


def test_get_current_user_no_token(db_mock):
    with pytest.raises(AppError) as err:
        get_current_user(access_token=None, db=db_mock)

    assert err.value.code == ErrorCode.NOT_AUTHENTICATED


def test_get_current_user_invalid_token(mocker, db_mock):
    mocker.patch(
        "app.core.security.jwt.decode",
        side_effect=JWTError()
    )

    with pytest.raises(AppError) as err:
        get_current_user(
            access_token="invalid_token",
            db=db_mock
        )

    assert err.value.code == ErrorCode.INVALID_TOKEN


def test_get_current_user_user_not_found(mocker, db_mock):
    mocker.patch(
        "app.core.security.jwt.decode",
        return_value={"sub": 1}
    )

    mocker.patch(
        "app.repositories.user_repository",
        return_value=None
    )

    with pytest.raises(AppError) as err:
        get_current_user(
            access_token="valid_token",
            db=db_mock
        )

    assert err.value.code == ErrorCode.USER_NOT_FOUND

# ------------------------
# UPDATE USER
# ------------------------


def test_update_user_success(mocker, db_mock):
    fake_user = User(id=1, email="old@test.com", username="old", password="hashed")

    db_mock.get.return_value = fake_user

    mocker.patch("app.services.user_service.verify_password", return_value=True)

    data = UpdateUserRequest(
        id=1,
        email="new@test.com",
        username="newuser",
        current_password="123456"
    )

    user = update_user(1, db_mock, data)

    assert user.email == "new@test.com"
    assert user.username == "newuser"

    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(fake_user)


def test_update_user_not_found(db_mock):
    db_mock.get.return_value = None

    data = UpdateUserRequest(
        id=1,
        current_password="123456"
    )

    with pytest.raises(AppError) as err:
        update_user(1, db_mock, data)

    assert err.value.code == ErrorCode.USER_NOT_FOUND


def test_update_user_invalid_password(mocker, db_mock):
    fake_user = User(id=1, password="hashed")
    db_mock.get.return_value = fake_user

    mocker.patch("app.services.user_service.verify_password", return_value=False)

    data = UpdateUserRequest(
        id=1,
        current_password="wrong"
    )

    with pytest.raises(AppError) as err:
        update_user(1, db_mock, data)

    assert err.value.code == ErrorCode.INVALID_CURRENT_PASSWORD


def test_update_user_password_hash(mocker, db_mock):
    fake_user = User(id=1, password="hashed")
    db_mock.get.return_value = fake_user

    mocker.patch("app.services.user_service.verify_password", return_value=True)
    mocker.patch("app.services.user_service.hash_password", return_value="new_hashed")

    data = UpdateUserRequest(
        id=1,
        password="newpass123",
        current_password="123456"
    )

    user = update_user(1, db_mock, data)

    assert user.password == "new_hashed"


def test_update_user_email_conflict(mocker, db_mock):
    fake_user = User(id=1, password="hashed")
    db_mock.get.return_value = fake_user

    mocker.patch("app.services.user_service.verify_password", return_value=True)

    db_mock.commit.side_effect = IntegrityError(
        statement=None,
        params=None,
        orig=Exception("email already exists")
    )

    data = UpdateUserRequest(
        id=1,
        email="existing@test.com",
        current_password="123456"
    )

    with pytest.raises(AppError) as err:
        update_user(1, db_mock, data)

    assert err.value.code == ErrorCode.EMAIL_ALREADY_EXISTS


def test_update_user_username_conflict(mocker, db_mock):
    fake_user = User(id=1, password="hashed")
    db_mock.get.return_value = fake_user

    mocker.patch("app.services.user_service.verify_password", return_value=True)

    db_mock.commit.side_effect = IntegrityError(
        statement=None,
        params=None,
        orig=Exception("username already exists")
    )

    data = UpdateUserRequest(
        id=1,
        username="existinguser",
        current_password="123456"
    )

    with pytest.raises(AppError) as err:
        update_user(1, db_mock, data)

    assert err.value.code == ErrorCode.USERNAME_ALREADY_EXISTS

# ------------------------
# DELETE USER
# ------------------------


def test_delete_user_success(db_mock):
    db_mock.commit = MagicMock()
    db_mock.delete = MagicMock()

    fake_user = User(id=1, email="test@test.com", password="hashed")
    db_mock.get.return_value = fake_user

    response = Response()
    user_id = 1

    delete_user(user_id, db_mock, response)

    # delete was called with correct user
    db_mock.delete.assert_called_once_with(fake_user)

    # commit happened
    db_mock.commit.assert_called_once()

    # cookie was cleared
    cookies = response.headers.get("set-cookie", "")
    assert "access_token" in cookies.lower()
