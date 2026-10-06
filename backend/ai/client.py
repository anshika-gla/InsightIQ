import os
import re

from dotenv import load_dotenv
from google import genai
from google.genai import types

from ai.prompts import build_query_prompt
from ai.schemas import validate_ai_query_plan
from models.query_models import QueryPlan

load_dotenv()


class AIClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash",
        )

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=self.api_key
        )

    async def generate_query_plan(
        self,
        user_query: str,
        schema_description: str = "",
    ) -> QueryPlan:

        prompt = build_query_prompt(
            user_query,
            schema_description,
        )

        try:
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0,
                    response_mime_type="application/json",
                    response_schema=QueryPlan,
                ),
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            # Gemini structured response
            if response.parsed is not None:
                return validate_ai_query_plan(
                    response.parsed
                )

            # Fallback if Gemini returned JSON text
            import json

            parsed_data = json.loads(
                response.text
            )

            return validate_ai_query_plan(
                parsed_data
            )

        except Exception as error:
            error_message = str(error)

            print(
                f"Gemini unavailable: {error_message}"
            )

            print(
                "Using local fallback planner."
            )

            # -------------------------------------------------
            # IMPORTANT:
            # Gemini 429 / 503 / timeout / temporary failure
            # should NOT break the application.
            # -------------------------------------------------

            try:
                return self._local_fallback_plan(
                    user_query
                )

            except ValueError:
                # If local planner also does not understand
                # the query, return the original Gemini error
                # so the user gets a meaningful message.
                raise RuntimeError(
                    "The AI planner is temporarily unavailable "
                    "and the local planner does not support "
                    "this query yet."
                ) from error

    def _local_fallback_plan(
        self,
        user_query: str,
    ) -> QueryPlan:

        query = user_query.lower().strip()

        # -------------------------------------------------
        # TOTAL SALES / TOTAL REVENUE
        # -------------------------------------------------

        if (
            "total sales" in query
            or "total revenue" in query
            or "sales total" in query
        ):
            return QueryPlan(
                operation="sum",
                metric="revenue",
                aggregation="sum",
                explanation=(
                    "Calculated total revenue from "
                    "the sales data."
                ),
            )

        # -------------------------------------------------
        # TOP N CITIES BY PROFIT
        # -------------------------------------------------

        city_match = re.search(
            r"top\s+(\d+)\s+cities?.*profit",
            query,
        )

        if city_match:
            limit = int(
                city_match.group(1)
            )

            return QueryPlan(
                operation="rank",
                metric="profit",
                group_by=["city"],
                limit=limit,
                order="desc",
                explanation=(
                    f"Ranked cities by total profit "
                    f"and returned the top {limit}."
                ),
            )

        # -------------------------------------------------
        # AVERAGE ORDER VALUE BY REGION
        # -------------------------------------------------

        if (
            "average order value" in query
            and "region" in query
        ):
            return QueryPlan(
                operation="group_by",
                metric="revenue",
                aggregation="average_order_value",
                group_by=["region"],
                order="desc",
                explanation=(
                    "Calculated average order value "
                    "for each region."
                ),
            )

        # -------------------------------------------------
        # SALES CONTRIBUTION BY CATEGORY
        # -------------------------------------------------

        if (
            "contribution" in query
            and "category" in query
        ):
            return QueryPlan(
                operation="percentage",
                metric="revenue",
                group_by=[
                    "product_category"
                ],
                order="desc",
                explanation=(
                    "Calculated each category's "
                    "contribution to total revenue."
                ),
            )

        # -------------------------------------------------
        # TOP CUSTOMERS IN EACH REGION
        # -------------------------------------------------

        customer_match = re.search(
            r"top\s+(\d+)\s+customers?.*each\s+region",
            query,
        )

        if customer_match:
            limit = int(
                customer_match.group(1)
            )

            return QueryPlan(
                operation="top_n",
                metric="revenue",
                group_by=[
                    "region",
                    "customer_id",
                ],
                limit=limit,
                order="desc",
                nested=True,
                explanation=(
                    f"Ranked customers by revenue "
                    f"within each region and returned "
                    f"the top {limit}."
                ),
            )

        # -------------------------------------------------
        # MONTHLY REVENUE
        # -------------------------------------------------

        if (
            "monthly revenue" in query
            or "revenue by month" in query
            or "sales by month" in query
        ):
            return QueryPlan(
                operation="time_analysis",
                metric="revenue",
                aggregation="sum",
                explanation=(
                    "Calculated revenue month by month."
                ),
            )

        # -------------------------------------------------
        # YOY
        # -------------------------------------------------

        if (
            "year over year" in query
            or "year-over-year" in query
            or "yoy" in query
        ):
            return QueryPlan(
                operation="time_analysis",
                metric="revenue",
                comparison_type="year_over_year",
                explanation=(
                    "Calculated year-over-year revenue "
                    "growth when sufficient historical "
                    "data is available."
                ),
            )

        # -------------------------------------------------
        # TARGET COMPARISON
        # -------------------------------------------------

        if (
            "target" in query
            and (
                "missed" in query
                or "miss" in query
                or "met" in query
            )
        ):
            month_match = re.search(
                r"(january|february|march|april|may|june|"
                r"july|august|september|october|november|december)"
                r"(?:\s+(\d{4}))?",
                query,
            )

            month_numbers = {
                "january": "01",
                "february": "02",
                "march": "03",
                "april": "04",
                "may": "05",
                "june": "06",
                "july": "07",
                "august": "08",
                "september": "09",
                "october": "10",
                "november": "11",
                "december": "12",
            }

            time_period = None

            if month_match:
                month_name = (
                    month_match.group(1)
                )

                year = month_match.group(2)

                if year:
                    time_period = (
                        f"{year}-"
                        f"{month_numbers[month_name]}"
                    )
                else:
                    # Dataset is 2024, so use 2024
                    time_period = (
                        f"2024-"
                        f"{month_numbers[month_name]}"
                    )

            return QueryPlan(
                operation="comparison",
                metric="revenue",
                time_period=time_period,
                explanation=(
                    "Compared actual revenue with "
                    "target revenue."
                ),
            )

        # -------------------------------------------------
        # UNSUPPORTED QUERY
        # -------------------------------------------------

        raise ValueError(
            "The local fallback planner does not "
            "support this query yet."
        )