from fastapi import APIRouter, Response, HTTPException, status, Depends
from app import models, schemas, utils, oauth
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

auth_router = APIRouter(tags=["Authentications"], prefix="/auth")


@auth_router.post("/login", response_model=schemas.Token)
async def login(res: Response, login_details: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user: models.User = db.query(models.User).filter(
        models.User.email == login_details.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    if not utils.verify(login_details.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Credentials")

    # create token
    token = oauth.create_access_token(data={"user_id": user.id})
    res.set_cookie(key="token", value=token)
    return {"token": token, "type": "bearer"}
