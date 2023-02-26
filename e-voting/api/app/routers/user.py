from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, database, models
router = APIRouter(tags=["Users"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.CreateVoter,
                      db: Session = Depends(database.get_db)):
    user_query = db.query(models.User).filter(models.User.nin == user.nin).first()
    if user_query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with nin {user.nin} already exists")
    return {"message": "User created successfully"}

