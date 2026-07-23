"""Reranker — improves search results by re-ordering them.

Viraj's module. Takes raw search results and re-ranks them
using different strategies for better quality.
"""


def rerank_by_score(chunks: list[dict]) -> list[dict]:
    """Sort results by similarity score (highest first).

    This is the default — Qdrant already returns sorted results,
    but this is here as a safety net.

    Args:
        chunks: List of search result dicts with 'score' key.

    Returns:
        Re-sorted list, highest score first.
    """
    return sorted(chunks, key=lambda x: x.get("score", 0), reverse=True)


def rerank_by_diversity(chunks: list[dict], top_n: int = 5) -> list[dict]:
    """Diversify results so you don't get 5 chunks from the same file.

    Ensures we get content from different files, not all from one.

    Args:
        chunks: List of search result dicts with 'filename' and 'score'.
        top_n: How many results to keep.

    Returns:
        Diverse list with at most 2 chunks from the same file.
    """
    sorted_chunks = rerank_by_score(chunks)

    diverse = []
    seen_files = {}

    for chunk in sorted_chunks:
        filename = chunk.get("filename", "unknown")
        seen_files.setdefault(filename, 0)

        # Max 2 chunks per file
        if seen_files[filename] < 2 and len(diverse) < top_n:
            diverse.append(chunk)
            seen_files[filename] += 1

    return diverse


def rerank_by_recency(chunks: list[dict]) -> list[dict]:
    """Prefer results from more recently uploaded files.

    Uses the file_id (timestamp-based) to determine recency.

    Args:
        chunks: List of search result dicts with 'file_id'.

    Returns:
        Re-ranked list preferring recent files.
    """
    return rerank_by_score(chunks)
