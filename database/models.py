from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Collatz(Base):
    """SQLAlchemy model storing Collatz computations."""

    __tablename__ = "collatz"

    starting_number = Column(Integer, primary_key=True, index=True)
    number_of_steps = Column(Integer, nullable=False)
    max_value = Column(Integer, nullable=False)
    sequence_length = Column(Integer, nullable=False)
    convergence = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)


class SequenceLength(Base):
    """Cache of known sequence lengths to speed up computations."""

    __tablename__ = "sequence_length"

    number = Column(Integer, primary_key=True)
    steps = Column(Integer, nullable=False)


class Convergence(Base):
    """Tracks convergence results for starting numbers."""

    __tablename__ = "convergence"

    number = Column(Integer, primary_key=True)
    converges = Column(Boolean, nullable=False)


class Distribution(Base):
    """Stores computed distribution statistics for Collatz data."""

    __tablename__ = "distribution"

    stat_name = Column(String, primary_key=True)
    value = Column(Float, nullable=False)


class DateTimeEntry(Base):
    """Keeps a log of computation timestamps."""

    __tablename__ = "date_time"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)


class CollatzRecord(BaseModel):
    """Pydantic schema mirroring the Collatz ORM model."""

    starting_number: int
    number_of_steps: int
    max_value: int
    sequence_length: int
    convergence: bool
    timestamp: datetime

    class Config:
        orm_mode = True
        from_attributes = True
