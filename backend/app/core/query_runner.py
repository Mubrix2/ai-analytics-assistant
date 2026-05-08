# backend/app/core/query_runner.py
import logging
from app.db.database import run_query

logger = logging.getLogger(__name__)

# SQL keywords that should never appear in a SELECT-only system
FORBIDDEN_KEYWORDS = [
    "INSERT", "UPDATE", "DELETE", "DROP", "CREATE",
    "ALTER", "TRUNCATE", "REPLACE", "MERGE",
]


def validate_sql(sql: str) -> None:
    """
    Reject any SQL that is not a SELECT statement.
    Raises ValueError with a clear message if invalid.
    """
    sql_upper = sql.upper().strip()

    if not sql_upper.startswith("SELECT"):
        raise ValueError(
            "Only SELECT queries are permitted. "
            "The generated query was not a SELECT statement."
        )

    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in sql_upper:
            raise ValueError(
                f"Query contains forbidden keyword '{keyword}'. "
                "Only read operations are allowed."
            )


def run_safe_query(sql: str) -> list[dict]:
    """
    Validate then execute a SQL query.
    Returns results as a list of dicts.

    This is the only function the rest of the app
    should use to execute SQL — never call run_query directly.
    """
    validate_sql(sql)

    try:
        results = run_query(sql)
        logger.info(f"Query returned {len(results)} rows")
        return results
    except Exception as e:
        logger.error(f"Query execution failed: {e}")
        raise ValueError(f"Query failed to execute: {str(e)}")