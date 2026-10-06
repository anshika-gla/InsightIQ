from typing import Any

from data.loader import load_sales_data, load_targets_data


ALLOWED_OPERATIONS = {
    "sum",
    "average",
    "count",
    "group_by",
    "filter",
    "rank",
    "percentage",
    "comparison",
    "top_n",
    "time_analysis",
}


def validate_query_plan(plan: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []

    if not isinstance(plan, dict):
        return False, ["Query plan must be a dictionary."]

    operation = plan.get("operation")

    if operation and operation not in ALLOWED_OPERATIONS:
        errors.append(
            f"Unsupported operation: {operation}"
        )

    try:
        sales_df = load_sales_data()
        targets_df = load_targets_data()

        valid_sales_columns = set(sales_df.columns)
        valid_target_columns = set(targets_df.columns)

        referenced_columns = plan.get("columns", [])

        if isinstance(referenced_columns, list):
            for column in referenced_columns:
                if (
                    column not in valid_sales_columns
                    and column not in valid_target_columns
                ):
                    errors.append(
                        f"Unknown column: {column}"
                    )

        group_by = plan.get("group_by", [])

        if isinstance(group_by, str):
            group_by = [group_by]

        if isinstance(group_by, list):
            for column in group_by:
                if column not in valid_sales_columns:
                    errors.append(
                        f"Invalid group-by column: {column}"
                    )

    except Exception as exc:
        errors.append(
            f"Dataset validation failed: {str(exc)}"
        )

    return len(errors) == 0, errors