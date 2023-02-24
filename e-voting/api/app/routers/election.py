#!/usr/bin/python3
"""This file defines the endpoints related to election"""

from fastapi import APIRouter

router = APIRouter(tags=["Candidates"])

@router.get("/")
def get_all_elections():
    """Retrieve and return all elections"""
    return []

@router.post("/")
def create_election():
    """Creates an election"""
    return {}

@router.get("/{electionId}")
def get_one_election(electionId:str):
    """Fetch single election base on ID"""
    return {}

@router.patch("/{electionId}")
def update_election(electionId:str):
    """Updates an election base on Id"""
    return {}

@router.delete("/{electionId}")
def delete_election(electionId:str):
    """Updates an election base on Id"""
    return None
