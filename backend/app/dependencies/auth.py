from fastapi import Depends, Cookie
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import os

from app.core.errors import AppError, ErrorCode
from app.database import get_db
from app.services.user_service import get_user_by_id

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


def get_current_user(
    access_token: str = Cookie(None),
    db: Session = Depends(get_db)
):

    if not access_token:
        raise AppError(ErrorCode.NOT_AUTHENTICATED)

    try:
        payload = jwt.decode(access_token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except JWTError:
        raise AppError(ErrorCode.INVALID_TOKEN)

    user = get_user_by_id(db, user_id)

    if not user:
        raise AppError(ErrorCode.USER_NOT_FOUND)

    return user
