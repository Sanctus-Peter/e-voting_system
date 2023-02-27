#!/usr/bin/python3
"""This file defines the endpoints related to election"""

from fastapi import APIRouter, status, Depends, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth
from datetime import datetime
from typing import List
from sqlalchemy import or_, and_, func

router = APIRouter(tags=["Candidates"], prefix="/elections")


@router.get("", response_model=List[schemas.Election])
def get_all_elections(db: Session = Depends(get_db)):
    """Retrieve and return all elections"""
    data = db.query(models.Election).all()
    return data


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Election)
def create_election(election: schemas.ElectionCreate,
                    db: Session = Depends(get_db), user: models.User = Depends(oauth.get_admin_user)):
    """Creates an election
    - todo : set up authorization
    """
    data = election.dict()
    new_election = models.Election(**data)
    db.add(new_election)
    db.commit()
    db.refresh(new_election)
    return new_election


@router.get("/active", response_model=List[schemas.Election])
def get_active_elections(db: Session = Depends(get_db)):
    """Find all active elections 
    """
    E = models.Election
    qry = db.query(E).where(
        (E.end_date > datetime.utcnow())
    )

    return qry.all()


@router.get("/{electionId}", response_model=schemas.Election)
def get_one_election(electionId: str, db: Session = Depends(get_db)):
    """Fetch single election base on ID"""
    election = db.query(models.Election).where(
        models.Election.id == electionId).first()
    if not election:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Election with id={electionId} not found!")
    return election


@router.patch("/{electionId}", response_model=schemas.Election)
def update_election(electionId: str, body: schemas.ElectionUpdate,
                    db: Session = Depends(get_db), user: models.User = Depends(oauth.get_admin_user)):
    """Updates an election base on Id
        Restricted to admin
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
    """Deletes an election base on Id
        Restricted to admin
    """
    db.query(models.Election).where(models.Election.id == electionId).delete()
    return None


@router.get("/active/mine")
def get_active_elections(db: Session = Depends(get_db), user: models.User = Depends(oauth.get_current_user)):
    """Find the active elections available to the logged in user
        All national elections (state = null and lga = null)
        All user's state elections (state = user.state and lga = null)
        All user's lga elections (lga = user.lga) 
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
