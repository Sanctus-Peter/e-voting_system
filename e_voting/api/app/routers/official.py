from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
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
