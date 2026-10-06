
from typing import Any

from ai.client import AIClient
from engine.validator import validate_query_plan
from engine.executor import execute_query_plan
from services.confidence_service import calculate_confidence
from services.explanation_service import generate_explanation


class QueryService:
    def __init__(self) -> None:
        self.ai_client = AIClient()

    async def process_query(self, user_query: str) -> dict[str, Any]:
        if not user_query or not user_query.strip():
            raise ValueError("Please enter an analytics question.")

        query = user_query.strip()

        # Step 1: Generate the plan using AI.
        plan = await self.ai_client.generate_query_plan(query)
        plan_data = plan.model_dump()

        # Step 2: Validate the plan.
        is_valid, errors = validate_query_plan(plan_data)

        if not is_valid:
            raise ValueError(
                "Invalid query plan: " + "; ".join(errors)
            )

        # Step 3: Execute the analytics plan.
        execution = execute_query_plan(plan_data)

        # Step 4: Calculate confidence and explanation.
        confidence = calculate_confidence(plan_data, execution)
        explanation = generate_explanation(plan_data, execution)

        return {
            "query": query,
            "status": "success",
            "plan": plan_data,
            "result": execution["result"],
            "logic": {
                "operation": plan_data.get("operation"),
                "metric": plan_data.get("metric"),
                "aggregation": plan_data.get("aggregation"),
                "group_by": plan_data.get("group_by", []),
                "filters": [
                    item.model_dump()
                    for item in plan.filters
                ],
                "time_period": plan_data.get("time_period"),
                "rows_returned": execution["rows_returned"],
            },
            "confidence": confidence,
            "explanation": explanation,
        }

