"""Ingestion pipeline — orchestrate: load → chunk → embed → store."""

import uuid
from .loader import load_document
from .chunker import chunk_text
from .embedder import embed_text
from api.config import settings
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct


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
        Dict with stats about the ingestion (now includes Qdrant persistence).
    """
    import os
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

    # Step 4: Store in Qdrant (implemented)
    client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY or None)
    collections = [c.name for c in client.get_collections().collections]
    if collection not in collections:
        client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

    points = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk["text"],
                    "source": file_path,
                    "chunk_id": str(uuid.uuid4())[:8],
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                },
            )
        )

    if points:
        client.upsert(collection_name=collection, points=points)
    print(f"[Ingestion] Stored {len(points)} points in Qdrant collection '{collection}'")

    return {
        "file_path": file_path,
        "total_characters": len(text),
        "total_chunks": len(chunks),
        "total_embeddings": len(embeddings),
        "collection": collection,
        "points_stored": len(points),
    }
