#!/usr/bin/python3
"""
This module defines the endpoints related to elections.
These endpoints handle operations such as creating, updating, and retrieving elections,
as well as retrieving statistics and participants for a particular election.
The endpoints in this module require authentication and certain actions are restricted to users with admin privileges.

Endpoints:
- GET /elections: Retrieve and return all elections.
- POST /elections: Create a new election.
- GET /elections/active: Retrieve all active elections.
- GET /elections/{electionId}: Retrieve a single election by its ID.
- PATCH /elections/{electionId}: Update a single election by its ID.
- DELETE /elections/{electionId}: Delete a single election by its ID.
- GET /elections/{electionId}/statistics: Retrieve the statistics of a particular election.
- GET /elections/{electionId}/participants: Retrieve the participants (candidates) for a particular election.
- GET /elections/active/mine: Retrieve all active elections available to the logged-in user.

This module depends on other modules such as `database`, `models`, `schemas`, `utils`, and `oauth`.
It uses SQLAlchemy for interacting with the database and FastAPI for creating the API.
"""
from fastapi import APIRouter, status, Depends, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth
from datetime import datetime
from typing import List
from sqlalchemy import or_, and_, func

router = APIRouter(tags=["Elections"], prefix="/elections")


@router.get("", response_model=List[schemas.Election])
def get_all_elections(db: Session = Depends(get_db)):
    """
    Retrieve and return all elections.

    Dependencies: Depends(get_db)
    Models: models.Election
    Schemas: schemas.Election

    Args:
        - db: Session (default: Depends(get_db)) - SQLAlchemy Session object
    Returns:
        - List[schemas.Election] - a list of Election objects in the form of a schema
    Raises:
        - None
    """

    data = db.query(models.Election).all()
    return data


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Election)
def create_election(election: schemas.ElectionCreate,
                    db: Session = Depends(get_db), user: models.User = Depends(oauth.get_admin_user)):
    """
    Creates a new election in the database.

    Args:
        election (schemas.ElectionCreate): The details of the election to be created.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        user (models.User, optional): The authenticated user. Defaults to Depends(oauth.get_admin_user).

    Returns:
        schemas.Election: The details of the newly created election.
    """

    data = election.dict()
    new_election = models.Election(**data, created_by=user.id)
    db.add(new_election)
    db.commit()
    db.refresh(new_election)
    return new_election


@router.get("/active", response_model=List[schemas.Election])
def get_active_elections(db: Session = Depends(get_db)):
    """
    Fetches all active elections from the database.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[schemas.Election]: A list of active elections.
    """

    E = models.Election
    qry = db.query(E).where(
        (E.end_date > datetime.utcnow())
    )

    return qry.all()


@router.get("/{electionId}", response_model=schemas.Election)
def get_one_election(electionId: str, db: Session = Depends(get_db)):
    """
    Fetches a single election from the database by ID.

    Args:
        electionId (str): The ID of the election to fetch.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        schemas.Election: The details of the election.

    Raises:
        HTTPException: If the election with the specified ID is not found in the database.
    """

    election = db.query(models.Election).where(
        models.Election.id == electionId).first()
    if not election:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Election with id={electionId} not found!")
    return election


@router.patch("/{electionId}", response_model=schemas.Election)
def update_election(electionId: str, body: schemas.ElectionUpdate,
                    db: Session = Depends(get_db), user: models.User = Depends(oauth.get_admin_user)):
    """
    Updates an existing election in the database by ID.

    Args:
        electionId (str): The ID of the election to update.
        body (schemas.ElectionUpdate): The new details to update the election with.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        user (models.User, optional): The authenticated user. Defaults to Depends(oauth.get_admin_user).

    Returns:
        schemas.Election: The updated details of the election.

    Raises:
        HTTPException: If the election with the specified ID is not found in the database.
    """

    qry = db.query(models.Election).where(models.Election.id == electionId)
    old = qry.first()
    if not old:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Election with id={electionId} not found!")
    data = utils.filter_nones(body.dict())
    if data == {}:
        return old
    qry.update(data)
    db.commit()
    db.refresh(old)
    return old


@router.delete("/{electionId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_election(electionId: str, db: Session = Depends(get_db),
                    user: models.User = Depends(oauth.get_admin_user)):
    """
    Deletes an existing election from the database by ID.

    Args:
        electionId (str): The ID of the election to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        user (models.User, optional): The authenticated user. Defaults to Depends(oauth.get_admin_user).

    Returns:
        None

    Raises:
        HTTPException: If the election with the specified ID is not found in the database.
    """

    db.query(models.Election).where(models.Election.id == electionId).delete()
    db.commit()
    return None


@router.get("/{electionId}/statistics")
def get_election_statistics(electionId: int, db: Session = Depends(get_db)):
    """
    Retrieve and return the statistics of an election, including vote distribution and percentages.

    Args:
        electionId (int): The ID of the election to retrieve statistics for.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A dictionary containing the statistics for the election.

    Raises:
        HTTPException: Raised if no election is found with the given ID.
    - mark as TODO
    """

    return "Stats"


@router.get("/{electionId}/participants")
def get_election_participants(electionId: int, db: Session = Depends(get_db)):
    """
    Retrieve the list of candidates and parties participating in an election.

    Args:
        electionId (int): The ID of the election to fetch participants for.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A dictionary with the ID of the election and a list of candidate and party information.
            Each item in the list contains the party name, logo URL, candidate name, and ID.

    Raises:
        HTTPException: Raised with a 404 status code if the election is not found in the database.
    """
    election: models.Election = db.query(models.Election).where(
        models.Election.id == electionId).first()
    if not election:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Election with id={electionId} not found!")

    candidates: List[models.Candidates] = election.candidates
    result = []
    for candidate in candidates:
        party: models.Party = candidate.party
        result.insert(0, {
            "party_name": party.name,
            "party_logo": party.party_logo_url,
            "candidate_name": candidate.name,
            "candidate_id": candidate.id
        })

    return {"election": election.id, "participants": result}


@router.get("/active/mine")
def get_active_elections(db: Session = Depends(get_db), user: models.User = Depends(oauth.get_current_user)):
    """
        Returns a list of all active elections available to the logged-in user.
        - All national elections (state = null and lga = null)
        - All user's state elections (state = user.state and lga = null)
        - All user's lga elections (lga = user.lga)

        Args:
            db (Session, optional): Database session. Defaults to Depends(get_db).
            user (models.User, optional): The logged-in user. Defaults to Depend on(oauth.get_current_user).

        Returns:
            list: A list of all active elections available to the logged-in user.
    """

    E = models.Election
    qry = db.query(E).where(
        and_(
            E.end_date > datetime.utcnow(),
            or_(
                and_(func.coalesce(E.state, "") ==
                     "", func.coalesce(E.lga, "") == ""),
                and_(E.state == user.state, func.coalesce(E.lga, "") == ""),
                (E.lga == user.lga)
            )
        )
    )

    return qry.all()
