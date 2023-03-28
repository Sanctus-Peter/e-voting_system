"""
This module provides utility functions for authentication and authorization of users.

Functions:

    create_access_token: creates an access token using a dictionary of data provided.
    verify_tok: verifies a given token and returns the token data if it is valid.
    get_current_user: gets the current user based on the provided token and database.
    get_admin_user: gets the current user and raises an HTTPException if they are not an admin.

Dependencies:

    JWTError: Exception class for errors in JSON Web Tokens.
    jwt: module for encoding and decoding JSON Web Tokens.
    datetime: module for working with dates and times.
    timedelta: class for representing time differences.
    schemas: module containing Pydantic models for the API's data structures.
    database: module providing database functionality for the API.
    models: module containing SQLAlchemy models for the API's database tables.
    Depends: class from FastAPI for injecting dependencies into endpoints.
    status: module containing HTTP status codes.
    HTTPException: class from FastAPI for raising HTTP exceptions.
    OAuth2PasswordBearer: class from FastAPI for handling OAuth2 password authentication.

Constants:

    oauth2_scheme: an instance of OAuth2PasswordBearer for use with token-based authentication.
    SECRET_KEY: the secret key used for encoding and decoding JSON Web Tokens.
    ALGORITHM: the encryption algorithm used for encoding and decoding JSON Web Tokens.
    ACCESS_TOKEN_EXPIRE_MINUTES: the number of minutes until an access token expires.

Configurations:

    settings: an instance of the Settings class containing environment variables used in the module.
"""
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_tok_expire_minutes


def create_access_token(data: dict):
    """
        Create an access token with the provided data.

        Args:
            data (dict): A dictionary containing the data to be included in the token.

        Returns:
            str: The encoded access token.
    """
    encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp": expire})

    encoded = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded


def verify_tok(token: str, credentials_exception):
    """
        Verify the given token and return its data.

        Args:
            token (str): The token to verify.
            credentials_exception (fastapi.HTTPException): The exception to raise if the token is not valid.

        Returns:
            schemas.TokData: The data contained in the token.

        Raises:
            fastapi.HTTPException: If the token is not valid.

    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        _id = payload.get("user_id")

        if not _id:
            raise credentials_exception
        tok_data = schemas.TokData(id=_id)
    except JWTError:
        raise credentials_exception
    return tok_data


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(database.get_db)):
    """
       Get the current user based on the provided token and database session.

       Args:
           token (str, optional): The access token to use for authentication. Defaults to Depends(oauth2_scheme).
           db (sqlalchemy.orm.Session, optional): The database session to use for queries.
                    Defaults to Depends(database.get_db).

       Returns:
           models.User: The current user.

       Raises:
           fastapi.HTTPException: If the token is not valid or the user does not exist.

    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token = verify_tok(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user


def get_admin_user(user: models.User = Depends(get_current_user)):
    """
        Get the current user as an admin user.

        Args:
            user (models.User): The current user.

        Raises:
            HTTPException: If the current user is not an admin user.

        Returns:
            models.User: The current user as an admin user.
    """
    if user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to execute this action"
        )
    return user
