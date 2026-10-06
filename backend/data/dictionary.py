from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "dataset"


def load_data_dictionary() -> dict:
    file_path = DATASET_DIR / "data_dictionary.json"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Data dictionary not found: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


BUSINESS_SYNONYMS = {
    "sales": "revenue",
    "sale": "revenue",
    "income": "revenue",
    "earnings": "profit",
    "order": "order_count",
    "orders": "order_count",
    "number of orders": "order_count",
    "count of orders": "order_count",
    "aov": "average_order_value",
    "average order value": "average_order_value",
    "avg order value": "average_order_value",
}


TIME_SYNONYMS = {
    "yoy": "year_over_year",
    "year over year": "year_over_year",
    "last month": "previous_calendar_month",
    "previous month": "previous_calendar_month",
    "this month": "current_calendar_month",
    "this quarter": "current_quarter",
    "last quarter": "previous_quarter",
}


def normalize_business_term(term: str) -> str:
    normalized = term.strip().lower()

    return BUSINESS_SYNONYMS.get(
        normalized,
        normalized
    )


def normalize_time_term(term: str) -> str:
    normalized = term.strip().lower()

    return TIME_SYNONYMS.get(
        normalized,
        normalized
    )