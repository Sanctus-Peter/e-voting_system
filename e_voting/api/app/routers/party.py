"""
This module defines the API routes for the party related operations, including registering and updating parties.

Routes:
    - `POST /party/register`: Create a new party with a logo.
    - `PUT /party/{partyID}/update`: Update an existing party.
    - `GET /party/{partyID}`: Get a single party by ID.
    - `DELETE /party/{partyID}`: Delete a single party by ID.
    - `GET /party/`: Get all parties.

Dependencies:
    - `fastapi.APIRouter`: Defines the API router and allows for route creation.
    - `fastapi.Depends`: Allows for easy dependency injection.
    - `fastapi.HTTPException`: Exception that will return an HTTP error response.
    - `fastapi.File`: Helper function to receive a file in a route.
    - `fastapi.UploadFile`: File uploaded via an HTTP request.
    - `sqlalchemy.orm.Session`: A SQLAlchemy database session.
    - `cloudinary.uploader.upload`: Upload files to a cloud storage service.
    - `cloudinary.utils.cloudinary_url`: Helper function to get a URL for a cloudinary file.

Models:
    - `models.Party`: A SQLAlchemy model representing a party.

Schemas:
    - `schemas.Party`: A Pydantic schema representing a party.
    - `schemas.PartyView`: A Pydantic schema representing a party for viewing.

Functions:
    - `create_party`: Route function that creates a new party with a logo.
    - `update_party`: Route function that updates an existing party.
    - `get_party`: Route function that gets a single party by ID.
    - `delete_party`: Route function that deletes a single party by ID.
    - `get_all_parties`: Route function that gets all parties.

Args:
    - `party`: A Pydantic schema representing a party.
    - `partyID`: An integer representing the ID of a party.
    - `db`: A SQLAlchemy database session.
    - `admin`: An integer representing the ID of an admin user.
    - `party_logo`: A file uploaded via an HTTP request.

Returns:
    - `Party`: A SQLAlchemy model representing a party.
    - `PartyView`: A Pydantic schema representing a party for viewing.
    - `List[PartyView]`: A list of Pydantic schemas representing parties for viewing.

Raises:
    - `HTTPException`: Exception that will return an HTTP error response.
"""


from typing import Optional, List
from fastapi import APIRouter, status, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from .. import schemas, database, models, utils, oauth
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url


router = APIRouter(tags=["party"], prefix="/party")


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.Party)
async def create_party(
        party: schemas.CreateParty,
        db: Session = Depends(database.get_db),
        admin: int = Depends(oauth.get_admin_user),
        party_logo: UploadFile = File(...)
):
    """
       Create a new political party with a name and an optional logo.

       Args:
           party (schemas.CreateParty): The data needed to create a new political party.
           db (Session, optional): The database session. Defaults to Depends(database.get_db).
           admin (int, optional): The user ID of an admin user. Defaults to Depends(oauth.get_admin_user).
           party_logo (UploadFile, optional): The image file of the party's logo. Defaults to File(...).

       Returns:
           models.Party: The newly created political party.

       Raises:
           HTTPException: If a party with the same name already exists or if the logo file is invalid.
    """

    # delete the file from memory and rollover to disk to save unnecessary memory space
    party_logo.file.rollover()
    party_logo.file.flush()

    valid_types = [
        'image/png',
        'image/jpeg',
        'image/bmp',
    ]
    await utils.validate_file(party_logo, 2000000, valid_types)
    party_query = db.query(models.Party).filter(models.Party.name == party.name).first()
    if party_query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Party with name {party.name} already exists")

    pics = upload(party_logo.file)
    url = pics.get("url")
    new_party = models.Party(**party.dict())
    new_party.party_logo_url = url
    db.add(new_party)
    db.commit()
    db.refresh(new_party)
    return new_party


@router.put('/{partyID}/update', response_model=schemas.Party)
async def update_party(
        partyID: int,
        party: schemas.UpdateParty,
        db: Session = Depends(database.get_db),
        admin: int = Depends(oauth.get_admin_user),
        file: Optional[UploadFile] = File(...)
):
    """
        Update an existing political party by ID with a new name and/or logo.

        Args:
            partyID (int): The ID of the political party to be updated.
            party (schemas.UpdateParty): The new data for the political party.
            db (Session, optional): The database session. Defaults to Depends(database.get_db).
            admin (int, optional): The user ID of an admin user. Defaults to Depends(oauth.get_admin_user).
            file (Optional[UploadFile], optional): The new image file of the party's logo. Defaults to File(...).

        Returns:
            models.Party: The updated political party.

        Raises:
            HTTPException: If the party does not exist, or if the logo file is invalid.
    """

    # delete the file from memory and rollover to disk to save unnecessary memory space
    if file:
        file.file.rollover()
        file.file.flush()
        valid_types = [
            'image/png',
            'image/jpeg',
            'image/bmp',
        ]
        await utils.validate_file(file, 2000000, valid_types)

    party_query = db.query(models.Party).filter(models.Party.id == partyID).first()
    if not party_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Party with id {partyID} does not exist")
    party_query.update(party)

    if file:
        pics = upload(file.file, public_id=file.filename)
        url = pics.get("url")
        party_query.party_logo_url = url

    db.commit()
    db.refresh(party_query)
    return party_query


@router.get('/{partyID}', response_model=schemas.PartyView)
async def get_party(partyID: int, db: Session = Depends(database.get_db)):
    """
        Retrieve the details of a political party by ID.

        Args:
            partyID (int): The ID of the political party to be retrieved.
            db (Session, optional): The database session. Defaults to Depends(database.get_db).

        Returns:
            schemas.PartyView: The details of the political party.

        Raises:
            HTTPException: If the party does not exist.
    """
    party_query = db.query(models.Party).filter(models.Party.id == partyID).first()
    if not party_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Party with id {partyID} does not exist")
    return party_query


@router.delete('/{partyID}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_party(
        partyID: int, db: Session = Depends(database.get_db), admin: int = Depends(oauth.get_admin_user)
):
    """
       Delete a political party by ID.

       Args:
           partyID (int): The ID of the political party to be deleted.
           db (Session, optional): The database session. Defaults to Depends(database.get_db).
           admin (int, optional): The user ID of an admin user. Defaults to Depends(oauth.get_admin_user).

       Returns:
           None

       Raises:
           HTTPException: If the party does not exist.
    """
    db.query(models.Party).where(models.Party.id == partyID).delete()
    db.commit()
    return


@router.get('/', response_model=List[schemas.PartyView])
async def get_all_parties(db: Session = Depends(database.get_db)):
    """
        Retrieves all parties from the database.

        Args:
            db (Session, optional): The database session to be used. Defaults to Depends(database.get_db).

        Returns:
            List[schemas.PartyView]: A list of dictionaries containing details of all the parties in the database.

        Raises:
            HTTPException: If there are no parties in the database.
    """
    parties = db.query(models.Party).all()
    return parties
