# backend/app/core/chart_builder.py
import logging
from typing import Any

logger = logging.getLogger(__name__)

# Keywords that suggest a column contains dates or time periods
DATE_KEYWORDS = ["date", "month", "year", "week", "period", "time", "day"]

# Keywords that suggest a column contains numeric/aggregate values
NUMERIC_KEYWORDS = ["total", "sum", "count", "amount", "revenue",
                    "sales", "avg", "average", "price", "quantity"]


def _is_date_column(col_name: str, values: list) -> bool:
    """Check if a column looks like it contains time/date data."""
    name_lower = col_name.lower()
    if any(kw in name_lower for kw in DATE_KEYWORDS):
        return True
    # Check if values look like dates e.g. "2024-01", "2024-01-15"
    if values and isinstance(values[0], str) and len(values[0]) >= 7:
        return values[0][4:5] == "-"
    return False


def _is_numeric(value: Any) -> bool:
    """Check if a value is numeric."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _detect_chart_type(
    columns: list[str],
    rows: list[dict],
) -> str:
    """
    Decide the best chart type for the data.

    Rules:
    - Line chart: one column looks like dates + one numeric column
    - Pie chart: one text column + one numeric column + fewer than 8 rows
    - Bar chart: one text column + one numeric column
    - Table: everything else
    """
    if not rows or not columns:
        return "table"

    numeric_cols = [
        c for c in columns
        if rows and _is_numeric(rows[0].get(c))
    ]
    text_cols = [c for c in columns if c not in numeric_cols]

    has_one_text = len(text_cols) == 1
    has_one_numeric = len(numeric_cols) == 1

    if has_one_text and has_one_numeric:
        if _is_date_column(text_cols[0], [r[text_cols[0]] for r in rows]):
            return "line"
        if len(rows) <= 7:
            return "pie"
        return "bar"

    if has_one_text and len(numeric_cols) > 1:
        return "bar"  # grouped bar

    return "table"


def build_chart(
    columns: list[str],
    rows: list[dict],
    question: str,
) -> dict:
    """
    Format query results into a chart-ready response.

    Returns a dict the FastAPI route sends directly to React.
    React uses chart_type to decide which Recharts component to render,
    and chart_data as the data prop.
    """
    if not rows:
        return {
            "chart_type": "empty",
            "chart_data": [],
            "columns": columns,
            "x_key": None,
            "y_keys": [],
            "title": question,
            "row_count": 0,
        }

    chart_type = _detect_chart_type(columns, rows)

    numeric_cols = [
        c for c in columns
        if _is_numeric(rows[0].get(c))
    ]
    text_cols = [c for c in columns if c not in numeric_cols]

    # x_key is what goes on the x-axis (or label in pie chart)
    x_key = text_cols[0] if text_cols else columns[0]

    # y_keys are the numeric columns to plot
    y_keys = numeric_cols if numeric_cols else columns[1:]

    # Format numeric values — round floats for cleaner display
    formatted_rows = []
    for row in rows:
        formatted_row = {}
        for col, val in row.items():
            if isinstance(val, float):
                formatted_row[col] = round(val, 2)
            else:
                formatted_row[col] = val
        formatted_rows.append(formatted_row)

    logger.info(
        f"Chart built: type={chart_type}, rows={len(rows)}, "
        f"x={x_key}, y={y_keys}"
    )

    return {
        "chart_type": chart_type,
        "chart_data": formatted_rows,
        "columns": columns,
        "x_key": x_key,
        "y_keys": y_keys,
        "title": question,
        "row_count": len(rows),
    }