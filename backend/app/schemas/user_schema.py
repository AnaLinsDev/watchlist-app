from pydantic import BaseModel, EmailStr, StringConstraints, Field
from typing import Optional, Annotated


Username = Annotated[
    str,
    StringConstraints(
        pattern=r"^[a-zA-Z0-9]+$",
        min_length=4,
        max_length=50
    )
]


class UpdateUserRequest(BaseModel):
    id: int
    email: Optional[EmailStr] = None
    username: Optional[Username] = None
    password: Optional[str] = Field(default=None, min_length=6, max_length=128)
    current_password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
