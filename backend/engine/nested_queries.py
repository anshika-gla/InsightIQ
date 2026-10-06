from typing import Optional

import pandas as pd


def top_n_within_groups(
    df: pd.DataFrame,
    group_column: str,
    item_column: str,
    metric_column: str,
    n: int = 3,
    ascending: bool = False
) -> pd.DataFrame:
    """
    Return the top N items within each group
    based on an aggregated metric.

    Example:
        Revenue of top 3 customers per region.
    """

    if n <= 0:
        raise ValueError("n must be greater than zero.")

    required_columns = {
        group_column,
        item_column,
        metric_column
    }

    missing_columns = (
        required_columns - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            f"Missing columns: {sorted(missing_columns)}"
        )

    grouped = (
        df.groupby(
            [group_column, item_column],
            as_index=False
        )[metric_column]
        .sum()
    )

    grouped["_rank"] = (
        grouped.groupby(group_column)[metric_column]
        .rank(
            method="first",
            ascending=ascending
        )
    )

    result = grouped[
        grouped["_rank"] <= n
    ].copy()

    return (
        result
        .sort_values(
            [group_column, "_rank"]
        )
        .reset_index(drop=True)
    )


def top_n_customers_per_region(
    df: pd.DataFrame,
    n: int = 3
) -> pd.DataFrame:
    """
    Convenience function for:
    'Top N customers by revenue per region.'
    """

    return top_n_within_groups(
        df=df,
        group_column="region",
        item_column="customer_id",
        metric_column="revenue",
        n=n,
        ascending=False
    )