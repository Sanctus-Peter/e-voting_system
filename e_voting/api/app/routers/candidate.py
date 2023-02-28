from fastapi import APIRouter, Depends, status
from app.database import get_db
from sqlalchemy.orm import Session
from app import models, schemas, oauth

candidate_router = APIRouter(tags=["Candidates"], prefix="/candidates")


@candidate_router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Candidate)
async def create_candidate(body: schemas.CandidateCreate, db: Session = Depends(get_db),
                           user: models.User = Depends(oauth.get_admin_user)):
    """Creates a candidate"""

    return "Candidate created"


@candidate_router.get("")
async def get_all_candidates(db: Session = Depends(get_db)):
    """Retrive Candidates"""
    return "All Candidates"


@candidate_router.get("/{candidateId}", response_model=schemas.Candidate)
async def get_candidate(candidateId: int, db: Session = Depends(get_db)):
    """Fetch one Candidate"""
    return "One Candidate"


@candidate_router.patch("/{candidateId}")
async def update_candidate(candidateId: int, db: Session = Depends(get_db),
                           user: models.User = Depends(oauth.get_admin_user)):
    """Update candidate Details"""
    return "Update Candidate"


@candidate_router.delete("/{candidateId}", status_code=status.HTTP_204_NO_CONTENT)
async def update_candidate(candidateId: int, db: Session = Depends(get_db)):
    """Deletes a Candidate"""
    return None


@candidate_router.get("/{candidateId}/votes")
def get_candidate_votes(candidateId: int, db: Session = Depends(get_db)):
    """Get the Number of Votes For a particular Candidate"""

    return "number of Votes"
