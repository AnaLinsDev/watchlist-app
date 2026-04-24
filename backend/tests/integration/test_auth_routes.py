from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.main import app
from app.routes.auth_routes import get_db

client = TestClient(app)


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

def test_register_route_success(mocker, fake_user):

    mocker.patch("app.routes.auth_routes.register_user",
                 return_value=fake_user
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

def test_login_route_success(mocker, fake_user):
    mocker.patch(
        "app.routes.auth_routes.login_user",
        return_value=fake_user
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

    response = client.post("/auth/logout")

    assert response.status_code == 200
