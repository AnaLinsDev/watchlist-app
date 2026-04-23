from sqlalchemy.orm import Session
from app.models import User
from app.core.errors import AppError, ErrorCode
from fastapi import Response

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def delete_user_service(user_id: int, db: Session, response: Response):

    user = db.get(User, user_id)

    if not user:
        raise AppError(ErrorCode.USER_NOT_FOUND)
    
    db.delete(user)
    db.commit()

    response.delete_cookie("access_token")