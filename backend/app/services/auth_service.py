from sqlalchemy.orm import Session
from fastapi import Response
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.errors import AppError, ErrorCode

from dotenv import load_dotenv
import os

from app.schemas.auth_schema import LoginRequest, RegisterRequest

load_dotenv()

ENV = os.getenv("ENV")


def register_user(db: Session, data: RegisterRequest):

    user = User(
        email=data.email,
        username=data.username,
        password=hash_password(data.password),
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        db.rollback()

        error_str = str(e.orig).lower()

        if "email" in error_str:
            raise AppError(ErrorCode.EMAIL_ALREADY_EXISTS)

        if "username" in error_str:
            raise AppError(ErrorCode.USERNAME_ALREADY_EXISTS)

        raise AppError(ErrorCode.USER_ALREADY_EXISTS)


def login_user(db: Session, response: Response, data: LoginRequest):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise AppError(ErrorCode.INVALID_CREDENTIALS)

    token = create_access_token({"sub": str(user.id)})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=ENV == "prod",
        samesite="lax",
        max_age=60 * 60 * 24,  # 1 day
    )

    return user
