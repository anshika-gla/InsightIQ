import pandas as pd


def compare_with_targets(
    sales_df: pd.DataFrame,
    targets_df: pd.DataFrame,
    month: str | None = None
) -> pd.DataFrame:
    """
    Compare actual revenue against target revenue by region.

    Parameters
    ----------
    sales_df:
        Sales dataset.

    targets_df:
        Target dataset.

    month:
        Optional month in YYYY-MM format.
    """

    sales = sales_df.copy()
    targets = targets_df.copy()

    # Calculate revenue
    sales["revenue"] = (
        sales["quantity"]
        * sales["unit_price"]
        * (1 - sales["discount"])
    )

    # Convert order date
    sales["order_date"] = pd.to_datetime(
        sales["order_date"]
    )

    # Create YYYY-MM month
    sales["month"] = sales["order_date"].dt.strftime(
        "%Y-%m"
    )

    # Filter both datasets when a month is provided
    if month is not None:
        sales = sales[
            sales["month"] == month
        ].copy()

        targets = targets[
            targets["month"] == month
        ].copy()

    # Calculate actual revenue by region
    actual = (
        sales.groupby("region", as_index=False)["revenue"]
        .sum()
        .rename(
            columns={
                "revenue": "actual_revenue"
            }
        )
    )

    # Start from targets so every target region is preserved
    result = targets.merge(
        actual,
        on="region",
        how="left"
    )

    # Regions with no sales get zero actual revenue
    result["actual_revenue"] = (
        result["actual_revenue"]
        .fillna(0)
    )

    result["target_revenue"] = (
        result["target_revenue"]
        .fillna(0)
    )

    # Difference between actual and target
    result["difference"] = (
        result["actual_revenue"]
        - result["target_revenue"]
    )

    # Achievement percentage
    result["achievement_percentage"] = 0.0

    valid_targets = (
        result["target_revenue"] != 0
    )

    result.loc[
        valid_targets,
        "achievement_percentage"
    ] = (
        result.loc[
            valid_targets,
            "actual_revenue"
        ]
        / result.loc[
            valid_targets,
            "target_revenue"
        ]
        * 100
    )

    # Target status
    result["target_met"] = (
        result["actual_revenue"]
        >= result["target_revenue"]
    )

    return result.sort_values(
        "region"
    ).reset_index(drop=True)