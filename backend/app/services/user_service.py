from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import Response

from app.models import User
from app.core.errors import AppError, ErrorCode
from app.core.security import hash_password, verify_password
from app.schemas.user_schema import UpdateUserRequest


def update_user(current_user: User, db: Session, data: UpdateUserRequest):
    user = db.get(User, current_user.id)

    if not user:
        raise AppError(ErrorCode.USER_NOT_FOUND)

    if not verify_password(data.current_password, user.password):
        raise AppError(ErrorCode.INVALID_CURRENT_PASSWORD)

    # only update provided fields
    update_data = data.model_dump(exclude_unset=True)

    update_data.pop("current_password", None)

    allowed_fields = {"email", "username", "password"}

    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    for field, value in update_data.items():
        if field in allowed_fields:
            setattr(user, field, value)

    try:
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


def delete_user(current_user: User, db: Session):

    user = db.get(User, current_user.id)

    if not user:
        raise AppError(ErrorCode.USER_NOT_FOUND)

    db.delete(user)
    db.commit()

