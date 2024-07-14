import sqlite3
from statistics import median, pstdev

DB_FILE = "collatz.db"


def check_collatz(n):
    """Perform the Collatz conjecture calculation for a given number."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    original_n, steps, max_value = n, 0, n
    sequence = []

    while True:
        sequence.append(n)
        c.execute("SELECT steps FROM sequence_length WHERE number = ?", (n,))
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

        if n in {1, 2, 4}:
            break

    for i, num in enumerate(sequence):
        c.execute(
            "INSERT OR REPLACE INTO sequence_length VALUES (?, ?)", (num, steps - i)
        )

    converges = 1 if n == 1 else 0
    c.execute(
        "INSERT OR REPLACE INTO convergence VALUES (?, ?)", (original_n, converges)
    )
    conn.commit()
    conn.close()

    return steps, max_value, steps - 1, converges


def calculate_stats():
    """Calculate statistics for the Collatz sequences."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT max_value FROM collatz")
    max_values = [row[0] for row in c.fetchall()]

    stats = {
        "min": min(max_values) if max_values else 0,
        "max": max(max_values) if max_values else 0,
        "mean": sum(max_values) / len(max_values) if max_values else 0,
        "median": median(max_values) if max_values else 0,
        "std_dev": pstdev(max_values) if max_values else 0,
    }

    for stat, value in stats.items():
        c.execute("INSERT INTO distribution VALUES (?, ?)", (stat, value))
    conn.commit()
    conn.close()
