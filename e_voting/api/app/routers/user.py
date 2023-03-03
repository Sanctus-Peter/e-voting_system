import uuid

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, database, models, utils, oauth
from random import randint


router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def create_user(
        user: schemas.CreateVoter, db: Session = Depends(database.get_db)
):
    user_query = db.query(models.User).filter(models.User.nin == user.nin).first()
    if user_query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with nin {user.nin} already exists")

    hashed_pwd = utils.hashed(user.password)
    user.password = hashed_pwd
    new_user = models.User(**user.dict())
    new_user.ward = randint(1, 10)
    new_user.vin = uuid.uuid4().hex.upper()[:20]
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
