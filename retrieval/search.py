"""Vector search — query Qdrant for similar document chunks.

This is Viraj's module. Handles all Qdrant search operations:
- Basic vector search
- Filtered search (by filename, date, etc.)
- Multi-collection search
- Result formatting with scores
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

from ingestion.embedder import embed_query
from api.config import settings


def get_client() -> QdrantClient:
    """Get a Qdrant client connection."""
    url = getattr(settings, 'QDRANT_URL', None) or getattr(settings, 'qdrant_url', 'http://localhost:6333')
    api_key = getattr(settings, 'QDRANT_API_KEY', None) or getattr(settings, 'qdrant_api_key', None) or None
    return QdrantClient(url=url, api_key=api_key)


def search_similar(
    query: str,
    collection: str = "default",
    top_k: int = 5,
    similarity_threshold: float = 0.5,
    filters: dict | None = None,
) -> list[dict]:
    """Search Qdrant for chunks similar to the query.

    Args:
        query: The search query text.
        collection: Qdrant collection name.
        top_k: Number of results to return.
        similarity_threshold: Minimum similarity score (0.0 to 1.0).
        filters: Optional filters e.g. {"filename": "report.pdf"}

    Returns:
        List of matched chunks with text, score, and metadata.
    """
    client = get_client()

    # Embed the query text into a vector
    query_vector = embed_query(query)

    # Build optional Qdrant filter
    query_filter = None
    if filters:
        conditions = []
        for key, value in filters.items():
            conditions.append(
                FieldCondition(key=key, match=MatchValue(value=value))
            )
        query_filter = Filter(must=conditions)

    # Search Qdrant (v1.18+ uses query_points)
    response = client.query_points(
        collection_name=collection,
        query=query_vector,
        limit=top_k,
        score_threshold=similarity_threshold,
        query_filter=query_filter,
    )

    results = response.points

    # Format results into clean dicts
    chunks = []
    for result in results:
        chunks.append({
            "text": result.payload.get("text", ""),
            "score": round(result.score, 3),
            "filename": result.payload.get("filename", ""),
            "chunk_index": result.payload.get("chunk_index", 0),
            "total_chunks": result.payload.get("total_chunks", 0),
        })

    return chunks


def search_by_filename(
    query: str,
    filename: str,
    collection: str = "default",
    top_k: int = 5,
) -> list[dict]:
    """Search only within a specific uploaded file.

    Args:
        query: The search query text.
        filename: Filter to this specific file.
        collection: Qdrant collection name.
        top_k: Number of results to return.

    Returns:
        List of matched chunks from that file.
    """
    return search_similar(
        query=query,
        collection=collection,
        top_k=top_k,
        filters={"filename": filename},
    )


def search_all_collections(
    query: str,
    top_k: int = 3,
) -> dict[str, list[dict]]:
    """Search across ALL collections in Qdrant.

    Args:
        query: The search query text.
        top_k: Results per collection.

    Returns:
        Dict with collection names as keys, results as values.
    """
    client = get_client()
    collections = [c.name for c in client.get_collections().collections]
    query_vector = embed_query(query)

    results = {}
    for col_name in collections:
        response = client.query_points(
            collection_name=col_name,
            query=query_vector,
            limit=top_k,
            score_threshold=0.3,
        )
        chunks = []
        for r in response.points:
            chunks.append({
                "text": r.payload.get("text", ""),
                "score": round(r.score, 3),
                "filename": r.payload.get("filename", ""),
            })
        if chunks:
            results[col_name] = chunks

    return results
