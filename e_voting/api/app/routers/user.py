"""
This module defines the API routes for managing the users in the system.

Dependencies:
    - uuid
    - typing.List
    - fastapi.APIRouter
    - fastapi.status
    - fastapi.Depends
    - fastapi.HTTPException
    - fastapi.security.OAuth2PasswordRequestForm
    - sqlalchemy.orm.Session
    - ..schemas
    - ..database
    - ..models
    - ..utils
    - ..oauth
    - random.randint

Models:
    - User

Schemas:
    - User
    - UserCreate
    - UpdateVoters
    - CreateVoter
    - UserProfile

Functions:
    - get_all_users(db: Session, admin_user: int) -> List[schemas.User]
    - create_user(user: schemas.CreateVoter, db: Session) -> schemas.UserCreate
    - get_user_profile(user_ID: int, form_data: OAuth2PasswordRequestForm) -> schemas.UserProfile
    - update_user(userID: int, user: schemas.UpdateVoters, db: Session, found_user: models.User) -> schemas.User
    - delete_user(userID: int, db: Session, user: models.User)
    - get_user(user_ID: int, form_data: OAuth2PasswordRequestForm) -> schemas.User

Routes:
    - /users/ -> GET
        Retrieve all users.

    - /users/register -> POST
        Register a new user.

    - /users/profile/{user_ID} -> GET
        Retrieve a user's profile.

    - /users/{userID}/update -> PUT
        Update a user's information.

    - /users/{userID} -> DELETE
        Delete a user.

    - /users/{userID} -> GET
        Retrieve a user's information.
"""

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
    """
        Retrieve all users.

        Args:
            db (Session): The database session.
            admin_user (int): The ID of the admin user who is making the request.

        Returns:
            List[schemas.User]: A list of all users in the database.

        Raises:
            HTTPException: If the authenticated user is not an admin user.
    """
    users = db.query(models.User).all()
    return users


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreate)
async def create_user(
        user: schemas.CreateVoter, db: Session = Depends(database.get_db)
):
    """
        Register a new user.

    Args:
        user (schemas.CreateVoter): The user information to create.
        db (Session): The database session.

    Returns:
        schemas.UserCreate: The created user.

    Raises:
        HTTPException: If a user with the same national identification number (NIN) already exists in the database.

    """
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
    """
        Retrieve a user's profile.

    Args:
        user_ID (int): The ID of the user to retrieve the profile for.
        form_data (OAuth2PasswordRequestForm): The OAuth2 form data for authentication.

    Returns:
        schemas.UserProfile: The user's profile.

    Raises:
        HTTPException: If the user making the request is not authenticated or authorized to retrieve the profile.

    """
    user = utils.get_user_with_id(user_ID)
    return user


@router.put("/{userID}/update", response_model=schemas.User)
async def update_user(
        userID: int, user: schemas.UpdateVoters, db: Session = Depends(database.get_db),
        found_user: models.User = Depends(oauth.get_current_user)
):
    """
        Update a user's information.

    Args:
        userID (int): The ID of the user to update.
        user (schemas.UpdateVoters): The updated user information.
        db (Session): The database session.
        found_user (models.User): The authenticated user making the request.

    Returns:
        schemas.User: The updated user information.

    Raises:
        HTTPException: If the authenticated user is not authorized to update the user information
                    or the user with the specified ID does not exist.

    """
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
    """
        Delete a user.

    Args:
        userID (int): The ID of the user to delete.
        db (Session): The database session.
        user (models.User): The authenticated admin user making the request.

    Raises:
        HTTPException: If the authenticated user is not authorized to delete the user
                    or the user with the specified ID does not exist.

    """
    db.query(models.User).where(models.User.id == userID).delete()
    db.commit()
    return


@router.get("/{userID}", status_code=status.HTTP_200_OK, response_model=schemas.User)
async def get_user(
        user_ID: int, form_data: OAuth2PasswordRequestForm = Depends(oauth.get_current_user)
):
    """
        Retrieve a user's information.

    Args:
        user_ID (int): The ID of the user to retrieve the information for.
        form_data (OAuth2PasswordRequestForm): The OAuth2 form data for authentication.

    Returns:
        schemas.User: The user's information.

    Raises:
        HTTPException: If the user making the request is not authenticated or authorized to retrieve the user information.

    """
    user = utils.get_user_with_id(user_ID)
    return user
