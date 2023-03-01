from datetime import date, datetime
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from fastapi import HTTPException, status


class CreateVoter(BaseModel):
    name: str
    email: EmailStr
    password: str
    nin: str
    state: str
    lga: str
    address: str
    dob: date
    gender: str
    mobile_no: str

    @validator("dob")
    def validate_dob(cls, v):
        if v > date(date.today().year - 18, date.today().month, date.today().day):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="You must be at least 18 years old to be able to vote"
            )
        return v


class Official(BaseModel):
    admin_id: str
    email: EmailStr
    name: str

    class Config:
        orm_mode = True


class ElectionCreate(BaseModel):
    title: str
    state: Optional[str]
    lga: Optional[str]
    start_date: datetime
    end_date: datetime


class ElectionUpdate(BaseModel):
    title: Optional[str]
    state: Optional[str]
    lga: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]


class Election(ElectionCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TokData(BaseModel):
    id: Optional[str] = None


class Token(BaseModel):
    token: str
    type: str


class VoteCreate(BaseModel):
    candidateId: int
    electionId: int


class Vote(VoteCreate):
    id: int
    voterId: int
    voted_at: datetime

    class Config:
        orm_mode = True


class CandidateCreate(BaseModel):
    name: str
    party_name: str
    position: str
    state: str
    election_id: int
    ideology: str = "Some random ideologies"


class CandidateUpdate(BaseModel):
    name: Optional[str]
    party_name: Optional[str]
    position: Optional[str]
    state: Optional[str]
    election_id: Optional[int]
    ideology: Optional[str]


class Candidate(CandidateCreate):
    id: int
    reg_date: datetime

    class Config:
        orm_mode = True
