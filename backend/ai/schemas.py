from models.query_models import QueryPlan


def validate_ai_query_plan(data: dict) -> QueryPlan:
    """
    Validate and convert an AI-generated dictionary
    into a trusted QueryPlan.

    The deterministic analytics engine will only receive
    validated QueryPlan objects.
    """

    return QueryPlan.model_validate(data)