from typing import Any

import pandas as pd

from data.loader import load_sales_data, load_targets_data
from engine.filters import apply_filters
from engine.aggregations import aggregate, add_derived_columns
from engine.ranking import rank_by_metric, rank_within_groups
from engine.percentages import calculate_contribution_percentage
from engine.comparisons import compare_with_targets
from engine.time_analysis import monthly_metric, calculate_yoy_growth
from engine.nested_queries import top_n_within_groups


def execute_query_plan(
    plan: dict[str, Any]
) -> dict[str, Any]:
    """Execute a validated analytics query plan."""

    operation = plan.get("operation")

    metric = plan.get("metric") or "revenue"

    group_by = plan.get("group_by") or []

    # Make sure group_by is always a list.
    if isinstance(group_by, str):
        group_by = [group_by]

    limit = plan.get("limit")

    filters = plan.get("filters") or []

    # =========================================================
    # LOAD DATA
    # =========================================================

    sales_df = add_derived_columns(
        load_sales_data()
    )

    targets_df = load_targets_data()

    # =========================================================
    # APPLY FILTERS
    # =========================================================

    filter_dict = {}

    for item in filters:

        if hasattr(item, "model_dump"):
            item = item.model_dump()

        if not isinstance(item, dict):
            raise ValueError(
                "Each filter must be a dictionary."
            )

        column = item.get("column")

        operator = item.get(
            "operator",
            "eq"
        )

        value = item.get("value")

        if not column:
            raise ValueError(
                "Filter column is required."
            )

        if operator != "eq":
            raise ValueError(
                f"Unsupported filter operator: {operator}"
            )

        filter_dict[column] = value

    sales_df = apply_filters(
        sales_df,
        filter_dict
    )

    # =========================================================
    # TARGET COMPARISON
    # =========================================================

    if operation == "comparison":

        result = compare_with_targets(
            sales_df,
            targets_df,
            month=plan.get(
                "time_period"
            ),
        )

    # =========================================================
    # PERCENTAGE CONTRIBUTION
    # =========================================================

    elif operation == "percentage":

        if not group_by:
            raise ValueError(
                "A group_by column is required "
                "for percentages."
            )

        result = calculate_contribution_percentage(
            sales_df,
            group_by[0],
            metric,
        )

    # =========================================================
    # RANKING / TOP-N
    # =========================================================

    elif operation in {
        "rank",
        "top_n",
    }:

        if not group_by:
            raise ValueError(
                "A group_by column is required "
                "for ranking."
            )

        ascending = (
            plan.get(
                "order",
                "desc"
            )
            == "asc"
        )

        # -----------------------------------------------------
        # Ranking within groups
        # -----------------------------------------------------

        if len(group_by) >= 2:

            if plan.get("nested"):

                result = top_n_within_groups(
                    sales_df,
                    group_column=group_by[0],
                    item_column=group_by[1],
                    metric_column=metric,
                    n=limit or 3,
                    ascending=ascending,
                )

            else:

                result = rank_within_groups(
                    sales_df,
                    group_column=group_by[0],
                    item_column=group_by[1],
                    metric_column=metric,
                    ascending=ascending,
                    limit=limit,
                )

        # -----------------------------------------------------
        # Normal ranking
        # -----------------------------------------------------

        else:

            result = rank_by_metric(
                sales_df,
                group_column=group_by[0],
                metric_column=metric,
                ascending=ascending,
                limit=limit,
            )

    # =========================================================
    # TIME ANALYSIS
    # =========================================================

    elif operation == "time_analysis":

        if (
            plan.get(
                "comparison_type"
            )
            == "year_over_year"
        ):

            result = calculate_yoy_growth(
                sales_df,
                metric_column=metric,
            )

        else:

            result = monthly_metric(
                sales_df,
                metric_column=metric,
                aggregation=(
                    plan.get(
                        "aggregation"
                    )
                    or "sum"
                ),
            )

    # =========================================================
    # GROUP BY
    # =========================================================

    elif operation == "group_by":

        if not group_by:
            raise ValueError(
                "A group_by column is required."
            )

        # =====================================================
        # AVERAGE ORDER VALUE BY GROUP
        # =====================================================

        if (
            plan.get(
                "aggregation"
            )
            in {
                "average_order_value",
                "aov",
            }
        ):

            required_columns = {
                "order_id",
                "revenue",
            }

            missing_columns = (
                required_columns
                - set(sales_df.columns)
            )

            if missing_columns:
                raise ValueError(
                    "Missing columns required "
                    f"for AOV: "
                    f"{sorted(missing_columns)}"
                )

            grouped = (
                sales_df
                .groupby(group_by)
                .agg(
                    total_revenue=(
                        "revenue",
                        "sum",
                    ),
                    order_count=(
                        "order_id",
                        "nunique",
                    ),
                )
                .reset_index()
            )

            grouped[
                "average_order_value"
            ] = 0.0

            valid_orders = (
                grouped[
                    "order_count"
                ]
                != 0
            )

            grouped.loc[
                valid_orders,
                "average_order_value",
            ] = (
                grouped.loc[
                    valid_orders,
                    "total_revenue",
                ]
                / grouped.loc[
                    valid_orders,
                    "order_count",
                ]
            )

            result = grouped[
                group_by
                + [
                    "average_order_value"
                ]
            ]

            result = result.sort_values(
                "average_order_value",
                ascending=(
                    plan.get(
                        "order",
                        "desc"
                    )
                    == "asc"
                ),
            )

            if limit:
                result = result.head(
                    limit
                )

            result = result.reset_index(
                drop=True
            )

        # =====================================================
        # NORMAL GROUPED SUM
        # =====================================================

        else:

            missing = [
                column
                for column in (
                    group_by
                    + [metric]
                )
                if column
                not in sales_df.columns
            ]

            if missing:
                raise ValueError(
                    "Unknown columns: "
                    f"{sorted(set(missing))}"
                )

            result = (
                sales_df
                .groupby(
                    group_by,
                    as_index=False,
                )[metric]
                .sum()
                .sort_values(
                    metric,
                    ascending=(
                        plan.get(
                            "order",
                            "desc"
                        )
                        == "asc"
                    ),
                )
            )

            if limit:
                result = result.head(
                    limit
                )

            result = result.reset_index(
                drop=True
            )

    # =========================================================
    # SCALAR AGGREGATIONS
    # =========================================================

    elif operation in {
        "sum",
        "average",
        "count",
    }:

        aggregation = (
            plan.get(
                "aggregation"
            )
            or operation
        )

        result = aggregate(
            sales_df,
            aggregation,
            metric,
        )

    # =========================================================
    # UNSUPPORTED OPERATION
    # =========================================================

    else:

        raise ValueError(
            f"Unsupported operation: {operation}"
        )

    # =========================================================
    # CONVERT RESULT TO JSON-FRIENDLY FORMAT
    # =========================================================

    if isinstance(
        result,
        pd.DataFrame,
    ):

        output = result.to_dict(
            orient="records"
        )

    elif isinstance(
        result,
        pd.Series,
    ):

        output = result.to_dict()

    elif hasattr(
        result,
        "item",
    ):

        output = result.item()

    else:

        output = result

    # =========================================================
    # FINAL RESPONSE
    # =========================================================

    return {
        "operation": operation,
        "metric": metric,
        "result": output,
        "rows_returned": (
            len(output)
            if isinstance(
                output,
                list,
            )
            else 1
        ),
    }