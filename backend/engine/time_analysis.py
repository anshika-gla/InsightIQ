from typing import Any

import pandas as pd


def prepare_time_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare sales data for time-based analysis.

    Adds:
    - year
    - month
    - year_month
    """

    result = df.copy()

    if "order_date" not in result.columns:
        raise ValueError(
            "order_date column is required for time analysis."
        )

    result["order_date"] = pd.to_datetime(
        result["order_date"]
    )

    result["year"] = result["order_date"].dt.year
    result["month"] = result["order_date"].dt.month

    result["year_month"] = (
        result["order_date"]
        .dt.to_period("M")
        .astype(str)
    )

    return result


def monthly_metric(
    df: pd.DataFrame,
    metric_column: str,
    aggregation: str = "sum"
) -> pd.DataFrame:
    """
    Calculate a metric month by month.
    """

    result = prepare_time_data(df)

    if metric_column not in result.columns:
        raise ValueError(
            f"Metric column not found: {metric_column}"
        )

    if aggregation == "sum":
        output = (
            result.groupby("year_month", as_index=False)[metric_column]
            .sum()
        )

    elif aggregation == "average":
        output = (
            result.groupby("year_month", as_index=False)[metric_column]
            .mean()
        )

    elif aggregation == "count":
        output = (
            result.groupby("year_month", as_index=False)[metric_column]
            .count()
        )

    else:
        raise ValueError(
            f"Unsupported aggregation: {aggregation}"
        )

    return output.sort_values(
        "year_month"
    ).reset_index(drop=True)


def calculate_yoy_growth(
    df: pd.DataFrame,
    metric_column: str
) -> dict[str, Any]:
    """
    Calculate year-over-year growth.

    If fewer than two years are available, return a
    graceful insufficient-data response instead of
    fabricating a YoY value.
    """

    result = prepare_time_data(df)

    if metric_column not in result.columns:
        raise ValueError(
            f"Metric column not found: {metric_column}"
        )

    years = sorted(
        result["year"].dropna().unique().tolist()
    )

    if len(years) < 2:
        return {
            "status": "insufficient_data",
            "message": (
                "Year-over-year growth cannot be calculated "
                "because the dataset contains fewer than "
                "two years of historical data."
            ),
            "available_years": years
        }

    yearly = (
        result.groupby("year")[metric_column]
        .sum()
        .sort_index()
    )

    current_year = years[-1]
    previous_year = years[-2]

    current_value = float(
        yearly.loc[current_year]
    )

    previous_value = float(
        yearly.loc[previous_year]
    )

    if previous_value == 0:
        growth = None
    else:
        growth = (
            (current_value - previous_value)
            / previous_value
            * 100
        )

    return {
        "status": "success",
        "current_year": int(current_year),
        "previous_year": int(previous_year),
        "current_value": current_value,
        "previous_value": previous_value,
        "growth_percentage": growth
    }