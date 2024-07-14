from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import datetime

from database.database import get_db

router = APIRouter()


@router.get(
    "/",
    summary="Collatz Computation Statistics",
    description="Get the overall computation statistics, including the last checked number, total computation time, and average steps.",
)
def read_stats(db: Session = Depends(get_db)):
    """Retrieve overall computation statistics."""
    c = db.execute(
        "SELECT MAX(starting_number), MIN(timestamp), MAX(timestamp) FROM collatz"
    )
    last_number, min_timestamp_str, max_timestamp_str = c.fetchone()
    c = db.execute("SELECT AVG(number_of_steps) FROM collatz")
    average_steps = c.fetchone()[0]

    if last_number is None:
        return {
            "last_checked_number": 0,
            "total_computation_time": 0,
            "average_steps": 0,
        }
    else:
        min_timestamp = datetime.datetime.strptime(
            min_timestamp_str, "%Y-%m-%d %H:%M:%S"
        )
        max_timestamp = datetime.datetime.strptime(
            max_timestamp_str, "%Y-%m-%d %H:%M:%S"
        )
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
    current_time = datetime.datetime.now()
    one_hour_ago = current_time - datetime.timedelta(hours=1)

    c = db.execute(
        "SELECT COUNT(*) FROM collatz WHERE timestamp BETWEEN ? AND ?",
        (one_hour_ago, current_time),
    )
    count = c.fetchone()[0]

    return {"collatz_count_last_hour": count}


@router.get(
    "/distribution",
    summary="Collatz Distribution Statistics",
    description="Get the distribution statistics for Collatz computations. This feature is not yet implemented.",
)
def read_distribution():
    """Placeholder for distribution statistics endpoint."""
    return {"message": "Distribution statistics not yet implemented"}
