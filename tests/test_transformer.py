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