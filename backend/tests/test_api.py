# backend/tests/test_api.py
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import create_app

client = TestClient(create_app())


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_get_sample_questions():
    response = client.get("/api/v1/query/samples")
    assert response.status_code == 200
    data = response.json()
    assert len(data["questions"]) > 0
    assert "question" in data["questions"][0]


def test_question_too_short():
    response = client.post(
        "/api/v1/query/ask",
        json={"question": "hi"},
    )
    assert response.status_code == 422


@patch("app.api.routes.query.answer_question")
def test_ask_question_success(mock_answer):
    mock_answer.return_value = {
        "sql": "SELECT name, SUM(amount) FROM sales GROUP BY name",
        "chart_type": "bar",
        "chart_data": [{"name": "Lagos", "total": 5000000}],
        "columns": ["name", "total"],
        "x_key": "name",
        "y_keys": ["total"],
        "title": "Sales by region",
        "row_count": 1,
        "message": None,
    }
    response = client.post(
        "/api/v1/query/ask",
        json={"question": "What are total sales by region?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["chart_type"] == "bar"
    assert data["sql"] is not None
    assert data["row_count"] == 1