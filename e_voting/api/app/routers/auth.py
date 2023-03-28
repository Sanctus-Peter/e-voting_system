"""
This module defines endpoints for user authentication and authorization. It provides two API routes:
- /authentication/login: Logs a user into the system and returns an access token.
- /authentication/official/login: Logs an admin user into the system and returns an access token.

Both routes use OAuth2 for authentication, and rely on SQLAlchemy to interact with the database. The endpoints
return JSON responses with information about the user and their access token.

Note that this module requires a valid database connection to function properly. The `get_db` function from the
`database` module is used to create a SQLAlchemy session, which is passed as a dependency to the API routes.

For more information on how to use the endpoints, refer to the documentation for each function.
"""


from fastapi import APIRouter, Response, HTTPException, status, Depends
from .. import models, schemas, utils, oauth
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags=["Authentications"], prefix="/authentication")


@router.post("/login", response_model=schemas.UserLogin)
async def user_login(
        res: Response, usr_credentials: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    """
       Logs a user into the system and returns an access token.

       Args:
           res (Response): A FastAPI Response object.
           usr_credentials (OAuth2PasswordRequestForm): A form containing the user's email and password.
           db (Session): A SQLAlchemy session object.

       Returns:
           dict: A dictionary containing the user's name, access token, token type, and ID.

       Raises:
           HTTPException: If the user's credentials are invalid or if the user does not exist.
    """
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
    """
    Logs an admin user into the system and returns an access token.

    Args:
        res (Response): A FastAPI Response object.
        request (OAuth2PasswordRequestForm): A form containing the admin user's username and password.
        db (Session): A SQLAlchemy session object.

    Returns:
        dict: A dictionary containing the access token and token type.

    Raises:
        HTTPException: If the admin user's credentials are invalid or if the user is not authorized to perform the request.
    """
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
