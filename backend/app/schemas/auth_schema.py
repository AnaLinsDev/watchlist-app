from pydantic import BaseModel, EmailStr, StringConstraints, Field
from typing import Annotated


Username = Annotated[
    str,
    StringConstraints(
        pattern=r"^[a-zA-Z0-9]+$",
        min_length=4,
        max_length=50
    )
]


class RegisterRequest(BaseModel):
    email: EmailStr
    username: Username
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class AuthResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
