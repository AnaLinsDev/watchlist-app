from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.main import app
from app.routes.auth_routes import get_db

client = TestClient(app)


# ------------------------
# FAKE USER (important)
# ------------------------

class FakeUser:
    def __init__(self):
        self.id = 1
        self.email = "test@test.com"
        self.username = "test"
        self.password = "hashed_password"


# ------------------------
# DB OVERRIDE
# ------------------------

def override_get_db():
    db = MagicMock()
    yield db


app.dependency_overrides[get_db] = override_get_db


# ------------------------
# REGISTER
# ------------------------

def test_register_route_success(mocker):
    mocker.patch("app.controllers.auth_controller.register_user",
                 return_value=FakeUser()
                 )

    response = client.post("/auth/register", json={
        "email": "test@test.com",
        "username": "test",
        "password": "123456"
    })

    assert response.status_code == 200
    assert response.json()["email"] == "test@test.com"


# ------------------------
# LOGIN
# ------------------------

def test_login_route_success(mocker):
    mocker.patch(
        "app.controllers.auth_controller.login_user",
        return_value=FakeUser()
    )

    response = client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "123456"
    })

    assert response.status_code == 200
    assert response.json()["email"] == "test@test.com"


# ------------------------
# LOGOUT
# ------------------------

def test_logout_route_success(mocker):
    mocker.patch(
        "app.controllers.auth_controller.logout_user",
        return_value=None
    )

    response = client.post("/auth/logout")

    assert response.status_code == 200
