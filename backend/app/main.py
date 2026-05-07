# backend/app/main.py
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import query, health
from app.config import APP_ENV
from app.db.database import init_db
from app.core.sql_generator import get_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting AI Analytics Assistant | env={APP_ENV}")
    init_db()
    _auto_seed()
    get_client()
    logger.info("Database and LLM client ready.")
    yield


def _auto_seed():
    from app.db.database import SessionLocal
    from app.db.models import Sale
    db = SessionLocal()
    try:
        if db.query(Sale).count() == 0:
            logger.info("Database empty — seeding data")
            from scripts.seed_data import seed
            seed()
    finally:
        db.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Analytics Assistant",
        description="Ask questions about sales data in plain English. Get charts back.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(query.router, prefix="/api/v1")

    return app


app = create_app()