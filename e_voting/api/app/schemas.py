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
    created_at: datetime

    class Config:
        orm_mode = True


class TokData(BaseModel):
    id: Optional[str] = None


class VoteCreate(BaseModel):
    voterId: int
    electionId: int


class Vote(VoteCreate):
    voted_at: datetime

    class Config:
        orm_mode = True
