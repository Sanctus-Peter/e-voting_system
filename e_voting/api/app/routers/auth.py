from fastapi import APIRouter, Response, HTTPException, status, Depends
from .. import models, schemas, utils, oauth
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags=["Authentications"], prefix="/authentication")


@router.post("/login", response_model=schemas.UserLogin)
async def user_login(res: Response, usr_credentials: OAuth2PasswordRequestForm = Depends(),
                     db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == usr_credentials.username).first()

    if not user or not utils.verify(usr_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid login credentials")

    access_tok = oauth.create_access_token(data={"user_id": user.id})
    res.set_cookie(key="token", value=access_tok)
    return {
        "name": user.name,
        "access_token": access_tok,
        "token_type": "bearer",
        "id": user.id
    }

@router.post("/official/login", response_model=schemas.UserLogin)
async def official_login(
        res: Response, request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.admin_id == request.username).first()

    if not user or not utils.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Login Credentials")

    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to perform this request")

    access_token = oauth.create_access_token(data={"user_id": user.id})
    res.set_cookie(key="token", value=access_token)
    return {
        # "name": user.name,
        "access_token": access_token,
        "token_type": "bearer"
        # "id": user.id
    }
