#!/usr/bin/python3
"""This file defines the endpoints related to election"""

from fastapi import APIRouter, status, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app import models

router = APIRouter(tags=["Candidates"], prefix="/elections")


@router.get("")
def get_all_elections(db: Session = Depends(get_db)):
    """Retrieve and return all elections"""
    data = db.query(models.Election).all()
    return {"message": "All elections", "data": data}


@router.post("", status_code=status.HTTP_201_CREATED)
def create_election():
    """Creates an election"""
    return "This route create a new election election"


@router.get("/{electionId}")
def get_one_election(electionId: str):
    """Fetch single election base on ID"""
    return {}


@router.patch("/{electionId}")
def update_election(electionId: str):
    """Updates an election base on Id"""
    return {}


@router.delete("/{electionId}")
def delete_election(electionId: str):
    """Updates an election base on Id"""
    return None


@router.get("/active/mine")
def get_active_elections():
    """Find the active elections available to the logged in user
    """

    return {"message": "My active elections"}
