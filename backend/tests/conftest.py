import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.main import app
from app.dependencies.auth import get_current_user
from app.database import get_db
from app.models.user import User


# ------------------------
# UNIT TEST DB MOCK
# ------------------------

@pytest.fixture
def db_mock():
    return MagicMock()


# ------------------------
# FAKE USER
# ------------------------

@pytest.fixture
def fake_user():
    return User(
        id=1,
        email="test@test.com",
        username="test",
        password="hashed"
    )


# ------------------------
# AUTH OVERRIDE
# ------------------------

@pytest.fixture
def override_auth(fake_user):
    def _override():
        return fake_user

    app.dependency_overrides[get_current_user] = _override
    yield
    app.dependency_overrides.pop(get_current_user, None)


# ------------------------
# DB OVERRIDE (INTEGRATION)
# ------------------------

@pytest.fixture
def override_db():
    db = MagicMock()

    app.dependency_overrides[get_db] = lambda: db
    yield db
    app.dependency_overrides.pop(get_db, None)


# ------------------------
# TEST CLIENT
# ------------------------

@pytest.fixture
def client():
    return TestClient(app)
