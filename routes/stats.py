import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import models
from database.database import get_db

router = APIRouter()


@router.get(
    "/",
    summary="Collatz Computation Statistics",
    description="Get the overall computation statistics, including the last checked number, total computation time, and average steps.",
)
def read_stats(db: Session = Depends(get_db)):
    """Retrieve overall computation statistics."""

    last_number = db.query(func.max(models.Collatz.starting_number)).scalar()
    timestamps = db.query(
        func.min(models.Collatz.timestamp), func.max(models.Collatz.timestamp)
    ).one()
    average_steps = db.query(func.avg(models.Collatz.number_of_steps)).scalar()

    if last_number is None or timestamps[0] is None or timestamps[1] is None:
        return {
            "last_checked_number": 0,
            "total_computation_time": 0,
            "average_steps": 0,
        }

    min_timestamp, max_timestamp = timestamps
    total_time = (max_timestamp - min_timestamp).total_seconds()

    return {
        "last_checked_number": last_number,
        "total_computation_time": total_time,
        "average_steps": average_steps,
    }


@router.get(
    "/hourly",
    summary="Hourly Collatz Statistics",
    description="Get the hourly Collatz computation statistics.",
)
def read_hourly_stats(db: Session = Depends(get_db)):
    """Retrieve hourly Collatz computation statistics."""

    current_time = datetime.datetime.utcnow()
    one_hour_ago = current_time - datetime.timedelta(hours=1)

    count = (
        db.query(func.count(models.Collatz.starting_number))
        .filter(models.Collatz.timestamp.between(one_hour_ago, current_time))
        .scalar()
    )

    return {"collatz_count_last_hour": count}


@router.get(
    "/distribution",
    summary="Collatz Distribution Statistics",
    description="Get the distribution statistics for Collatz computations. This feature is not yet implemented.",
)
def read_distribution():
    """Placeholder for distribution statistics endpoint."""

    return {"message": "Distribution statistics not yet implemented"}
