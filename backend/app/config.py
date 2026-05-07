# backend/app/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _require(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(f"Required env variable '{key}' is not set.")
    return value


GROQ_API_KEY: str = _require("GROQ_API_KEY")
LLM_MODEL: str = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{BASE_DIR}/data/analytics.db"
)
APP_ENV: str = os.getenv("APP_ENV", "development")