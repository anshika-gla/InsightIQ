from typing import Any

from data.loader import load_sales_data, load_targets_data
from engine.aggregations import (
    add_derived_columns,
    calculate_average_order_value,
    calculate_count,
    calculate_sum,
    calculate_average,
)
from engine.filters import apply_filters
from engine.ranking import rank_by_metric
from engine.comparisons import compare_with_targets
from engine.percentages import calculate_contribution_percentage
from engine.time_analysis import monthly_metric, calculate_yoy_growth
from engine.nested_queries import top_n_within_groups


def _normalize_group_by(group_by):
    if group_by is None:
        return []

    if isinstance(group_by, str):
        return [group_by]

    return list(group_by)


def _normalize_filters(filters):
    if not filters:
        return {}

    filter_dict = {}

    for item in filters:
        if hasattr(item, "model_dump"):
            item = item.model_dump()

        if not isinstance(item, dict):
            raise ValueError("Each filter must be a dictionary.")

        column = item.get("column")
        operator = item.get("operator", "eq")
        value = item.get("value")

        if not column:
            raise ValueError("Filter column is required.")

        if operator != "eq":
            raise ValueError(
                f"Unsupported filter operator: {operator}"
            )

        filter_dict[column] = value

    return filter_dict


def _validate_group_columns(df, group_by):
    for column in group_by:
        if column not in df.columns:
            raise ValueError(
                f"Unknown group-by column: {column}"
            )


def _validate_metric(df, metric):
    supported_metrics = {
        "revenue",
        "profit",
        "quantity",
        "shipping_cost",
        "average_order_value",
        "order_count",
    }

    if metric not in supported_metrics and metric not in df.columns:
        raise ValueError(
            f"Unsupported metric: {metric}"
        )


def execute_query_plan(plan: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(plan, dict):
        if hasattr(plan, "model_dump"):
            plan = plan.model_dump()
        else:
            raise ValueError(
                "Query plan must be a dictionary."
            )

    operation = plan.get("operation")

    if not operation:
        raise ValueError(
            "Query plan must contain an operation."
        )

    metric = plan.get("metric") or "revenue"
    group_by = _normalize_group_by(
        plan.get("group_by")
    )
    limit = plan.get("limit")
    order = plan.get("order", "desc")
    filters = plan.get("filters") or []
    time_period = plan.get("time_period")
    nested = plan.get("nested", False)

    sales_df = load_sales_data()
    targets_df = load_targets_data()

    sales_df = add_derived_columns(sales_df)

    filter_dict = _normalize_filters(filters)

    if filter_dict:
        sales_df = apply_filters(
            sales_df,
            filter_dict
        )

    if group_by:
        _validate_group_columns(
            sales_df,
            group_by
        )

    if operation not in {
        "comparison",
        "percentage",
        "time_analysis"
    }:
        _validate_metric(
            sales_df,
            metric
        )

    if operation == "sum":

        if group_by:
            grouped = sales_df.groupby(
                group_by,
                as_index=False
            )[metric].sum()

            result = grouped.to_dict(
                orient="records"
            )

        else:
            result = calculate_sum(
                sales_df,
                metric
            )

    elif operation == "average":

        if metric == "average_order_value":

            if group_by:

                grouped_results = []

                for group_values, group_df in sales_df.groupby(
                    group_by
                ):

                    if not isinstance(
                        group_values,
                        tuple
                    ):
                        group_values = (
                            group_values,
                        )

                    row = {}

                    for index, column in enumerate(
                        group_by
                    ):
                        row[column] = group_values[index]

                    row["average_order_value"] = (
                        calculate_average_order_value(
                            group_df
                        )
                    )

                    grouped_results.append(row)

                result = grouped_results

            else:
                result = calculate_average_order_value(
                    sales_df
                )

        elif group_by:

            grouped = sales_df.groupby(
                group_by,
                as_index=False
            )[metric].mean()

            result = grouped.to_dict(
                orient="records"
            )

        else:

            result = calculate_average(
                sales_df,
                metric
            )

    elif operation == "count":

        if group_by:

            grouped = (
                sales_df
                .groupby(group_by)
                .size()
                .reset_index(name="count")
            )

            result = grouped.to_dict(
                orient="records"
            )

        else:

            result = calculate_count(
                sales_df,
                metric
            )

    elif operation == "group_by":

        if not group_by:
            raise ValueError(
                "group_by operation requires group_by columns."
            )

        if metric == "average_order_value":

            grouped_results = []

            for group_values, group_df in sales_df.groupby(
                group_by
            ):

                if not isinstance(
                    group_values,
                    tuple
                ):
                    group_values = (
                        group_values,
                    )

                row = {}

                for index, column in enumerate(
                    group_by
                ):
                    row[column] = group_values[index]

                row["average_order_value"] = (
                    calculate_average_order_value(
                        group_df
                    )
                )

                grouped_results.append(row)

            result = grouped_results

        else:

            grouped = sales_df.groupby(
                group_by,
                as_index=False
            )[metric].sum()

            result = grouped.to_dict(
                orient="records"
            )

    elif operation in {
        "rank",
        "top_n"
    }:

        if not group_by:
            raise ValueError(
                "Ranking requires at least one group-by column."
            )

        if limit is None:
            limit = 5

        if not isinstance(
            limit,
            int
        ) or limit <= 0:
            raise ValueError(
                "limit must be a positive integer."
            )

        if nested or len(group_by) >= 2:

            if len(group_by) < 2:
                raise ValueError(
                    "Nested ranking requires two group-by columns."
                )

            group_column = group_by[0]
            item_column = group_by[1]

            output_df = top_n_within_groups(
                sales_df,
                group_column=group_column,
                item_column=item_column,
                metric_column=metric,
                n=limit,
                ascending=(
                    order == "asc"
                )
            )

            result = output_df.to_dict(
                orient="records"
            )

        else:

            output_df = rank_by_metric(
                sales_df,
                group_column=group_by[0],
                metric_column=metric,
                limit=limit,
                ascending=(
                    order == "asc"
                )
            )

            result = output_df.to_dict(
                orient="records"
            )

    elif operation == "percentage":

        if not group_by:
            raise ValueError(
                "Percentage operation requires a group-by column."
            )

        output_df = calculate_contribution_percentage(
            sales_df,
            group_column=group_by[0],
            metric_column=metric
        )

        result = output_df.to_dict(
            orient="records"
        )

    elif operation == "comparison":

        month = (
            time_period
            if time_period
            else None
        )

        output_df = compare_with_targets(
            sales_df,
            targets_df,
            month=month
        )

        result = output_df.to_dict(
            orient="records"
        )

    elif operation == "time_analysis":

        comparison_type = plan.get(
            "comparison_type"
        )

        if comparison_type == "year_over_year":

            result = calculate_yoy_growth(
                sales_df,
                metric=metric
            )

        else:

            output_df = monthly_metric(
                sales_df,
                metric=metric
            )

            result = output_df.to_dict(
                orient="records"
            )

    elif operation == "filter":

        result = sales_df.to_dict(
            orient="records"
        )

    else:

        raise ValueError(
            f"Unsupported operation: {operation}"
        )

    rows_returned = (
        len(result)
        if isinstance(result, list)
        else 1
    )

    return {
        "operation": operation,
        "metric": metric,
        "result": result,
        "rows_returned": rows_returned
    }