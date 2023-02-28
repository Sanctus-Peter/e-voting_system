from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
import uuid

from .. import schemas, database, models, utils, oauth

router = APIRouter(tags=["Officials"], prefix="/officials")


@router.post("/register/{user_id}", status_code=status.HTTP_201_CREATED,
             response_model=schemas.Official)
async def create_official(
        user_id: str, db: Session = Depends(database.get_db), user: int = Depends(oauth.get_current_user)
):
    found_user = db.query(models.User).filter(models.User.id == user_id)
    is_found = found_user.first()
    is_admin = user.role == "admin"
    if not is_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to perform this request")

    found_user.update({"role": "admin", "admin_id": f"{uuid.uuid4().hex[:8]}"}, synchronized_session=False)
    db.commit()
    return found_user.first()
    pass

@router.post("/login")
async def login_official(
        request: OAuth2PasswordBearer = Depends(), db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.admin_id == request.username).first()
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to perform this request")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Login credentials")
    if not utils.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Login Credentials")

    access_token = oauth.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
