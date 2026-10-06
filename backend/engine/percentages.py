import pandas as pd


def calculate_contribution_percentage(
    df: pd.DataFrame,
    group_column: str,
    metric_column: str
) -> pd.DataFrame:
    """
    Calculate each group's percentage contribution
    to the total metric.

    Example:
        Revenue contribution by product_category.
    """

    if group_column not in df.columns:
        raise ValueError(
            f"Group column not found: {group_column}"
        )

    if metric_column not in df.columns:
        raise ValueError(
            f"Metric column not found: {metric_column}"
        )

    grouped = (
        df.groupby(group_column, as_index=False)[metric_column]
        .sum()
    )

    total = grouped[metric_column].sum()

    if total == 0:
        grouped["contribution_percentage"] = 0.0
    else:
        grouped["contribution_percentage"] = (
            grouped[metric_column] / total * 100
        )

    return grouped