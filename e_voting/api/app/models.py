from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, text, CHAR
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    nin = Column(String, nullable=False, unique=True)
    vin = Column(Integer, nullable=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    ward = Column(String, nullable=False)
    state = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
<<<<<<< HEAD
    mobile_no = Column(CHAR(11), nullable=False)
=======
    mobile_no = Column(Integer, nullable=False)
>>>>>>> parent of 1385510 (added login endpoint)
    dob = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    reg_date = Column(TIMESTAMP(timezone=True),
                      nullable=False, server_default=text("NOW()"))
    role = Column(String, nullable=False, server_default="user")
    accredited = Column(Boolean, nullable=False, server_default="False")
    voted = Column(Boolean, nullable=False, server_default="False")
    admin_id = Column(String)


class Officials(Base):
    __tablename__ = "officials"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    reg_date = Column(TIMESTAMP(timezone=True),
                      nullable=False, server_default=text("NOW()"))


class Candidates(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    party_name = Column(String, ForeignKey(
        "party.name", ondelete="CASCADE"), nullable=False)
    position = Column(String, nullable=False)
    state = Column(String, nullable=False)
    ideology = Column(String, nullable=False)
    reg_date = Column(TIMESTAMP(timezone=True),
                      nullable=False, server_default=text("NOW()"))
    total_votes = Column(Integer, nullable=False, server_default=text("0"))
    election_id = Column(Integer, ForeignKey(
        "election.id", ondelete="CASCADE"
    ), nullable=False)
    created_by = Column(Integer)

    party = relationship("Party")

    # Total Votes earned by this candidate
    votes = relationship("Vote")


class Party(Base):
    __tablename__ = "party"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    party_logo_url = Column(String, nullable=False)
    fullname = Column(String)


class Vote(Base):
    __tablename__ = "votes"
    # Vote is identified by two fields voterId and electionId
    voterId = Column(Integer, primary_key=True, nullable=False)
    electionId = Column(Integer, ForeignKey(
        "election.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    candidateId = Column(Integer, ForeignKey(
        "candidates.id", ondelete="CASCADE"), nullable=False)
    voted_at = Column(TIMESTAMP(timezone=True),
                      nullable=False, server_default=text("Now()"))


class Election(Base):
    __tablename__ = "election"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    # If specified only users from that state can participate
    state = Column(String(255))
    # if specified only users from the lga can participate
    lga = Column(String(255))
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("Now()"))
    created_by = Column(Integer)

    # List of candidates in this election
    candidates = relationship("Candidates")

    # total votes casted in this election
    votes = relationship("Vote")

    def user_eligible(self, user: User):
        """Check if a user is eligible to cast a vote for this election

        Args:
            user (User): The user ti validate

        Returns:
            boolean: True if user is eligible false otherwise
        """
        if not user.accredited:
            return False
        if not self.lga and not self.state:
            return True
        if self.state and not self.lga:
            return self.state.lower() == user.state.lower()
        if self.lga:
            return self.lga.lower() == user.lga.lower()
