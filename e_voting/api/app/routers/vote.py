from fastapi import APIRouter
from fastapi import APIRouter, status, Depends, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app import models, schemas, utils


votes_router = APIRouter(tags=["Votes"], prefix="/votes")


@votes_router.post("")
def vote(body: schemas.VoteCreate, db: Session = Depends(get_db)):
    election = db.query(models.Election).where(
        models.Election.id == body.electionId).first()
    if not election:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Election with Id= {body.electionId}"
        )

    # confirm election is still active

    # confirm voter is eligible to vote in this election

    # confirm has not already voted

    # cast vote

    return "Voted Successfully"


router = APIRouter(tags=["Votes"])
