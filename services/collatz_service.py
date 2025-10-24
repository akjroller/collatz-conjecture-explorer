from statistics import median, pstdev
from typing import List

from sqlalchemy.orm import Session

from database import models


def check_collatz(n: int, db: Session):
    """Perform the Collatz conjecture calculation for a given number."""

    original_n = n
    steps = 0
    max_value = n
    sequence: List[int] = []

    while True:
        sequence.append(n)
        cached_length = db.get(models.SequenceLength, n)

        if cached_length is not None:
            steps += cached_length.steps
            break
        elif n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1

        steps += 1
        max_value = max(max_value, n)

        if n in {1, 2, 4}:
            break

    for index, number in enumerate(sequence):
        db.merge(models.SequenceLength(number=number, steps=steps - index))

    converges = n == 1
    db.merge(models.Convergence(number=original_n, converges=converges))

    sequence_length = steps - 1 if steps > 0 else 0
    return steps, max_value, sequence_length, converges


def calculate_stats(db: Session) -> None:
    """Calculate statistics for the Collatz sequences."""

    max_values = [value for (value,) in db.query(models.Collatz.max_value).all()]

    if not max_values:
        return

    stats = {
        "min": min(max_values),
        "max": max(max_values),
        "mean": sum(max_values) / len(max_values),
        "median": median(max_values),
        "std_dev": pstdev(max_values) if len(max_values) > 1 else 0.0,
    }

    for stat, value in stats.items():
        existing = db.get(models.Distribution, stat)
        if existing is None:
            db.add(models.Distribution(stat_name=stat, value=value))
        else:
            existing.value = value

    db.commit()
