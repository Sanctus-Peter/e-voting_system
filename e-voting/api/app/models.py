from enum import unique

from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    nin = Column(Integer, nullable=False, unique=True)
    vin = Column(Integer, nullable=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    ward = Column(String, nullable=False)
    state = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    reg_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
    role = Column(String, nullable=False, server_default="user")


class Officials(Base):
    __tablename__ = "officials"


class Candidates(User):
    __tablename__ = "candidates"


class Party(Base):
    __tablename__ = "party"


class Vote(Base):
    __tablename__ = "votes"


class Election(Base):
    __tablename__ = "election"
