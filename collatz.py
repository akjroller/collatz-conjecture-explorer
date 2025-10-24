import datetime
import signal
import sys

from sqlalchemy import func
from sqlalchemy.orm import Session

from database import models
from database.database import SessionLocal, setup_database
from services.collatz_service import check_collatz, calculate_stats


def shutdown(session: Session):
    """Create a signal handler that gracefully shuts down the process."""

    def handler(signum, frame):
        calculate_stats(session)
        session.close()
        sys.exit(0)

    return handler


def main():
    """Main function to setup the database and start Collatz sequence calculations."""

    setup_database()
    session = SessionLocal()

    signal.signal(signal.SIGINT, shutdown(session))
    signal.signal(signal.SIGTERM, shutdown(session))

    last_number = session.query(func.max(models.Collatz.starting_number)).scalar()
    start_number = (last_number or 0) + 1

    print(f"Starting processing from number: {start_number}")

    i = start_number
    try:
        while True:
            try:
                steps, max_value, sequence_length, converges = check_collatz(i, session)
            except Exception as exc:  # pragma: no cover - logging during long run
                print(f"Error encountered while processing {i}: {exc}")
                break

            record = models.Collatz(
                starting_number=i,
                number_of_steps=steps,
                max_value=max_value,
                sequence_length=sequence_length,
                convergence=converges,
                timestamp=datetime.datetime.utcnow(),
            )
            session.add(record)
            session.merge(models.DateTimeEntry(id=i))
            session.commit()
            i += 1
    finally:
        session.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"An error occurred: {exc}")
        raise
