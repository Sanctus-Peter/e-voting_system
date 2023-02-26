from datetime import datetime
from pydantic import BaseModel, EmailStr


class CreateVoter(BaseModel):
    name: str
    email: EmailStr
    password: str
    nin: int
    ward: str
    state: str
    address: str
    dob: datetime.date
    gender: str
    mobile_no: int
