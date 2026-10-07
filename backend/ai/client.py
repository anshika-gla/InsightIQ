import os
import re
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from ai.prompts import build_query_prompt
from ai.schemas import validate_ai_query_plan
from models.query_models import QueryPlan


load_dotenv()


class AIClient:
    def __init__(self) -> None:

        self.api_key = os.getenv(
            "GEMINI_API_KEY"
        )

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

            response = (
                await self.client.aio.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0,
                        response_mime_type="application/json",
                        response_schema=QueryPlan,
                    ),
                )
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            # =================================================
            # GEMINI STRUCTURED RESPONSE
            # =================================================

            if response.parsed is not None:

                return validate_ai_query_plan(
                    response.parsed
                )

            # =================================================
            # GEMINI JSON TEXT RESPONSE
            # =================================================

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

            # =================================================
            # LOCAL FALLBACK
            # =================================================

            try:

                return self._local_fallback_plan(
                    user_query
                )

            except ValueError:

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

        # =================================================
        # TOTAL SALES / TOTAL REVENUE
        # =================================================
        #
        # Supported examples:
        #
        # What are the total sales?
        # What are the total revenue?
        # What is the total revenue?
        # How much revenue did we make in total?
        # How much sales did we make in total?
        # What was our total revenue?
        # What was our overall revenue?
        # Show total revenue
        # Show me the revenue in total
        # Give me overall sales
        #
        # =================================================

        total_revenue_patterns = [
            "total sales",
            "total revenue",
            "sales total",
            "revenue total",
            "overall sales",
            "overall revenue",
            "sales overall",
            "revenue overall",
            "sales in total",
            "revenue in total",
            "total income",
            "income in total",
        ]

        if any(
            phrase in query
            for phrase in total_revenue_patterns
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
        # Natural-language total revenue pattern
        # -------------------------------------------------

        if (
            (
                "how much" in query
                or "what was" in query
                or "what is" in query
                or "what's" in query
            )
            and (
                "revenue" in query
                or "sales" in query
            )
            and (
                "make" in query
                or "made" in query
                or "earn" in query
                or "earned" in query
            )
            and (
                "total" in query
                or "overall" in query
            )
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

        # =================================================
        # TOP N CITIES BY PROFIT
        # =================================================

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
        # Highest / best city by profit
        # -------------------------------------------------

        if (
            (
                "highest profit" in query
                or "highest-profit" in query
                or "most profitable city" in query
                or "best city by profit" in query
            )
            and "city" in query
        ):

            return QueryPlan(
                operation="rank",
                metric="profit",
                group_by=["city"],
                limit=1,
                order="desc",
                explanation=(
                    "Ranked cities by total profit "
                    "and returned the highest-profit city."
                ),
            )

        # =================================================
        # AVERAGE ORDER VALUE BY REGION
        # =================================================

        if (
            (
                "average order value" in query
                or "average order" in query
                or "aov" in query
            )
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

        # =================================================
        # SALES CONTRIBUTION BY CATEGORY
        # =================================================

        if (
            "contribution" in query
            and (
                "category" in query
                or "categories" in query
            )
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

        # =================================================
        # TOP CUSTOMERS IN EACH REGION
        # =================================================

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
        # Alternative customer wording
        # -------------------------------------------------

        customer_match = re.search(
            r"top\s+(\d+)\s+customers?.*region",
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

        # =================================================
        # MONTHLY REVENUE
        # =================================================

        if (
            "monthly revenue" in query
            or "revenue by month" in query
            or "sales by month" in query
            or "monthly sales" in query
            or "revenue each month" in query
            or "sales each month" in query
            or "revenue month by month" in query
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
        # Show revenue over months
        # -------------------------------------------------

        if (
            (
                "revenue" in query
                or "sales" in query
            )
            and (
                "over months" in query
                or "across months" in query
                or "by month" in query
            )
        ):

            return QueryPlan(
                operation="time_analysis",
                metric="revenue",
                aggregation="sum",
                explanation=(
                    "Calculated revenue month by month."
                ),
            )

        # =================================================
        # YEAR OVER YEAR
        # =================================================

        if (
            "year over year" in query
            or "year-over-year" in query
            or "year on year" in query
            or "year-on-year" in query
            or "yoy" in query
            or "y-o-y" in query
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

        # =================================================
        # TARGET COMPARISON
        # =================================================
        #
        # Supports:
        #
        # Compare actual revenue with target
        # Compare actual sales with target
        # Compare revenue against target
        # Compare sales versus target
        # Show target performance for February 2024
        # Which regions missed their target?
        # Which regions met their target?
        #
        # =================================================

        if (
            "target" in query
            and (
                "revenue" in query
                or "sales" in query
                or "actual" in query
            )
            and (
                "compare" in query
                or "comparison" in query
                or "against" in query
                or "versus" in query
                or "vs" in query
                or "missed" in query
                or "miss" in query
                or "met" in query
                or "performance" in query
            )
        ):

            # -------------------------------------------------
            # Detect month and optional year
            # -------------------------------------------------

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

                year = (
                    month_match.group(2)
                )

                if year:

                    time_period = (
                        f"{year}-"
                        f"{month_numbers[month_name]}"
                    )

                else:

                    time_period = (
                        f"2024-"
                        f"{month_numbers[month_name]}"
                    )

            return QueryPlan(
                operation="comparison",
                metric="revenue",
                comparison_type="target",
                time_period=time_period,
                explanation=(
                    "Compared actual revenue with "
                    "target revenue."
                ),
            )

        # =================================================
        # UNSUPPORTED QUERY
        # =================================================

        raise ValueError(
            "The local fallback planner does not "
            "support this query yet."
        )