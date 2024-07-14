import sqlite3


def get_db():
    """Yields a database connection."""
    conn = sqlite3.connect("collatz.db")
    db = conn.cursor()
    try:
        yield db
    finally:
        conn.close()


def setup_database():
    """Creates the necessary tables if they do not exist."""
    conn = sqlite3.connect("collatz.db")
    c = conn.cursor()
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
    for table in tables.values():
        c.execute(table)
    conn.commit()
    conn.close()
