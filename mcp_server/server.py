"""MCP Server — expose RegEngine as an AI tool.

Implements three functional tools backed by the real RAG pipeline:
  - search_documentation(query, top_k=3)
  - ingest_document(file_path)
  - get_rag_status()

All tools catch exceptions and return informative messages so the MCP
protocol server never crashes from a tool-level error.
"""
from __future__ import annotations

import logging
import os
from typing import Any

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger("regengine.mcp")
if not logger.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    logger.addHandler(_h)
logger.setLevel(logging.INFO)

mcp = FastMCP("RegEngine")


def _format_search_results(query: str, top_k: int, results: list[dict]) -> str:
    """Render retrieved chunks as a structured human-readable context block."""
    if not results:
        return (
            f"No matching documentation found for query='{query}' "
            f"(top_k={top_k}). Try ingesting more documents or rephrasing."
        )

    parts: list[str] = [f"Found {len(results)} chunk(s) for query='{query}':"]
    parts.append("=" * 60)
    for i, r in enumerate(results, 1):
        text = (r.get("text") or "").strip().replace("\n", " ")
        if len(text) > 280:
            text = text[:277] + "..."
        score = r.get("score", 0.0)
        meta = r.get("metadata") or {}
        source = meta.get("source") or meta.get("filename") or "unknown"
        parts.append(
            f"[{i}] (score={score:.3f}, source={source})\n{text}"
        )
    parts.append("=" * 60)
    return "\n".join(parts)


@mcp.tool()
async def search_documentation(query: str, top_k: int = 3) -> str:
    """Search the RAG index and return structured context for the query.

    Args:
        query: Natural-language search query.
        top_k: Maximum number of chunks to return (default 3).

    Returns:
        Formatted multi-chunk context string, or an informative error.
    """
    try:
        from retrieval.search import search_context  # type: ignore
        results = search_context(query=query, top_k=top_k)
        if not isinstance(results, list):
            return (
                f"Error: retrieval returned unexpected type "
                f"{type(results).__name__}."
            )
        return _format_search_results(query, top_k, results)
    except ImportError as e:
        logger.warning("retrieval.search.search_context unavailable: %s", e)
        # Fallback: use the lower-level search_similar if available
        try:
            from retrieval.search import search_similar
            results = search_similar(query=query, top_k=top_k)
            return _format_search_results(query, top_k, results)
        except Exception as inner:
            return (
                f"Search failed: retrieval module not wired "
                f"({type(inner).__name__}: {inner})."
            )
    except Exception as e:
        logger.exception("search_documentation failed")
        return f"Search failed: {type(e).__name__}: {e}"


@mcp.tool()
async def ingest_document(file_path: str) -> str:
    """Ingest a document into the RAG pipeline.

    Args:
        file_path: Absolute or relative path to a .txt/.md/.pdf/.docx file.

    Returns:
        Ingestion summary (chunks stored, collection, etc.) or an error.
    """
    try:
        if not file_path or not isinstance(file_path, str):
            return "Error: file_path must be a non-empty string."

        if not os.path.exists(file_path):
            return f"Error: file does not exist at '{file_path}'."

        if not os.path.isfile(file_path):
            return f"Error: path '{file_path}' is not a regular file."

        allowed_exts = {".txt", ".md", ".pdf", ".docx"}
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in allowed_exts:
            return (
                f"Error: unsupported extension '{ext}'. "
                f"Allowed: {', '.join(sorted(allowed_exts))}."
            )

        # Try the orchestrator function first; fall back gracefully.
        from ingestion.pipeline import run_pipeline  # type: ignore
        result: Any = run_pipeline(file_path=file_path)
    except ImportError:
        try:
            from ingestion.pipeline import ingest_document as _ingest
            result = _ingest(file_path=file_path)
        except Exception as e:
            logger.exception("ingest_document fallback failed")
            return f"Ingestion failed: {type(e).__name__}: {e}"
    except FileNotFoundError as e:
        return f"Error: {e}"
    except Exception as e:
        logger.exception("ingest_document failed")
        return f"Ingestion failed: {type(e).__name__}: {e}"

    if isinstance(result, dict):
        chunks = result.get("total_chunks") or result.get("chunks_stored") or 0
        collection = result.get("collection", "default")
        return (
            f"Successfully ingested '{os.path.basename(file_path)}'. "
            f"chunks={chunks}, collection='{collection}'."
        )
    return f"Ingestion result: {result}"


@mcp.tool()
async def get_rag_status() -> str:
    """Report RAG system health: Qdrant connectivity and per-collection point counts.

    Returns:
        Human-readable status block, or an informative error string.
    """
    try:
        from qdrant_client import QdrantClient
        from api.config import settings
    except ImportError as e:
        return f"Error: required dependency missing ({type(e).__name__}: {e})."

    try:
        client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=getattr(settings, "QDRANT_API_KEY", "") or None,
        )
        collections = client.get_collections().collections
        if not collections:
            return (
                "Qdrant reachable, but no collections exist yet. "
                "Ingest a document to create one."
            )

        lines: list[str] = [
            f"Qdrant OK at {settings.QDRANT_URL}",
            f"Collections: {len(collections)}",
            "-" * 60,
        ]
        for c in collections:
            try:
                info = client.get_collection(c.name)
                count = getattr(info, "points_count", 0) or 0
            except Exception as inner:
                count = f"error: {inner}"
            lines.append(f"  - {c.name}: {count} points")
        lines.append("-" * 60)
        return "\n".join(lines)
    except Exception as e:
        logger.exception("get_rag_status failed")
        return (
            f"Qdrant unreachable ({type(e).__name__}: {e}). "
            f"Configured URL: {getattr(settings, 'QDRANT_URL', 'unknown')}."
        )


if __name__ == "__main__":
    mcp.run()
