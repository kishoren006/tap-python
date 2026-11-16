"""Read CSV files into lists of dictionaries."""

import csv
from pathlib import Path


def read_csv(path: str | Path) -> list[dict[str, str]]:
    """Read a CSV file and return its rows as dictionaries.

    Args:
        path: Path to a comma-delimited CSV file with a header row.

    Returns:
        One dictionary per data row, keyed by the header names.
    """
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))