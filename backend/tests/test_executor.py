import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.executor import execute_query_plan


def test_total_sales():
    plan = {
        "operation": "sum",
        "metric": "revenue"
    }

    response = execute_query_plan(plan)

    assert response["operation"] == "sum"
    assert response["metric"] == "revenue"
    assert response["result"] == pytest.approx(6134.4)


def test_average_order_value():
    plan = {
        "operation": "average",
        "metric": "average_order_value"
    }

    response = execute_query_plan(plan)

    assert response["operation"] == "average"
    assert response["metric"] == "average_order_value"
    assert response["result"] == pytest.approx(613.44)


def test_top_cities_by_profit():
    plan = {
        "operation": "top_n",
        "metric": "profit",
        "group_by": ["city"],
        "limit": 2,
        "order": "desc"
    }

    response = execute_query_plan(plan)

    result = response["result"]

    assert len(result) == 2
    assert result[0]["city"] == "New York"
    assert result[0]["profit"] == pytest.approx(200)
    assert result[1]["city"] == "San Francisco"
    assert result[1]["profit"] == pytest.approx(180)


def test_top_customers_within_regions():
    plan = {
        "operation": "top_n",
        "metric": "revenue",
        "group_by": ["region", "customer_id"],
        "limit": 3,
        "order": "desc",
        "nested": True
    }

    response = execute_query_plan(plan)

    result = response["result"]

    assert len(result) == 9

    regions = {
        row["region"]
        for row in result
    }

    assert regions == {
        "APAC",
        "EMEA",
        "NA"
    }


def test_target_comparison():
    plan = {
        "operation": "comparison",
        "metric": "revenue",
        "time_period": "2024-02"
    }

    response = execute_query_plan(plan)

    result = response["result"]

    assert len(result) == 3

    for row in result:
        assert "actual_revenue" in row
        assert "target_revenue" in row
        assert "difference" in row
        assert "achievement_percentage" in row
        assert "target_met" in row