"""
This module defines the API endpoints related to authentication and officials in the election.

Routes:
- POST /register/{userID}: Creates a new official and returns the created instance.
- POST /accredit/{voterID}: Accredits a voter and returns a status message.
- POST /de_accredit/{voterID}: De-accredits a voter and returns a status message.

Dependencies:
- db: SQLAlchemy database session dependency.
- user: OAuth2 user authentication dependency.

Models:
- User: SQLAlchemy User model used for database operations.

Schemas:
- Official: Pydantic schema for Official model.

Functions:
- create_official(userID: str, db: Session, user: int) -> Official:
        Creates a new official and returns the created instance.
- accredit_voter(voterID: str, db: Session, user: int) -> Dict[str, str]:
        Accredits a voter and returns a status message.
- de_accredit_voter(voterID: str, db: Session, user: int) -> Dict[str, str]:
        De-accredits a voter and returns a status message.

Raises:
- HTTPException: Raises an HTTPException with a corresponding error message for various error scenarios.

"""

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from .. import schemas, database, models, utils, oauth


router = APIRouter(tags=["Officials"], prefix="/officials")


@router.post("/register/{userID}", status_code=status.HTTP_201_CREATED,
             response_model=schemas.Official)
async def create_official(
        userID: str, db: Session = Depends(database.get_db), user: int = Depends(oauth.get_admin_user)
):
    """
    Creates a new official and returns the created instance.
    Args:
        userID (str): The ID of the user to be created as an official.
        db (Session): The SQLAlchemy database session dependency.
        user (int): The OAuth2 user authentication dependency.

    Returns:
        schemas.Official: The Pydantic schema for the created Official instance.

    Raises:
        HTTPException: If the provided user ID is not valid or if the user is already accredited.
    """
    found_user = utils.get_user_with_id(userID)

    if not found_user.accredited:
        found_user.update({"accredited": True}, synchronize_session=False)
    found_user.update({"role": "admin", "admin_id": f"{uuid.uuid4().hex[:8]}"}, synchronize_session=False)
    db.commit()
    return found_user.first()


@router.post("/accredit/{voterID}", status_code=status.HTTP_201_CREATED)
async def accredit_voter(
        voterID: str, db: Session = Depends(database.get_db), user: int = Depends(oauth.get_admin_user)
):
    """
    Accredits a voter and returns a status message.
    Args:
        voterID (str): The ID of the voter to be accredited.
        db (Session): The SQLAlchemy database session dependency.
        user (int): The OAuth2 user authentication dependency.

    Returns:
        Dict[str, str]: A dictionary containing the status message.

    Raises:
        HTTPException: If the provided voter ID is not valid or if the voter is already accredited.
    """
    found_user = utils.get_user_with_id(voterID)

    if not found_user.accredited:
        found_user.update({"accredited": True}, synchronize_session=False)
        db.commit()
        return {"status": "successfully accredited"}


@router.post("/de_accredit/{voterID}", status_code=status.HTTP_201_CREATED)
async def de_accredit_voter(
        voterID: str, db: Session = Depends(database.get_db), user: int = Depends(oauth.get_admin_user)
):
    """
    This function de-accredits a voter by updating the accredited column of their user profile to False.

    Args:
        voterID (str): The ID of the voter to be de-accredited.
        db (Session, optional): The database session. Defaults to Depends(database.get_db).
        user (int, optional): The admin user who is performing the de-accreditation. Defaults to Depends(oauth.get_admin_user).

    Returns:
        dict: A dictionary containing a status message indicating that the voter was successfully de-accredited.

    Raises:
        HTTPException: Raised if the specified voter ID is invalid or if the user is not an admin.
    """
    found_user = utils.get_user_with_id(voterID)

    if found_user.accredited:
        found_user.update({"accredited": False}, synchronize_session=False)
        db.commit()

