from typing import Any

import pandas as pd


def apply_filters(
    df: pd.DataFrame,
    filters: dict[str, Any] | None = None
) -> pd.DataFrame:
    """
    Apply equality-based filters to a DataFrame.

    Example:
        {
            "country": "India",
            "region": "APAC"
        }
    """

    if not filters:
        return df.copy()

    result = df.copy()

    for column, value in filters.items():

        if column not in result.columns:
            raise ValueError(
                f"Cannot filter by unknown column: {column}"
            )

        if isinstance(value, list):
            result = result[result[column].isin(value)]
        else:
            result = result[result[column] == value]

    return result.reset_index(drop=True)