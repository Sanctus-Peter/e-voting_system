from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional, List


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
