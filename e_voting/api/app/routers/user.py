import uuid
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, database, models, utils, oauth
from random import randint


router = APIRouter(tags=["Users"], prefix="/users")


@router.get("/", response_model=List[schemas.User])
async def get_all_users(
        db: Session = Depends(database.get_db), admin_user: int = Depends(oauth.get_admin_user)
):
    users = db.query(models.User).all()
    return users


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreate)
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


@router.get("/profile/{user_ID}", status_code=status.HTTP_200_OK, response_model=schemas.UserProfile)
async def get_user_profile(
        user_ID: int, form_data: OAuth2PasswordRequestForm = Depends(oauth.get_current_user)
):
    user = utils.get_user_with_id(user_ID)
    return user


@router.put("/{userID}/update", response_model=schemas.User)
async def update_user(
        userID: int, user: schemas.UpdateVoters, db: Session = Depends(database.get_db),
        found_user: models.User = Depends(oauth.get_current_user)
):
    if found_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {userID} not found")
    found_user.update(user)
    db.commit()
    db.refresh(found_user)
    return found_user


@router.delete("/{userID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        userID: int, db: Session = Depends(database.get_db), user: models.User = Depends(oauth.get_admin_user)
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {userID} not found")
    db.delete(user)
    db.commit()
    return


@router.get("/{userID}", status_code=status.HTTP_200_OK, response_model=schemas.User)
async def get_user(
        user_ID: int, form_data: OAuth2PasswordRequestForm = Depends(oauth.get_current_user)
):
    user = utils.get_user_with_id(user_ID)
    return user
