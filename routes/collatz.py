from typing import Iterable, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import models
from database.database import get_db
from utils.logger import logger

router = APIRouter()


def _to_record(model: models.Collatz) -> models.CollatzRecord:
    """Convert an ORM instance to its Pydantic schema."""

    return models.CollatzRecord(
        starting_number=model.starting_number,
        number_of_steps=model.number_of_steps,
        max_value=model.max_value,
        sequence_length=model.sequence_length,
        convergence=model.convergence,
        timestamp=model.timestamp,
    )


def _serialize(records: Iterable[models.Collatz]) -> List[models.CollatzRecord]:
    return [_to_record(record) for record in records]


@router.get(
    "/{num}",
    response_model=models.CollatzRecord,
    summary="Retrieve Collatz Sequence",
    description="Get the Collatz sequence and its statistics for a specific starting number.",
)
def read_collatz(num: int, db: Session = Depends(get_db)):
    """Retrieve Collatz sequence and its statistics for a specific starting number."""

    logger.info("Accessing Collatz sequence for number: %s", num)
    record = db.get(models.Collatz, num)
    if record is None:
        raise HTTPException(status_code=404, detail="No data found for this number.")
    return _to_record(record)


@router.get(
    "/range/{start}/{end}",
    summary="Collatz Sequences in Range",
    description="Get the Collatz sequences for a range of starting numbers.",
)
def read_collatz_range(start: int, end: int, db: Session = Depends(get_db)):
    """Retrieve Collatz sequences for a range of starting numbers."""

    results = (
        db.query(models.Collatz)
        .filter(models.Collatz.starting_number.between(start, end))
        .order_by(models.Collatz.starting_number.asc())
        .all()
    )
    return _serialize(results)


@router.get(
    "/top/{n}",
    summary="Top N Collatz Sequences",
    description="Get the top N Collatz sequences with the highest number of steps.",
)
def read_top_collatz(n: int, db: Session = Depends(get_db)):
    """Retrieve the top N Collatz sequences with the highest number of steps."""

    results = (
        db.query(models.Collatz)
        .order_by(models.Collatz.number_of_steps.desc())
        .limit(n)
        .all()
    )
    return _serialize(results)


@router.get(
    "/average/{n}",
    summary="Average Collatz Statistics",
    description="Get the average number of steps and average max value over the last N Collatz sequences.",
)
def read_average_collatz(n: int, db: Session = Depends(get_db)):
    """Retrieve the average number of steps and average max value over the last N Collatz sequences."""

    subquery = (
        db.query(models.Collatz)
        .order_by(models.Collatz.starting_number.desc())
        .limit(n)
        .subquery()
    )
    avg_steps, avg_max = db.query(
        func.avg(subquery.c.number_of_steps), func.avg(subquery.c.max_value)
    ).one()
    return {"average_number_of_steps": avg_steps, "average_max_value": avg_max}


@router.get(
    "/search/{number_of_steps}/{max_value}",
    summary="Search Collatz Sequences",
    description="Search for Collatz sequences by a specific number of steps and max value.",
)
def read_search_collatz(
    number_of_steps: int, max_value: int, db: Session = Depends(get_db)
):
    """Search for Collatz sequences by a specific number of steps and max value."""

    results = (
        db.query(models.Collatz)
        .filter(
            models.Collatz.number_of_steps == number_of_steps,
            models.Collatz.max_value == max_value,
        )
        .order_by(models.Collatz.starting_number.asc())
        .all()
    )
    return _serialize(results)
