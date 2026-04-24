from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user_schema import UpdateUserRequest, UserResponse
from app.dependencies.auth import get_current_user
from app.services.user_service import update_user, delete_user

router = APIRouter(prefix="/user")


# Get Profile
@router.get("/profile", response_model=UserResponse)
def get_profile(current_user=Depends(get_current_user)):
    return current_user


# Update User
@router.put("/edit", response_model=UserResponse)
def update(
    data: UpdateUserRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_user(current_user, db, data)


# Delete User
@router.delete("/delete")
def delete(
    response: Response,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    delete_user(current_user, db)

    response.delete_cookie("access_token")

    return {"message": "User deleted successfully"}
