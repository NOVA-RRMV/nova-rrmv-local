"""Vector search — query Qdrant for similar document chunks."""

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

from ingestion.embedder import embed_query
from api.config import settings


def get_client() -> QdrantClient:
    """Get a Qdrant client connection."""
    return QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key or None,
    )


def search_similar(
    query: str,
    collection: str = "default",
    top_k: int = 5,
    similarity_threshold: float = 0.7,
) -> list[dict]:
    """Search Qdrant for chunks similar to the query.

    Args:
        query: The search query text.
        collection: Qdrant collection name.
        top_k: Number of results to return.
        similarity_threshold: Minimum similarity score.

    Returns:
        List of matched chunks with scores.
    """
    client = get_client()

    # Embed the query
    query_vector = embed_query(query)

    # Search Qdrant (v1.18+ uses query_points)
    response = client.query_points(
        collection_name=collection,
        query=query_vector,
        limit=top_k,
        score_threshold=similarity_threshold,
    )

    results = response.points

    # Format results
    chunks = []
    for result in results:
        chunks.append({
            "text": result.payload.get("text", ""),
            "score": result.score,
            "metadata": result.payload.get("metadata", {}),
        })

    return chunks
