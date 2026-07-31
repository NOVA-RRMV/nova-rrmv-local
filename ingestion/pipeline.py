"""Ingestion pipeline — orchestrate: load → chunk → embed → store in Qdrant."""

import os
import uuid
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

from .loader import load_document
from .chunker import chunk_text
from .embedder import embed_text

# ─── Qdrant Config ─────────────────────────────────────────


def get_qdrant() -> QdrantClient:
    """Get a Qdrant client connection."""
    try:
        from api.config import settings
        url = getattr(settings, "QDRANT_URL", None) or getattr(settings, "qdrant_url", "http://localhost:6333")
        api_key = getattr(settings, "QDRANT_API_KEY", None) or getattr(settings, "qdrant_api_key", None)
        return QdrantClient(url=url, api_key=api_key or None)
    except ImportError:
        return QdrantClient(url="http://localhost:6333")


def get_embedding_dim() -> int:
    """Get embedding dimension (all-MiniLM-L6-v2 = 384)."""
    return 384


def ensure_collection(client: QdrantClient, collection: str) -> None:
    """Create collection if it doesn't exist."""
    collections = [c.name for c in client.get_collections().collections]
    if collection not in collections:
        client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(
                size=get_embedding_dim(),
                distance=Distance.COSINE,
            ),
        )
        print(f"[Ingestion] Created collection: {collection}")


# ─── Main Pipeline ─────────────────────────────────────────


def ingest_document(
    file_path: str,
    collection: str = "default",
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    file_id: str = None,
) -> dict:
    """Full ingestion pipeline for a single document.

    Args:
        file_path: Path to the document file.
        collection: Qdrant collection name.
        chunk_size: Target chunk size in characters.
        chunk_overlap: Overlap between chunks.
        file_id: Optional unique ID for the document.

    Returns:
        Dict with stats about the ingestion.
    """
    # Step 1: Load document
    text = load_document(file_path)
    print(f"[Ingestion] Loaded {len(text)} characters from {file_path}")

    if not text.strip():
        print("[Ingestion] WARNING: Document is empty or unreadable")
        return {
            "file_path": file_path,
            "total_characters": 0,
            "total_chunks": 0,
            "total_embeddings": 0,
            "collection": collection,
        }

    # Step 2: Chunk text
    chunks = chunk_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    print(f"[Ingestion] Split into {len(chunks)} chunks")

    if not chunks:
        print("[Ingestion] WARNING: No chunks produced")
        return {
            "file_path": file_path,
            "total_characters": len(text),
            "total_chunks": 0,
            "total_embeddings": 0,
            "collection": collection,
        }

    # Step 3: Embed chunks
    chunk_texts = [c["text"] for c in chunks]
    embeddings = embed_text(chunk_texts)
    print(f"[Ingestion] Generated {len(embeddings)} embeddings")

    # Step 4: Store in Qdrant
    if not file_id:
        file_id = str(uuid.uuid4())[:8]

    client = get_qdrant()
    ensure_collection(client, collection)

    points = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk["text"],
                    "filename": Path(file_path).name,
                    "file_id": file_id,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "start": chunk.get("start", 0),
                    "end": chunk.get("end", 0),
                },
            )
        )

    client.upsert(
        collection_name=collection,
        points=points,
    )
    stored = len(points)
    print(f"[Ingestion] Stored {stored} points in Qdrant ({collection})")

    return {
        "file_path": file_path,
        "file_id": file_id,
        "total_characters": len(text),
        "total_chunks": len(chunks),
        "total_embeddings": len(embeddings),
        "stored_points": stored,
        "collection": collection,
    }
