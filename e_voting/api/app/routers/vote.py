from fastapi import APIRouter
from fastapi import APIRouter, status, Depends, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app import models, schemas, utils, oauth
from datetime import datetime


votes_router = APIRouter(tags=["Votes"], prefix="/votes")


@votes_router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Vote)
def vote(body: schemas.VoteCreate, db: Session = Depends(get_db),
         user: models.User = Depends(oauth.get_current_user)):
    election: models.Election = db.query(models.Election).where(
        models.Election.id == body.electionId).first()
    if not election:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Election with Id= {body.electionId}"
        )

    # confirm election is still active
    if election.end_date <= datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Election is Closed!"
        )

    # confirm voter is eligible to vote in this election
    if not election.user_eligible(user=user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not eligible to vote in this election"
        )

    # confirm has not already voted
    has_voted = db.query(models.Vote).where(
        models.Vote.electionId == election.id, models.Vote.voterId == user.id
    ).first()
    if has_voted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="multiple voting is not allowed"
        )

    # cast vote
    vote = models.Vote(voterId=user.id, electionId=election.id)
    db.add(vote)
    db.commit()
    db.refresh(vote)

    return vote
