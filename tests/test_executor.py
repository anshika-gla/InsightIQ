
from engine.executor import execute_query_plan


tests = [
    {
        "name": "Total revenue",
        "plan": {
            "operation": "sum",
            "metric": "revenue",
            "aggregation": "sum",
        },
    },
    {
        "name": "Top 2 cities by profit",
        "plan": {
            "operation": "rank",
            "metric": "profit",
            "group_by": ["city"],
            "limit": 2,
            "order": "desc",
        },
    },
    {
        "name": "Monthly revenue",
        "plan": {
            "operation": "time_analysis",
            "metric": "revenue",
            "aggregation": "sum",
        },
    },
    {
        "name": "Year-over-year growth",
        "plan": {
            "operation": "time_analysis",
            "metric": "revenue",
            "comparison_type": "year_over_year",
        },
    },
]


for test in tests:
    print(f"\n--- {test['name']} ---")

    try:
        response = execute_query_plan(test["plan"])
        print(response)
    except Exception as error:
        print(f"FAILED: {type(error).__name__}: {error}")

