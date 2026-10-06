
from typing import Any


def generate_explanation(
    plan: dict[str, Any],
    execution: dict[str, Any],
) -> str:
    """Generate a human-readable explanation of the analytics result."""

    operation = plan.get("operation", "analysis")
    metric = plan.get("metric", "revenue")
    group_by = plan.get("group_by") or []
    filters = plan.get("filters") or []

    if operation == "time_analysis":
        if plan.get("comparison_type") == "year_over_year":
            result = execution.get("result", {})

            if (
                isinstance(result, dict)
                and result.get("status") == "insufficient_data"
            ):
                return result.get(
                    "message",
                    "There is not enough historical data to calculate year-over-year growth.",
                )

            return (
                f"Year-over-year analysis was performed for {metric}. "
                "Review the result for the calculated growth."
            )

        return (
            f"Monthly {metric} was calculated using "
            f"{plan.get('aggregation') or 'sum'} aggregation."
        )

    if operation == "comparison":
        return (
            "Actual revenue was compared with the target revenue. "
            "The result includes the difference and target achievement."
        )

    if operation == "percentage":
        group = group_by[0] if group_by else "selected groups"
        return (
            f"The contribution percentage of {metric} was calculated "
            f"for each {group} relative to the total."
        )

    if operation in {"rank", "top_n"}:
        group = group_by[0] if group_by else "selected category"
        return (
            f"Results were ranked by {metric} in descending or "
            f"requested order, grouped by {group} where applicable."
        )

    if operation == "group_by":
        return (
            f"{metric} was aggregated for each combination of "
            f"{', '.join(group_by)}."
        )

    if operation in {"sum", "average", "count"}:
        aggregation = plan.get("aggregation") or operation
        message = f"The {aggregation} of {metric} was calculated."

        if filters:
            message += " The requested filters were applied."

        return message

    return (
        f"The query was processed using the {operation} operation. "
        "See the result and logic fields for details."
    )

