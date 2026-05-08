# backend/tests/test_sql_generator.py
import pytest
from unittest.mock import patch, MagicMock
from app.core.query_runner import validate_sql, run_safe_query


def test_validate_sql_accepts_select():
    # Should not raise
    validate_sql("SELECT name, amount FROM sales")


def test_validate_sql_rejects_delete():
    with pytest.raises(ValueError, match="Only SELECT"):
        validate_sql("DELETE FROM sales")


def test_validate_sql_rejects_drop():
    with pytest.raises(ValueError, match="forbidden keyword"):
        validate_sql("SELECT * FROM sales; DROP TABLE sales")


def test_validate_sql_rejects_insert():
    with pytest.raises(ValueError, match="Only SELECT"):
        validate_sql("INSERT INTO sales VALUES (1, 2, 3, 100, '2024-01-01')")


def test_validate_sql_rejects_update():
    with pytest.raises(ValueError, match="Only SELECT"):
        validate_sql("UPDATE sales SET amount = 0")


@patch("app.core.query_runner.run_query")
def test_run_safe_query_success(mock_run):
    mock_run.return_value = [{"region": "Lagos", "total": 5000000}]
    result = run_safe_query("SELECT region, SUM(amount) as total FROM sales")
    assert len(result) == 1
    assert result[0]["region"] == "Lagos"


@patch("app.core.query_runner.run_query")
def test_run_safe_query_raises_on_db_error(mock_run):
    mock_run.side_effect = Exception("table not found")
    with pytest.raises(ValueError, match="Query failed"):
        run_safe_query("SELECT * FROM nonexistent_table")