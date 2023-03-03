from fastapi import APIRouter, Depends, status, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, oauth, utils
from typing import List

candidate_router = APIRouter(tags=["Candidates"], prefix="/candidates")


@candidate_router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Candidate)
async def create_candidate(body: schemas.CandidateCreate, db: Session = Depends(get_db),
                           user: models.User = Depends(oauth.get_admin_user)):
    """Creates a candidate"""
    data = body.dict()
    new_candidate = models.Candidates(**data, created_by=user.id)
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)
    return new_candidate


@candidate_router.get("", response_model=List[schemas.Candidate])
async def get_all_candidates(db: Session = Depends(get_db)):
    """Retrive Candidates"""
    data = db.query(models.Candidates).all()
    return data


@candidate_router.get("/{candidateId}", response_model=schemas.Candidate)
async def get_candidate(candidateId: int, db: Session = Depends(get_db)):
    candidate = db.query(models.Candidates).where(
        models.Candidates.id == candidateId).first()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No candidate found with id: {candidateId}"
        )

    return candidate


@candidate_router.patch("/{candidateId}")
async def update_candidate(candidateId: int, body: schemas.CandidateUpdate,
                           db: Session = Depends(get_db), user: models.User = Depends(oauth.get_admin_user)):
    """Update candidate Details"""
    data = utils.filter_nones(body)
    candidate_qry = db.query(models.Candidates).where(
        models.Candidates.id == candidateId)
    old = candidate_qry.first()
    if not old:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No candidate found with id: {candidateId}"
        )
    candidate_qry.update(data)
    db.commit()
    db.refresh(old)

    return old


@candidate_router.delete("/{candidateId}", status_code=status.HTTP_204_NO_CONTENT)
async def update_candidate(candidateId: int, db: Session = Depends(get_db)):
    """Deletes a Candidate"""
    db.query(models.Candidates).where(
        models.Candidates.id == candidateId).delete()
    return None


@candidate_router.get("/{candidateId}/votes")
def get_candidate_votes(candidateId: int, db: Session = Depends(get_db)):
    """Get the Number of Votes For a particular Candidate"""
    candidate: models.Candidates = db.query(models.Candidates).where(
        models.Candidates.id == candidateId).first()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No candidate found with id: {candidateId}"
        )

    return {"election": candidate.election_id, "votes": candidate.votes}
