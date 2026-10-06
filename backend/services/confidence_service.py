
from typing import Any


def calculate_confidence(
    plan: dict[str, Any],
    execution: dict[str, Any],
) -> float:
    """
    Estimate confidence based on plan validation
    and execution outcome.
    """

    if not isinstance(plan, dict):
        return 0.0

    if not isinstance(execution, dict):
        return 0.0

    if "result" not in execution:
        return 0.0

    if execution.get("operation") != plan.get("operation"):
        return 0.3

    # The plan passed validation and execution returned a result.
    return 0.90

