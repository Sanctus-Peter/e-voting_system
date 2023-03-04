from fastapi import APIRouter, status, Depends, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, oauth
from datetime import datetime
from typing import List


votes_router = APIRouter(tags=["Votes"], prefix="/votes")


@votes_router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Vote)
def vote(body: schemas.VoteCreate, db: Session = Depends(get_db),
         user: models.User = Depends(oauth.get_current_user)):
    """Cast A Vote"""
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

    # confirm candidate is participating in the election
    candidate_found = len(
        tuple(filter(lambda c: c.id == body.candidateId, election.candidates)))
    if not candidate_found:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candidate is not registered for this election"
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
    vote_cast = models.Vote(voterId=user.id, electionId=election.id,
                            candidateId=body.candidateId)
    db.add(vote_cast)
    db.commit()
    db.refresh(vote_cast)

    return vote_cast


@votes_router.get("/{electionId}", response_model=List[schemas.Vote])
def get_all_votes_for_election(electionId: int, db: Session = Depends(get_db)):
    """Retrieve All Votes for an Election"""
    votes = db.query(models.Vote).where(
        models.Vote.electionId == electionId).all()
    return votes
