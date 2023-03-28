"""
This module defines the API routes and endpoints for managing votes in an election.

Routes:
- POST /votes: Cast a vote in an election
- GET /votes/{electionId}: Retrieve all votes for an election

Dependencies:
- get_db: A function that returns a SQLAlchemy database session
- oauth.get_current_user: A function that returns the current authenticated user

Models:
- User: A SQLAlchemy model representing a user in the database
- Election: A SQLAlchemy model representing an election in the database
- Vote: A SQLAlchemy model representing a vote in the database

Schemas:
- UserBase: A Pydantic schema representing the base user model
- UserCreate: A Pydantic schema representing the user model for creation
- UserUpdate: A Pydantic schema representing the user model for updating
- UserInDB: A Pydantic schema representing the user model as it exists in the database
- Token: A Pydantic schema representing an access token
- ElectionBase: A Pydantic schema representing the base election model
- ElectionCreate: A Pydantic schema representing the election model for creation
- ElectionUpdate: A Pydantic schema representing the election model for updating
- ElectionInDB: A Pydantic schema representing the election model as it exists in the database
- CandidateBase: A Pydantic schema representing the base candidate model
- CandidateCreate: A Pydantic schema representing the candidate model for creation
- CandidateUpdate: A Pydantic schema representing the candidate model for updating
- CandidateInDB: A Pydantic schema representing the candidate model as it exists in the database
- VoteBase: A Pydantic schema representing the base vote model
- VoteCreate: A Pydantic schema representing the vote model for creation
- VoteInDB: A Pydantic schema representing the vote model as it exists in the database
- Vote: A Pydantic schema representing the vote model for API responses

Functions:
- vote: Cast a vote in an election
- get_all_votes_for_election: Retrieve all votes for an election

Args:
- body: A Pydantic schema representing the body of a POST request to the /votes route
- db: A SQLAlchemy database session, obtained from the get_db dependency
- user: A SQLAlchemy model representing the current authenticated user,
            obtained from the oauth.get_current_user dependency
- electionId: An integer representing the ID of an election,
            passed as a path parameter to the /votes/{electionId} route

Returns:
- vote: A Pydantic schema representing the vote that was cast in the /votes route
- votes: A list of Pydantic schemas representing all votes for an election, returned by the /votes/{electionId} route

Raises:
- HTTPException: Raised when an error occurs during the handling of a request,
        such as when an election or candidate is not found, a user is not eligible to vote in an election,
        a user has already voted in an election, or when a request is unauthorized or forbidden.
"""

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
    """
       Cast a vote in an election.

       Args:
           body (schemas.VoteCreate): The details of the vote to be cast.
           db (Session, optional): The database session. Defaults to Depends(get_db).
           user (models.User, optional): The user casting the vote. Defaults to Depends(oauth.get_current_user).

       Returns:
           models.Vote: The vote object that was created.

       Raises:
           HTTPException:
               404 Not Found: If the election with the given ID does not exist.
               400 Bad Request: If the candidate with the given ID is not registered for this election.
               403 Forbidden: If the election is closed, the user is not eligible to vote, or the user has already voted.
               401 Unauthorized: If the user is not authenticated.
    """
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
    """
    Retrieve all votes for an election.

    Args:
        electionId (int): The ID of the election.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[schemas.Vote]: A list of all votes for the election.

    Raises:
        HTTPException:
            404 Not Found: If the election with the given ID does not exist.
    """
    votes = db.query(models.Vote).where(
        models.Vote.electionId == electionId).all()
    return votes
