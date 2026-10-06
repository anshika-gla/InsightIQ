from typing import Any, Optional

from pydantic import BaseModel, Field


class FilterCondition(BaseModel):
    column: str
    operator: str = "eq"
    value: Any


class QueryPlan(BaseModel):
    operation: str

    metric: Optional[str] = None

    aggregation: Optional[str] = None

    group_by: list[str] = Field(
        default_factory=list
    )

    filters: list[FilterCondition] = Field(
        default_factory=list
    )

    limit: Optional[int] = None

    order: str = "desc"

    numerator: Optional[str] = None

    denominator: Optional[str] = None

    comparison_type: Optional[str] = None

    time_period: Optional[str] = None

    nested: Optional[bool] = False

    explanation: Optional[str] = None


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    query: str
    result: Any
    logic: dict[str, Any]
    confidence: float
    explanation: str