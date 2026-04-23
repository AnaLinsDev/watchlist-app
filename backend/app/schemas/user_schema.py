from pydantic import BaseModel, EmailStr


class ProfileResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
