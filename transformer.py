"""Transform rows: rename columns, convert types, and compute totals."""
from datetime import datetime
import re



def to_snake_case(name: str) -> str:
    """Convert a column name to snake_case.

    Examples:
        "Order ID" -> "order_id"
        "freightValue" -> "freight_value"
        "order-item.id" -> "order_item_id"

    Args:
        name: The original column name.

    Returns:
        The name in lowercase snake_case.
    """
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name.strip())
    s = re.sub(r"[\s\-.]+", "_", s)
    s = re.sub(r"[^0-9A-Za-z_]", "", s)
    s = re.sub(r"_+", "_", s)
    return s.lower().strip("_")


def snake_case_columns(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Return new rows with every column name converted to snake_case.

    Args:
        rows: Rows as returned by read_csv.

    Returns:
        A new list of dictionaries with snake_case keys.
    """
    return [{to_snake_case(k): v for k, v in row.items()} for row in rows]



COLUMN_MAPPING: dict[str, str] = {
    "order_id": "order_id",
    "customer_id": "customer_id",
    "order_status": "status",
    "order_purchase_timestamp": "order_date",
    "order_delivered_customer_date": "delivered_date",
    "order_item_id": "line_number",
    "product_id": "product_id",
    "seller_id": "seller_id",
    "shipping_limit_date": "shipping_deadline",
    "price": "item_price",
    "freight_value": "freight_amount",
}


def map_columns(rows: list[dict[str, str]], mapping: dict[str, str]) -> list[dict[str, str]]:
    """Rename columns to the standard schema.

    Columns that aren't in the mapping keep their original names.

    Args:
        rows: Rows with snake_case keys.
        mapping: Dictionary from source column names to standard names.

    Returns:
        A new list of dictionaries with the renamed keys.
    """
    return [{mapping.get(k, k): v for k, v in row.items()} for row in rows]



TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
FLOAT_COLUMNS = ("item_price", "freight_amount")
DATETIME_COLUMNS = ("shipping_deadline", "order_date", "delivered_date")


def to_float(value: str | None) -> float | None:
    """Convert a string to float. Blank values become None.

    Args:
        value: The raw string from the CSV.

    Returns:
        The number as a float, or None if the value is blank.
    """
    if value is None or value.strip() == "":
        return None
    return float(value)


def to_datetime(value: str | None) -> datetime | None:
    """Convert an Olist timestamp string to datetime. Blank values become None.

    Args:
        value: A string like "2018-03-04 12:48:00".

    Returns:
        A datetime object, or None if the value is blank.
    """
    if value is None or value.strip() == "":
        return None
    return datetime.strptime(value.strip(), TIMESTAMP_FORMAT)


def convert_types(rows: list[dict[str, str]]) -> list[dict]:
    """Convert price and freight to float and timestamps to datetime.

    Columns that aren't present in a row are skipped.

    Args:
        rows: Rows with standard column names, as returned by map_columns.

    Returns:
        A new list of dictionaries with converted values.
    """
    converted = []
    for row in rows:
        new_row = dict(row)
        for col in FLOAT_COLUMNS:
            if col in new_row:
                new_row[col] = to_float(new_row[col])
        for col in DATETIME_COLUMNS:
            if col in new_row:
                new_row[col] = to_datetime(new_row[col])
        converted.append(new_row)
    return converted



def calculate_order_totals(rows: list[dict]) -> dict[str, float]:
    """Sum item price and freight for each order.

    Rows with a missing price or freight value count as 0.

    Args:
        rows: Rows with standard column names and converted types,
            as returned by convert_types.

    Returns:
        A dictionary mapping each order_id to its total amount.
    """
    totals: dict[str, float] = {}
    for row in rows:
        order_id = row["order_id"]
        item_price = row.get("item_price") or 0.0
        freight = row.get("freight_amount") or 0.0
        totals[order_id] = totals.get(order_id, 0.0) + item_price + freight
    return {order_id: round(total, 2) for order_id, total in totals.items()}

"""Tests for the transformer functions."""

from transformer import calculate_order_totals, to_float, to_snake_case


def test_to_snake_case_converts_spaces_camel_case_and_punctuation():
    assert to_snake_case("Order ID") == "order_id"
    assert to_snake_case("freightValue") == "freight_value"
    assert to_snake_case("order-item.id") == "order_item_id"


def test_to_float_converts_strings_and_treats_blank_as_none():
    assert to_float("19.18") == 19.18
    assert to_float("  ") is None
    assert to_float(None) is None


def test_calculate_order_totals_sums_price_and_freight_per_order():
    rows = [
        {"order_id": "A", "item_price": 10.0, "freight_amount": 2.5},
        {"order_id": "A", "item_price": 5.0, "freight_amount": None},
        {"order_id": "B", "item_price": 7.25, "freight_amount": 1.0},
    ]
    assert calculate_order_totals(rows) == {"A": 17.5, "B": 8.25}