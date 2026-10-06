
from typing import Any

import pandas as pd


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add calculated business metrics to the sales data."""

    result = df.copy()

    # Revenue = quantity × unit_price × (1 - discount)
    if {"quantity", "unit_price", "discount"}.issubset(result.columns):
        result["revenue"] = (
            pd.to_numeric(result["quantity"])
            * pd.to_numeric(result["unit_price"])
            * (1 - pd.to_numeric(result["discount"]))
        )

    return result


def calculate_sum(df: pd.DataFrame, column: str) -> float:
    """Calculate the total of a numeric column."""

    if not column or column not in df.columns:
        raise ValueError(f"Column not found: {column}")

    return float(pd.to_numeric(df[column]).sum())


def calculate_average(df: pd.DataFrame, column: str) -> float:
    """Calculate the average of a numeric column."""

    if not column or column not in df.columns:
        raise ValueError(f"Column not found: {column}")

    if df.empty:
        return 0.0

    return float(pd.to_numeric(df[column]).mean())


def calculate_count(df: pd.DataFrame, column: str) -> int:
    """Count non-null values in a column."""

    if not column or column not in df.columns:
        raise ValueError(f"Column not found: {column}")

    return int(df[column].count())


def calculate_average_order_value(df: pd.DataFrame) -> float:
    """AOV = total revenue / number of unique orders."""

    if df.empty:
        return 0.0

    required = {"order_id", "quantity", "unit_price", "discount"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing columns for AOV: {sorted(missing)}"
        )

    prepared = add_derived_columns(df)
    order_count = prepared["order_id"].nunique()

    if order_count == 0:
        return 0.0

    return float(prepared["revenue"].sum() / order_count)


def aggregate(
    df: pd.DataFrame,
    operation: str,
    column: str | None = None,
) -> Any:
    """Run a supported aggregation."""

    operation = operation.lower().strip()

    if operation in {"sum", "average", "count"}:
        if not column:
            raise ValueError(
                f"A column is required for {operation}."
            )

        prepared = (
            add_derived_columns(df)
            if column == "revenue"
            else df
        )

        if operation == "sum":
            return calculate_sum(prepared, column)

        if operation == "average":
            return calculate_average(prepared, column)

        return calculate_count(prepared, column)

    if operation in {"average_order_value", "aov"}:
        return calculate_average_order_value(df)

    raise ValueError(f"Unsupported aggregation: {operation}")
