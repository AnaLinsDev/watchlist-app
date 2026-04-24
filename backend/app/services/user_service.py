from sqlalchemy.orm import Session
from app.models import User
from app.core.errors import AppError, ErrorCode
from fastapi import Response

from app.core.security import hash_password, verify_password
from app.schemas.user_schema import UpdateUserRequest
from repositories.user_repository import get_user_by_email, get_user_by_username


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def update_user(user_id: int, db: Session, data: UpdateUserRequest):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise AppError(ErrorCode.USER_NOT_FOUND)

    if not verify_password(data.current_password, user.password):
        raise AppError(ErrorCode.INVALID_CURRENT_PASSWORD)

    # only update provided fields
    update_data = data.model_dump(exclude_unset=True)

    # remove fields that should not be directly applied
    update_data.pop("current_password", None)

    if "email" in update_data and update_data["email"] != user.email:
        if get_user_by_email(db, update_data["email"]):
            raise AppError(ErrorCode.EMAIL_ALREADY_EXISTS)

    if "username" in update_data and update_data["username"] != user.username:
        if get_user_by_username(db, update_data["username"]):
            raise AppError(ErrorCode.USERNAME_ALREADY_EXISTS)

    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user(user_id: int, db: Session, response: Response):

    user = db.get(User, user_id)

    if not user:
        raise AppError(ErrorCode.USER_NOT_FOUND)

    db.delete(user)
    db.commit()

    response.delete_cookie("access_token")
