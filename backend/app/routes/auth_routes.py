from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth_schema import RegisterRequest, LoginRequest, AuthResponse
from app.controllers.auth_controller import (
    register_controller,
    login_controller,
    logout_controller,
)

router = APIRouter(prefix="/auth")


# Auth Register
@router.post("/register", response_model=AuthResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return register_controller(db, data)


# Auth Login
@router.post("/login", response_model=AuthResponse)
def login(
    data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    return login_controller(db, response, data)


# Auth Logout
@router.post("/logout")
def logout(response: Response):
    return logout_controller(response)
