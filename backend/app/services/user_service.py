from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password
from sqlalchemy.exc import IntegrityError

from app.core.errors import AppError, ErrorCode


def create_user(db: Session, email: str, username: str, password: str):
    user = User(
    email=email,
    username=username,
    password=hash_password(password)
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise AppError(ErrorCode.USER_ALREADY_EXISTS)