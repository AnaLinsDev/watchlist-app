from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext

from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXPIRES_IN = os.getenv("JWT_EXPIRES_IN", "1d")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire_delta = parse_expires_in(JWT_EXPIRES_IN)
    expire = datetime.now(timezone.utc) + expire_delta

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)


def parse_expires_in(value: str) -> timedelta:
    unit = value[-1]
    amount = int(value[:-1])

    if unit == "d":
        return timedelta(days=amount)
    elif unit == "h":
        return timedelta(hours=amount)
    elif unit == "m":
        return timedelta(minutes=amount)
    else:
        raise ValueError("Invalid JWT_EXPIRES_IN format")
