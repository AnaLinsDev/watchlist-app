from fastapi import APIRouter, Depends

from app.controllers.user_controller import (
    get_current_user,
)
from app.schemas.user_schema import ProfileResponse

router = APIRouter(prefix="/user")


# Get Profile
@router.get("/profile", response_model=ProfileResponse)
def get_profile(current_user=Depends(get_current_user)):
    return current_user
