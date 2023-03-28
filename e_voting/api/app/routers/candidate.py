"""
This module defines the API routes for managing candidates in an election.

The routes provided by this module allow creating, retrieving, updating, and deleting
candidates in an election. The module also provides a route for retrieving the number of
votes a candidate has received in an election.

Routes:
    - POST /candidates: create a new candidate in the database
    - GET /candidates: retrieve all candidates from the database
    - GET /candidates/{candidateId}: retrieve a candidate with the specified ID
    - PATCH /candidates/{candidateId}: update a candidate with the specified ID
    - DELETE /candidates/{candidateId}: delete a candidate with the specified ID
    - GET /candidates/{candidateId}/votes: retrieve the number of votes for a candidate with the specified ID

Dependencies:
    - fastapi.APIRouter
    - fastapi.Depends
    - fastapi.status
    - fastapi.HTTPException
    - fastapi.security.OAuth2PasswordRequestForm
    - sqlalchemy.orm.Session
    - typing.List

Models:
    - models.User
    - models.Candidates

Schemas:
    - schemas.Candidate
    - schemas.CandidateCreate
    - schemas.CandidateUpdate

Functions:
    - create_candidate: create a new candidate in the database
    - get_all_candidates: retrieve all candidates from the database
    - get_candidate: retrieve a candidate with the specified ID
    - update_candidate: update a candidate with the specified ID
    - delete_candidate: delete a candidate with the specified ID
    - get_candidate_votes: retrieve the number of votes for a candidate with the specified ID

"""

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, oauth, utils
from typing import List

candidate_router = APIRouter(tags=["Candidates"], prefix="/candidates")


@candidate_router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Candidate)
async def create_candidate(body: schemas.CandidateCreate, db: Session = Depends(get_db),
                           user: models.User = Depends(oauth.get_admin_user)):
    """
    Creates a new candidate in the database with the provided data.

    Args:

        body: An instance of schemas.CandidateCreate containing the data for the new candidate.
        db: An instance of sqlalchemy.orm.Session representing the database session.
        user: An instance of models.User representing the admin user making the request.
    Returns:
        An instance of schemas.Candidate representing the newly created candidate.
    """
    data = body.dict()
    new_candidate = models.Candidates(**data, created_by=user.id)
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)
    return new_candidate


@candidate_router.get("", response_model=List[schemas.Candidate])
async def get_all_candidates(db: Session = Depends(get_db)):
    """
    Retrieves all candidates from the database.

    Args:

        db: An instance of sqlalchemy.orm.Session representing the database session.
    Returns:
        A list of instances of schemas.Candidate representing all candidates in the database.

    """
    data = db.query(models.Candidates).all()
    return data


@candidate_router.get("/{candidateId}", response_model=schemas.Candidate)
async def get_candidate(candidateId: int, db: Session = Depends(get_db)):
    """
    Retrieves a candidate with the specified ID from the database.

    Args:

        candidateId: An integer representing the ID of the candidate to retrieve.
        db: An instance of sqlalchemy.orm.Session representing the database session.
    Returns:
        An instance of schemas.Candidate representing the candidate with the specified ID.
    """
    candidate = db.query(models.Candidates).where(
        models.Candidates.id == candidateId).first()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No candidate found with id: {candidateId}"
        )

    return candidate


@candidate_router.patch("/{candidateId}")
async def update_candidate(
        candidateId: int, body: schemas.CandidateUpdate,
        db: Session = Depends(get_db), user: models.User = Depends(oauth.get_admin_user)
):
    """
    Updates the details of a candidate with the specified ID in the database.

    Args:

        candidateId: An integer representing the ID of the candidate to update.
        body: An instance of schemas.CandidateUpdate containing the data to update the candidate with.
        db: An instance of sqlalchemy.orm.Session representing the database session.
        user: An instance of models.User representing the admin user making the request.
    Returns:
        An instance of schemas.Candidate representing the updated candidate.
    """
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
async def delete_candidate(
        candidateId: int, db: Session = Depends(get_db),
        user: int = Depends(oauth.get_admin_user)
):
    """
    Deletes a candidate with the specified ID from the database.

    Args:

        candidateId: An integer representing the ID of the candidate to delete.
        db: An instance of sqlalchemy.orm.Session representing the database session.
        user: An instance of models.User representing the admin user making the request.
    Returns:
        None.
    """
    db.query(models.Candidates).where(
        models.Candidates.id == candidateId).delete()
    db.commit()
    return None


@candidate_router.get("/{candidateId}/votes")
def get_candidate_votes(candidateId: int, db: Session = Depends(get_db)):
    """
    Retrieves the number of votes for a candidate with the specified ID.

    Args:

        candidateId: An integer representing the ID of the candidate to retrieve the votes for.
        db: An instance of sqlalchemy.orm.Session representing the database session.
    Returns:
        A dictionary containing the ID of the election the candidate is running in and the number of votes they have received.

    """
    candidate: models.Candidates = db.query(models.Candidates).where(
        models.Candidates.id == candidateId).first()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No candidate found with id: {candidateId}"
        )

    return {"election": candidate.election_id, "votes": candidate.votes}
