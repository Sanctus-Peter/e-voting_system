from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .. import schemas, database, models, utils, oauth
from random import randint


router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/register", status_code=status.HTTP_201_CREATED)
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
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User awaiting accreditation"}

@router.post("/login")
async def user_login(
        request: OAuth2PasswordBearer = Depends(), db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.admin_id == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Login credentials")
    if not utils.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Login Credentials")

    access_token = oauth.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}