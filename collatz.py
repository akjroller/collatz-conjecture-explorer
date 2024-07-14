import datetime
import signal
import sys
import sqlite3

from database.database import setup_database
from services.collatz_service import check_collatz, calculate_stats

DB_FILE = "collatz.db"
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()


def shutdown(signal, frame):
    """Handle shutdown signal to calculate stats and close database connection."""
    calculate_stats()
    conn.close()
    sys.exit(0)


def main():
    """Main function to set up database and start Collatz processing."""
    setup_database()

    c.execute("SELECT MAX(starting_number) FROM collatz")
    last_number = c.fetchone()[0]
    start_number = last_number + 1 if last_number else 1

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    i = start_number
    print(f"Starting processing from number: {i}")
    while True:
        try:
            steps, max_value, sequence_length, converges = check_collatz(i)
        except Exception as e:
            print(f"Error encountered while processing {i}: {e}")
            break

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute(
            "INSERT INTO collatz VALUES (?, ?, ?, ?, ?, ?)",
            (i, steps, max_value, sequence_length, converges, timestamp),
        )
        c.execute("INSERT INTO date_time (id) VALUES (?)", (i,))
        conn.commit()
        i += 1


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
