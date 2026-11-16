"""Validate rows before transforming them."""

from collections.abc import Iterable


def find_missing_columns(rows: list[dict[str, str]], required: Iterable[str]) -> list[str]:
    """Return the required column names that are missing from the rows.

    Args:
        rows: Rows as returned by read_csv or snake_case_columns.
        required: Column names that must be present.

    Returns:
        The missing column names, in the order they were required.
        If rows is empty, every required column is reported as missing.
    """
    if not rows:
        return list(required)
    present = set(rows[0].keys())
    return [col for col in required if col not in present]