from typing import List

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
    found_user = utils.get_user_with_id(voterID)

    if not found_user.accredited:
        found_user.update({"accredited": True}, synchronize_session=False)
        db.commit()
        return {"status": "successfully accredited"}


@router.post("/de_accredit/{voterID}", status_code=status.HTTP_201_CREATED)
async def de_accredit_voter(
        voterID: str, db: Session = Depends(database.get_db), user: int = Depends(oauth.get_admin_user)
):
    found_user = utils.get_user_with_id(voterID)

    if found_user.accredited:
        found_user.update({"accredited": False}, synchronize_session=False)
        db.commit()

