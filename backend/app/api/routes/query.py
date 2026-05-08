# backend/app/api/routes/query.py
import logging
from fastapi import APIRouter, HTTPException, status
from app.api.schemas import (
    QueryRequest,
    QueryResponse,
    SampleQuestion,
    SampleQuestionsResponse,
)
from app.services.analytics_service import answer_question

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/query", tags=["Query"])

# Sample questions shown in the UI so users know what to ask
SAMPLE_QUESTIONS = [
    SampleQuestion(
        question="What are total sales by region?",
        description="Bar chart of revenue per region"
    ),
    SampleQuestion(
        question="Show monthly revenue trend for 2024",
        description="Line chart showing revenue over time"
    ),
    SampleQuestion(
        question="Which product category generates the most revenue?",
        description="Pie chart of sales by category"
    ),
    SampleQuestion(
        question="What are the top 5 products by total sales?",
        description="Bar chart of best selling products"
    ),
    SampleQuestion(
        question="How many units of each product were sold?",
        description="Table of product quantities"
    ),
    SampleQuestion(
        question="What is the average sale amount per region?",
        description="Bar chart of average transaction value"
    ),
]


@router.get(
    "/samples",
    response_model=SampleQuestionsResponse,
    summary="Get sample questions to try",
)
async def get_sample_questions():
    """Return pre-built sample questions for the UI."""
    return SampleQuestionsResponse(questions=SAMPLE_QUESTIONS)


@router.post(
    "/ask",
    response_model=QueryResponse,
    summary="Ask a question about the sales data",
)
async def ask_question(request: QueryRequest):
    """
    Convert a natural language question into SQL,
    execute it, and return chart-ready data.
    """
    try:
        result = answer_question(question=request.question)
        return QueryResponse(question=request.question, **result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process question. Please try again.",
        )