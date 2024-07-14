from pydantic import BaseModel


class CollatzRecord(BaseModel):
    """Pydantic model for a Collatz record."""

    starting_number: int
    number_of_steps: int
    max_value: int
    sequence_length: int
    convergence: int
    timestamp: str
