from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import CollatzRecord
from utils.logger import logger

router = APIRouter()


@router.get(
    "/{num}",
    response_model=CollatzRecord,
    summary="Retrieve Collatz Sequence",
    description="Get the Collatz sequence and its statistics for a specific starting number.",
)
def read_collatz(num: int, db: Session = Depends(get_db)):
    """Retrieve Collatz sequence and its statistics for a specific starting number."""
    logger.info(f"Accessing Collatz sequence for number: {num}")
    c = db.execute("SELECT * FROM collatz WHERE starting_number = ?", (num,))
    data = c.fetchone()
    if data is None:
        raise HTTPException(status_code=404, detail="No data found for this number.")
    else:
        return CollatzRecord(
            starting_number=data[0],
            number_of_steps=data[1],
            max_value=data[2],
            sequence_length=data[3],
            convergence=data[4],
            timestamp=data[5],
        )


@router.get(
    "/range/{start}/{end}",
    summary="Collatz Sequences in Range",
    description="Get the Collatz sequences for a range of starting numbers.",
)
def read_collatz_range(start: int, end: int, db: Session = Depends(get_db)):
    """Retrieve Collatz sequences for a range of starting numbers."""
    c = db.execute(
        "SELECT * FROM collatz WHERE starting_number BETWEEN ? AND ?", (start, end)
    )
    data = c.fetchall()
    return [
        {
            "starting_number": x[0],
            "number_of_steps": x[1],
            "max_value": x[2],
            "sequence_length": x[3],
            "convergence": x[4],
            "timestamp": x[5],
        }
        for x in data
    ]


@router.get(
    "/top/{n}",
    summary="Top N Collatz Sequences",
    description="Get the top N Collatz sequences with the highest number of steps.",
)
def read_top_collatz(n: int, db: Session = Depends(get_db)):
    """Retrieve the top N Collatz sequences with the highest number of steps."""
    c = db.execute("SELECT * FROM collatz ORDER BY number_of_steps DESC LIMIT ?", (n,))
    data = c.fetchall()
    return [
        {
            "starting_number": x[0],
            "number_of_steps": x[1],
            "max_value": x[2],
            "sequence_length": x[3],
            "convergence": x[4],
            "timestamp": x[5],
        }
        for x in data
    ]


@router.get(
    "/average/{n}",
    summary="Average Collatz Statistics",
    description="Get the average number of steps and average max value over the last N Collatz sequences.",
)
def read_average_collatz(n: int, db: Session = Depends(get_db)):
    """Retrieve the average number of steps and average max value over the last N Collatz sequences."""
    c = db.execute(
        "SELECT AVG(number_of_steps), AVG(max_value) FROM (SELECT * FROM collatz ORDER BY starting_number DESC LIMIT ?)",
        (n,),
    )
    avg_steps, avg_max = c.fetchone()
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
    c = db.execute(
        "SELECT * FROM collatz WHERE number_of_steps = ? AND max_value = ?",
        (number_of_steps, max_value),
    )
    data = c.fetchall()
    return [
        {
            "starting_number": x[0],
            "number_of_steps": x[1],
            "max_value": x[2],
            "sequence_length": x[3],
            "convergence": x[4],
            "timestamp": x[5],
        }
        for x in data
    ]
