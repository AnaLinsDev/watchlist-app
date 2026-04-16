from sqlalchemy.orm import Session
from fastapi import Response
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.errors import AppError, ErrorCode


def register_user(db: Session, email: str, username: str, password: str):
    
    print("RAW PASSWORD:", password)
    print("LENGTH:", len(password.encode("utf-8")))
    
    user = User(
        email=email,
        username=username,
        password=hash_password(password),
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise AppError(ErrorCode.USER_ALREADY_EXISTS)


def login_user(db: Session, response: Response, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        raise AppError(ErrorCode.INVALID_CREDENTIALS)

    token = create_access_token({"sub": str(user.id)})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24,
    )

    return user


def logout_user(response: Response):
    response.delete_cookie("access_token")