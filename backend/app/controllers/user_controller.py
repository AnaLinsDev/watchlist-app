# app/dependencies/auth.py

from fastapi import Depends, Cookie, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import os

from app.database import get_db
from app.services.user_service import get_user_by_id

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


def get_current_user(
    access_token: str = Cookie(None),
    db: Session = Depends(get_db)
):

    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(access_token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
