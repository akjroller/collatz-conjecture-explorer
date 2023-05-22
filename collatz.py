import sqlite3
import datetime
import signal
import sys
from statistics import median, pstdev

# Name of the database file
DB_FILE = 'collatz.db'


# Function to set up the database
def setup_database():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()

        # Definitions of the tables to be created
        tables = {
            "collatz": """CREATE TABLE IF NOT EXISTS collatz (
                          starting_number INTEGER,
                          number_of_steps INTEGER,
                          max_value INTEGER,
                          sequence_length INTEGER,
                          convergence INTEGER,
                          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                          )""",
            "distribution": """CREATE TABLE IF NOT EXISTS distribution (
                               stat_name TEXT,
                               value REAL
                               )""",
            "sequence_length": """CREATE TABLE IF NOT EXISTS sequence_length (
                                  number INTEGER PRIMARY KEY,
                                  steps INTEGER
                                  )""",
            "convergence": """CREATE TABLE IF NOT EXISTS convergence (
                              number INTEGER PRIMARY KEY,
                              converges INTEGER
                              )""",
            "date_time": """CREATE TABLE IF NOT EXISTS date_time (
                            id INTEGER PRIMARY KEY,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                            )""",
        }

        # Create the tables
        for table in tables.values():
            c.execute(table)


# Function to check the Collatz Conjecture for a given number
def check_collatz(n):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()

        # Initial values
        original_n, steps, max_value = n, 0, n

        # List to store the sequence
        sequence = []

        # Loop until the number becomes 1
        while True:
            sequence.append(n)
            c.execute('SELECT steps FROM sequence_length WHERE number = ?', (n,))
            row = c.fetchone()

            if row:
                steps += row[0]
                break
            elif n % 2 == 0:
                n //= 2
            else:
                n = 3 * n + 1

            steps += 1
            max_value = max(max_value, n)

            # Detect the 1-4-2-1 loop
            if n in {1, 2, 4}:
                break

        # Update the sequence_length table
        for i, num in enumerate(sequence):
            c.execute('INSERT OR REPLACE INTO sequence_length VALUES (?, ?)', (num, steps - i))

        # Check for convergence
        converges = 1 if n == 1 else 0
        c.execute('INSERT OR REPLACE INTO convergence VALUES (?, ?)', (original_n, converges))

        return steps, max_value, steps - 1, converges


# Function to run when the program is shut down
def shutdown(signal, frame):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()

        # Retrieve max_value data
        c.execute('SELECT max_value FROM collatz')
        max_values = [row[0] for row in c.fetchall()]

        # Calculate statistics
        stats = {
            'min': min(max_values) if max_values else 0,
            'max': max(max_values) if max_values else 0,
            'mean': sum(max_values) / len(max_values) if max_values else 0,
            'median': median(max_values) if max_values else 0,
            'std_dev': pstdev(max_values) if max_values else 0
        }

        # Update the distribution table
        for stat, value in stats.items():
            c.execute('INSERT INTO distribution VALUES (?, ?)', (stat, value))

    sys.exit(0)


# Main function to run the program
def main():
    # Set up the database
    setup_database()

    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()

        # Retrieve the last number processed
        c.execute('SELECT MAX(starting_number) FROM collatz')
        last_number = c.fetchone()[0]
        start_number = last_number + 1 if last_number else 1

        # Set up signal handlers
        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)

        # Process each number from start_number to infinity
        for i in range(start_number, float('inf')):
            print(f"Currently working on: {i}")
            steps, max_value, sequence_length, converges = check_collatz(i)

            # If the Collatz Conjecture is not satisfied
            if steps is None:
                print("Found a number that does not satisfy the Collatz Conjecture:", i)
                break

            # Update the collatz and date_time tables
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("INSERT INTO collatz VALUES (?, ?, ?, ?, ?, ?)", (i, steps, max_value, sequence_length, converges, timestamp))
            c.execute("INSERT INTO date_time (id) VALUES (?)", (i,))


# Run the main function if this script is run directly
if __name__ == "__main__":
    main()
