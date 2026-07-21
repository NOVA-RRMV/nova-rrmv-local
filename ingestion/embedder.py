"""Embedder — convert text to vectors using sentence-transformers."""

from sentence_transformers import SentenceTransformer
from typing import Optional

# Global model instance (lazy loaded)
_model: Optional[SentenceTransformer] = None


def get_model(model_name: str = "all-MiniLM-L6-v2") -> SentenceTransformer:
    """Get or load the embedding model."""
    global _model
    if _model is None:
        _model = SentenceTransformer(model_name)
    return _model


def embed_text(texts: list[str], model_name: str = "all-MiniLM-L6-v2") -> list[list[float]]:
    """Convert a list of texts to embedding vectors.

    Args:
        texts: List of text strings to embed.
        model_name: Name of the sentence-transformers model.

    Returns:
        List of embedding vectors (each is a list of floats).
    """
    model = get_model(model_name)
    embeddings = model.encode(texts, show_progress_bar=False)
    return embeddings.tolist()


def embed_query(query: str, model_name: str = "all-MiniLM-L6-v2") -> list[float]:
    """Embed a single query string.

    Args:
        query: The query text.
        model_name: Name of the sentence-transformers model.

    Returns:
        Embedding vector.
    """
    return embed_text([query], model_name)[0]
