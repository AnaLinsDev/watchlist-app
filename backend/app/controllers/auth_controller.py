from sqlalchemy.orm import Session
from fastapi import Response

from app.schemas.auth_schema import RegisterRequest, LoginRequest
from app.services.auth_service import register_user, login_user, logout_user


def register_controller(db: Session, data: RegisterRequest):
    return register_user(
        db,
        email=data.email,
        username=data.username,
        password=data.password,
    )


def login_controller(db: Session, response: Response, data: LoginRequest):
    return login_user(
        db,
        response,
        email=data.email,
        password=data.password,
    )


def logout_controller(response: Response):
    logout_user(response)
    return {"message": "Logged out successfully"}