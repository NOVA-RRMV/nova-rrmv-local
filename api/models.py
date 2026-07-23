"""Pydantic models for API request/response schemas."""

from pydantic import BaseModel
from typing import Optional


# ─── Query ────────────────────────────────────────────────────

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


# ─── Upload ───────────────────────────────────────────────────

class UploadResponse(BaseModel):
    """Response body for document upload."""
    filename: str
    chunks_stored: int
    collection: str


# ─── Health ───────────────────────────────────────────────────

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    qdrant_connected: bool
    version: str


# ─── Search (new) ──────────────────────────────────────────────

class SearchRequest(BaseModel):
    """Request body for raw search."""
    query: str
    collection: str = "default"
    top_k: int = 5


class SearchResult(BaseModel):
    """A single search result chunk."""
    text: str
    score: float
    filename: str
    chunk_index: int = 0
    total_chunks: int = 0


class SearchResponse(BaseModel):
    """Response body for raw search."""
    results: list[SearchResult]
    total_results: int
    collection: str
