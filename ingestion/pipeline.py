"""Ingestion pipeline — orchestrate: load → chunk → embed → store."""

from .loader import load_document
from .chunker import chunk_text
from .embedder import embed_text


def ingest_document(
    file_path: str,
    collection: str = "default",
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> dict:
    """Full ingestion pipeline for a single document.

    Args:
        file_path: Path to the document file.
        collection: Qdrant collection name.
        chunk_size: Target chunk size in characters.
        chunk_overlap: Overlap between chunks.

    Returns:
        Dict with stats about the ingestion.
    """
    # Step 1: Load document
    text = load_document(file_path)
    print(f"[Ingestion] Loaded {len(text)} characters from {file_path}")

    # Step 2: Chunk text
    chunks = chunk_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    print(f"[Ingestion] Split into {len(chunks)} chunks")

    # Step 3: Embed chunks
    chunk_texts = [c["text"] for c in chunks]
    embeddings = embed_text(chunk_texts)
    print(f"[Ingestion] Generated {len(embeddings)} embeddings")

    # Step 4: Store in Qdrant
    # TODO: Implement Qdrant storage
    # from retrieval.vector_store import store_vectors
    # store_vectors(collection, chunks, embeddings)

    return {
        "file_path": file_path,
        "total_characters": len(text),
        "total_chunks": len(chunks),
        "total_embeddings": len(embeddings),
        "collection": collection,
    }
