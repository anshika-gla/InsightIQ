from typing import Optional

import pandas as pd


def rank_by_metric(
    df: pd.DataFrame,
    group_column: str,
    metric_column: str,
    ascending: bool = False,
    limit: Optional[int] = None
) -> pd.DataFrame:
    """
    Rank groups by an aggregated metric.

    Example:
        Top 2 cities by profit
    """

    if group_column not in df.columns:
        raise ValueError(
            f"Group column not found: {group_column}"
        )

    if metric_column not in df.columns:
        raise ValueError(
            f"Metric column not found: {metric_column}"
        )

    result = (
        df.groupby(group_column, as_index=False)[metric_column]
        .sum()
        .sort_values(
            by=metric_column,
            ascending=ascending
        )
    )

    if limit is not None:
        result = result.head(limit)

    return result.reset_index(drop=True)


def rank_within_groups(
    df: pd.DataFrame,
    group_column: str,
    item_column: str,
    metric_column: str,
    ascending: bool = False,
    limit: Optional[int] = None
) -> pd.DataFrame:
    """
    Rank items within each group.

    Example:
        Top product in each region
    """

    required_columns = {
        group_column,
        item_column,
        metric_column
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )

    aggregated = (
        df.groupby(
            [group_column, item_column],
            as_index=False
        )[metric_column]
        .sum()
    )

    aggregated["_rank"] = (
        aggregated.groupby(group_column)[metric_column]
        .rank(
            method="first",
            ascending=ascending
        )
    )

    if limit is not None:
        aggregated = aggregated[
            aggregated["_rank"] <= limit
        ]

    return (
        aggregated
        .sort_values(
            [group_column, "_rank"]
        )
        .reset_index(drop=True)
    )