import sqlite3
from statistics import median, pstdev

DB_FILE = "collatz.db"


def check_collatz(n):
    """Perform the Collatz conjecture calculation for a given number."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    original_n, steps, max_value = n, 0, n
    sequence = []
    remaining_steps = 0
    cached_max_value = None
    converges = 0

    while True:
        sequence.append(n)
        c.execute("SELECT steps FROM sequence_length WHERE number = ?", (n,))
        row = c.fetchone()

        if row:
            cached_steps = row[0]
            steps += cached_steps
            remaining_steps = cached_steps
            c.execute(
                "SELECT max_value FROM collatz WHERE starting_number = ?", (n,)
            )
            cached_max = c.fetchone()
            if cached_max is not None:
                cached_max_value = cached_max[0]
                max_value = max(max_value, cached_max_value)
            c.execute(
                "SELECT converges FROM convergence WHERE number = ?", (n,)
            )
            cached_convergence = c.fetchone()
            if cached_convergence is not None:
                converges = cached_convergence[0]
            else:
                converges = 1
            break

        if n == 1:
            converges = 1
            break

        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1

        steps += 1
        max_value = max(max_value, n)

    if remaining_steps and cached_max_value is None:
        current = sequence[-1]
        temp_max = max_value
        for _ in range(remaining_steps):
            if current == 1:
                break
            if current % 2 == 0:
                current //= 2
            else:
                current = 3 * current + 1
            temp_max = max(temp_max, current)
        max_value = temp_max

    for i, num in enumerate(sequence):
        c.execute(
            "INSERT OR REPLACE INTO sequence_length VALUES (?, ?)", (num, steps - i)
        )

    c.execute(
        "INSERT OR REPLACE INTO convergence VALUES (?, ?)", (original_n, converges)
    )
    conn.commit()
    conn.close()

    sequence_length = len(sequence) + remaining_steps

    return steps, max_value, sequence_length, converges


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
