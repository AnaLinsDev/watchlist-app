# app/dependencies/auth.py

from fastapi import Depends, Cookie, HTTPException, Response
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import os

from app.database import get_db
from app.services.user_service import delete_user_service

def delete_user_controller(
    response: Response,
    current_user,
    db: Session
):
    delete_user_service(current_user.id, db, response)

    return {"message": "User deleted successfully"}