# backend/app/api/schemas.py
from typing import Any, Optional
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(
        min_length=5,
        max_length=500,
        description="Natural language question about the sales data",
        examples=["What are total sales by region?"]
    )


class QueryResponse(BaseModel):
    question: str
    sql: Optional[str]
    chart_type: str
    chart_data: list[dict[str, Any]]
    columns: list[str]
    x_key: Optional[str]
    y_keys: list[str]
    title: str
    row_count: int
    message: Optional[str]


class SampleQuestion(BaseModel):
    question: str
    description: str


class SampleQuestionsResponse(BaseModel):
    questions: list[SampleQuestion]


class HealthResponse(BaseModel):
    status: str
    env: str