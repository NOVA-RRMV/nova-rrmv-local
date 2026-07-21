"""Pydantic models for API request/response schemas."""

from pydantic import BaseModel
from typing import Optional


class QueryRequest(BaseModel):
    """Request body for asking a question."""
    question: str
    collection: str = "default"
    top_k: int = 5


class QueryResponse(BaseModel):
    """Response body for a query answer."""
    answer: str
    sources: list[dict]
    confidence: float


class UploadResponse(BaseModel):
    """Response body for document upload."""
    filename: str
    chunks_stored: int
    collection: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    qdrant_connected: bool
    version: str
