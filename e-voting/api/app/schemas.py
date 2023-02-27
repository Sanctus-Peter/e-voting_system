from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class CreateVoter(BaseModel):
    name: str
    email: EmailStr
    password: str
    nin: str
    ward: str
    state: str
    address: str
    dob: datetime.date
    gender: str
    mobile_no: int


class ElectionCreate (BaseModel):
    title: str
    state: Optional[str]
    lga: Optional[str]
    start_date: datetime
    end_date: datetime


class ElectionUpdate (BaseModel):
    title: Optional[str]
    state: Optional[str]
    lga: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]


class Election(ElectionCreate):
    created_at: datetime

    class Config:
        orm_mode = True
