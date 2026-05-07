# backend/app/core/sql_generator.py
import logging
from groq import Groq
from app.config import GROQ_API_KEY, LLM_MODEL

logger = logging.getLogger(__name__)

# This is the schema context you pass to the LLM.
# Every table, column, and relationship the LLM needs to know about.
# If you add a table later, add it here.
DATABASE_SCHEMA = """
You have access to a SQLite database with these tables:

TABLE: regions
  - id (INTEGER, primary key)
  - name (TEXT) — values: 'North', 'South', 'East', 'West', 'Lagos', 'Abuja'
  - country (TEXT) — always 'Nigeria'

TABLE: products
  - id (INTEGER, primary key)
  - name (TEXT) — product name e.g. 'Laptop Pro 15'
  - category (TEXT) — values: 'Electronics', 'Furniture', 'Software'
  - unit_price (REAL) — price in Nigerian Naira

TABLE: sales
  - id (INTEGER, primary key)
  - product_id (INTEGER, foreign key → products.id)
  - region_id (INTEGER, foreign key → regions.id)
  - quantity (INTEGER)
  - amount (REAL) — total sale amount in Naira
  - sale_date (DATETIME) — format: YYYY-MM-DD HH:MM:SS

RELATIONSHIPS:
  - sales.product_id → products.id
  - sales.region_id → regions.id

IMPORTANT NOTES:
  - Always use table aliases in JOINs for clarity
  - For date filtering use: strftime('%Y', sale_date) for year, strftime('%Y-%m', sale_date) for month
  - Amounts are in Nigerian Naira
  - Limit results to 50 rows maximum unless the user asks for all data
"""

SYSTEM_PROMPT = f"""You are a SQL expert. Convert the user's natural language question 
into a valid SQLite SQL query using the database schema below.

{DATABASE_SCHEMA}

Rules:
1. Return ONLY the SQL query — no explanation, no markdown, no backticks
2. Only write SELECT statements — never INSERT, UPDATE, DELETE, or DROP
3. Always include meaningful column aliases for readability
4. If the question cannot be answered with this schema, return: CANNOT_ANSWER
5. Use proper SQLite syntax"""

_client = None


def get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
        logger.info("Groq client initialised")
    return _client


def generate_sql(question: str) -> str:
    """
    Convert a natural language question into a SQL query.

    Returns the SQL string, or 'CANNOT_ANSWER' if the question
    cannot be answered with the available schema.
    """
    if not question.strip():
        raise ValueError("Question cannot be empty")

    client = get_client()
    logger.info(f"Generating SQL for: '{question[:60]}'")

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        temperature=0.0,
        max_tokens=500,
    )

    sql = response.choices[0].message.content.strip()
    logger.info(f"Generated SQL: {sql[:100]}")
    return sql