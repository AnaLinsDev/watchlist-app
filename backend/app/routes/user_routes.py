from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.controllers.user_controller import (
    delete_user_controller
)
from app.schemas.user_schema import ProfileResponse
from app.dependencies.auth import get_current_user_controller

router = APIRouter(prefix="/user")


# Get Profile
@router.get("/profile", response_model=ProfileResponse)
def get_profile(current_user=Depends(get_current_user_controller)):
    return current_user


# Delete User
@router.delete("/delete")
def delete_profile(
    response: Response,
    current_user=Depends(get_current_user_controller),
    db: Session = Depends(get_db)
):
    return delete_user_controller(response, current_user, db)