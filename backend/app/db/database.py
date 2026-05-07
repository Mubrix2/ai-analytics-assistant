# backend/app/db/database.py
import logging
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from app.config import DATABASE_URL, BASE_DIR
from app.db.models import Base

logger = logging.getLogger(__name__)

# Ensure data directory exists before engine creation
data_dir = BASE_DIR / "data"
data_dir.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_query(sql: str) -> list[dict]:
    """
    Execute a raw SQL query and return results as a list of dicts.
    This is what the query runner calls — plain SQL in, plain data out.
    """
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        columns = list(result.keys())
        rows = result.fetchall()
        return [dict(zip(columns, row)) for row in rows]