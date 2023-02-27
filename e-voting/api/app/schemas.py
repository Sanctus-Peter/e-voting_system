from datetime import datetime
from pydantic import BaseModel, EmailStr, conint, validator
from typing import Optional, List


class ElectionCreate (BaseModel):
    title: str
    state: Optional[str]
    lga: Optional[str]
    start_date: datetime
    end_date: datetime

    @validator("start_date")
    def validate_start_date(cls, val):
        """Confirm that satrt date is a future date

        Args:
            val (date): potential Value
        """
        # print(type(val), ">>>", val)
        # if val < datetime(
        #     year=datetime.now().year, month=datetime.now().month, day=datetime.now().day
        # ):
        #     raise ValueError("start_date is not a future date")
        return val

    @validator("end_date")
    def validate_end_date(cls, val):
        """Confirm that end_date is later than start_date

        Args:
            val (date): potential value
        """
        # if val < cls.start_date:
        #     raise ValueError("end_date has to be later than start date")
        return val


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


class VoteCreate(BaseModel):
    voterId: str
    electionId: str


class Vote(VoteCreate):
    voted_at: datetime
