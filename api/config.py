"""Application configuration."""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """RegEngine settings — loaded from environment variables."""

    # Qdrant
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")

    # LLM
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    # App
    app_env: str = os.getenv("APP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # Ingestion
    chunk_size: int = 500
    chunk_overlap: int = 50
    embedding_model: str = "all-MiniLM-L6-v2"

    # Retrieval
    top_k: int = 5
    similarity_threshold: float = 0.7

    class Config:
        env_file = ".env"


settings = Settings()
