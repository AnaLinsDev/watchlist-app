# app/dependencies/auth.py

from fastapi import Response
from sqlalchemy.orm import Session

from app.services.user_service import delete_user, update_user
from app.schemas.user_schema import UpdateUserRequest


def update_user_controller(
        db: Session,
        data: UpdateUserRequest,
        current_user):

    return update_user(current_user.id, db, data)


def delete_user_controller(
    response: Response,
    current_user,
    db: Session
):
    delete_user(current_user.id, db, response)

    return {"message": "User deleted successfully"}
