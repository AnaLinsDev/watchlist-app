from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.auth_schema import RegisterRequest, LoginRequest, AuthResponse
from app.controllers.auth_controller import (
    register_controller,
    login_controller,
    logout_controller,
)

router = APIRouter(prefix="/auth")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=AuthResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return register_controller(db, data)


@router.post("/login", response_model=AuthResponse)
def login(
    data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    return login_controller(db, response, data)


@router.post("/logout")
def logout(response: Response):
    return logout_controller(response)
