# backend/app/services/analytics_service.py
import logging
from app.core.sql_generator import generate_sql
from app.core.query_runner import run_safe_query
from app.core.chart_builder import build_chart

logger = logging.getLogger(__name__)


def answer_question(question: str) -> dict:
    """
    Full pipeline: question → SQL → data → chart response.

    Args:
        question: Natural language question from the user

    Returns:
        Dict containing sql, chart_type, chart_data, and metadata
    """
    if not question.strip():
        raise ValueError("Question cannot be empty")

    # Step 1 — Generate SQL
    sql = generate_sql(question)

    # Handle when LLM says it cannot answer
    if sql.strip().upper() == "CANNOT_ANSWER":
        return {
            "sql": None,
            "chart_type": "error",
            "chart_data": [],
            "columns": [],
            "x_key": None,
            "y_keys": [],
            "title": question,
            "row_count": 0,
            "message": (
                "This question cannot be answered with the available data. "
                "Try asking about sales, revenue, regions, or products."
            ),
        }

    # Step 2 — Run SQL safely
    rows = run_safe_query(sql)
    columns = list(rows[0].keys()) if rows else []

    # Step 3 — Build chart response
    chart = build_chart(
        columns=columns,
        rows=rows,
        question=question,
    )

    return {
        "sql": sql,
        "message": None,
        **chart,
    }