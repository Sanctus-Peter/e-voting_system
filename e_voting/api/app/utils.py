from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from e_voting.api.app import database, models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def filter_nones(body):
    """Filter out keys with values as None
    body - a pydantic schema
    """
    result = {}
    for key in body:
        if body[key] is not None:
            result[key] = body[key]

    return result


def hashed(password: str):
    return pwd_context.hash(password)


def verify(attempted_password, usr_password):
    return pwd_context.verify(attempted_password, usr_password)


# print(hashed("12345pass"))
def get_user_with_id(user_id, db: Session = Depends(database.get_db)):
    found_user = db.query(models.User).filter(models.User.id == user_id)
    is_found = found_user.first()
    if not is_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return is_found
