"""Application configuration — loads settings from .env file."""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Settings:
    """RegEngine settings."""

    # Qdrant
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")

    # LLM
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # App
    APP_ENV: str = os.getenv("APP_ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Ingestion
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # Retrieval
    TOP_K: int = 5
    SIMILARITY_THRESHOLD: float = 0.5

    # Paths
    UPLOAD_DIR: str = "uploads"
    COLLECT_DIR: str = "collections"


settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
