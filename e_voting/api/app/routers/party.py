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
    party_query = db.query(models.Party).filter(models.Party.id == partyID).first()
    if not party_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Party with id {partyID} does not exist")
    return party_query


@router.delete('/{partyID}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_party(
        partyID: int, db: Session = Depends(database.get_db), admin: int = Depends(oauth.get_admin_user)
):
    db.query(models.Party).where(models.Party.id == partyID).delete()
    db.commit()
    return


@router.get('/', response_model=List[schemas.PartyView])
async def get_all_parties(db: Session = Depends(database.get_db)):
    parties = db.query(models.Party).all()
    return parties
