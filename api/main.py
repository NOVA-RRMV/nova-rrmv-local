"""RegEngine — FastAPI Application.

Main entry point for the backend API.
All routes are here. This is your central hub.
"""

import os
import uuid
import shutil
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue,
)

from .config import settings
from .models import (
    QueryRequest, QueryResponse,
    UploadResponse, HealthResponse,
    SearchRequest, SearchResponse, SearchResult,
)

# ─── App Setup ───────────────────────────────────────────────

app = FastAPI(
    title="RegEngine API",
    description="RAG Engine — upload documents, ask questions, get answers",
    version="0.1.0",
)

# CORS — allow dashboard to talk to API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Qdrant Connection ───────────────────────────────────────


def get_qdrant() -> QdrantClient:
    """Get a Qdrant client connection."""
    url = getattr(settings, 'QDRANT_URL', None) or getattr(settings, 'qdrant_url', 'http://localhost:6333')
    api_key = getattr(settings, 'QDRANT_API_KEY', None) or getattr(settings, 'qdrant_api_key', None) or None
    return QdrantClient(url=url, api_key=api_key)


def get_upload_dir() -> str:
    return getattr(settings, 'UPLOAD_DIR', None) or getattr(settings, 'upload_dir', 'uploads')


def get_chunk_size() -> int:
    return getattr(settings, 'CHUNK_SIZE', None) or getattr(settings, 'chunk_size', 500)


def get_chunk_overlap() -> int:
    return getattr(settings, 'CHUNK_OVERLAP', None) or getattr(settings, 'chunk_overlap', 50)


def get_similarity_threshold() -> float:
    return getattr(settings, 'SIMILARITY_THRESHOLD', None) or getattr(settings, 'similarity_threshold', 0.5)


def get_embedding_model() -> str:
    return getattr(settings, 'EMBEDDING_MODEL', None) or getattr(settings, 'embedding_model', 'all-MiniLM-L6-v2')


def ensure_collection(client: QdrantClient, collection: str = "default"):
    """Create collection if it doesn't exist."""
    collections = [c.name for c in client.get_collections().collections]
    if collection not in collections:
        client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(
                size=384,  # all-MiniLM-L6-v2 produces 384-dim vectors
                distance=Distance.COSINE,
            ),
        )


# ─── Routes ──────────────────────────────────────────────────


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Check if all services are running."""
    qdrant_ok = False
    try:
        client = get_qdrant()
        client.get_collections()
        qdrant_ok = True
    except Exception:
        pass

    return HealthResponse(
        status="ok" if qdrant_ok else "degraded",
        qdrant_connected=qdrant_ok,
        version="0.1.0",
    )


@app.post("/api/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    collection: str = Query(default="default", description="Collection name"),
):
    """Upload a document for ingestion into the RAG pipeline.

    1. Save file to disk
    2. Load and extract text
    3. Split into chunks
    4. Generate embeddings
    5. Store in Qdrant
    """
    # Validate file type
    allowed = {".txt", ".md", ".pdf", ".docx"}
    ext = Path(file.filename).suffix.lower()
    if ext not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{ext}' not supported. Use: {', '.join(allowed)}",
        )

    upload_dir = get_upload_dir()
    os.makedirs(upload_dir, exist_ok=True)

    # Save file to disk
    file_id = str(uuid.uuid4())[:8]
    save_path = os.path.join(upload_dir, f"{file_id}_{file.filename}")
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Load document text
    try:
        from ingestion.loader import load_document
        text = load_document(save_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")

    if not text.strip():
        raise HTTPException(status_code=400, detail="File is empty or unreadable")

    # Chunk text
    from ingestion.chunker import chunk_text
    chunks = chunk_text(
        text,
        chunk_size=get_chunk_size(),
        chunk_overlap=get_chunk_overlap(),
    )

    # Generate embeddings
    from ingestion.embedder import embed_text
    chunk_texts = [c["text"] for c in chunks]
    embeddings = embed_text(chunk_texts, model_name=get_embedding_model())

    # Store in Qdrant
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
                    "filename": file.filename,
                    "file_id": file_id,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                },
            )
        )

    client.upsert(collection_name=collection, points=points)

    return UploadResponse(
        filename=file.filename,
        chunks_stored=len(chunks),
        collection=collection,
    )


@app.post("/api/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """Ask a question and get an answer with sources.

    1. Embed the question
    2. Search Qdrant for similar chunks
    3. Build context from results
    4. Generate answer with LLM (if API key available)
    """
    client = get_qdrant()

    # Check collection exists
    collections = [c.name for c in client.get_collections().collections]
    if request.collection not in collections:
        raise HTTPException(
            status_code=404,
            detail=f"Collection '{request.collection}' not found. Upload some documents first.",
        )

    # Embed the question
    from ingestion.embedder import embed_query
    query_vector = embed_query(request.question, model_name=get_embedding_model())

    # Search Qdrant (v1.18+ uses query_points)
    response = client.query_points(
        collection_name=request.collection,
        query=query_vector,
        limit=request.top_k,
        score_threshold=get_similarity_threshold(),
    )

    results = response.points

    if not results:
        return QueryResponse(
            answer="No relevant documents found. Try uploading some documents first.",
            sources=[],
            confidence=0.0,
        )

    # Format sources
    sources = []
    for r in results:
        sources.append({
            "text": r.payload.get("text", ""),
            "filename": r.payload.get("filename", ""),
            "file_id": r.payload.get("file_id", ""),
            "score": round(r.score, 3),
        })

    # Build context
    from retrieval.context import build_context, build_prompt
    context = build_context(sources)

    # Generate answer with LLM (if key available)
    openai_key = getattr(settings, 'OPENAI_API_KEY', None) or getattr(settings, 'openai_api_key', None)
    answer = ""
    if openai_key and openai_key != "sk-your-key-here":
        try:
            from openai import OpenAI
            openai_client = OpenAI(api_key=openai_key)
            prompt = build_prompt(request.question, context)

            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
            )
            answer = response.choices[0].message.content
        except Exception as e:
            answer = f"LLM error: {str(e)}\n\nHere are the relevant sources:\n\n{context}"
    else:
        answer = (
            "No OpenAI API key configured. "
            "Here are the relevant sources:\n\n"
            f"{context}"
        )

    # Calculate confidence
    avg_score = sum(s["score"] for s in sources) / len(sources)

    return QueryResponse(
        answer=answer,
        sources=sources,
        confidence=round(avg_score, 3),
    )


@app.post("/api/search", response_model=SearchResponse)
async def raw_search(request: SearchRequest):
    """Search documents and return raw chunks WITHOUT LLM.

    Useful for debugging or when you just want to see what's relevant.
    """
    client = get_qdrant()

    # Check collection exists
    collections = [c.name for c in client.get_collections().collections]
    if request.collection not in collections:
        raise HTTPException(
            status_code=404,
            detail=f"Collection '{request.collection}' not found.",
        )

    # Embed the query
    from ingestion.embedder import embed_query
    query_vector = embed_query(request.query, model_name=get_embedding_model())

    # Search Qdrant
    response = client.query_points(
        collection_name=request.collection,
        query=query_vector,
        limit=request.top_k,
        score_threshold=get_similarity_threshold(),
    )

    results_list = []
    for r in response.points:
        results_list.append(SearchResult(
            text=r.payload.get("text", ""),
            score=round(r.score, 3),
            filename=r.payload.get("filename", ""),
            chunk_index=r.payload.get("chunk_index", 0),
            total_chunks=r.payload.get("total_chunks", 0),
        ))

    return SearchResponse(
        results=results_list,
        total_results=len(results_list),
        collection=request.collection,
    )


@app.get("/api/collections")
async def list_collections():
    """List all document collections in Qdrant."""
    client = get_qdrant()
    collections_info = []

    for collection in client.get_collections().collections:
        info = client.get_collection(collection.name)
        collections_info.append({
            "name": collection.name,
            "points_count": info.points_count or 0,
        })

    return {"collections": collections_info}


@app.get("/api/collections/{collection}/documents")
async def list_documents(collection: str = "default"):
    """List all documents in a collection (unique filenames).

    Args:
        collection: Collection name.

    Returns:
        List of unique filenames and their chunk counts.
    """
    client = get_qdrant()

    # Check collection exists
    collections = [c.name for c in client.get_collections().collections]
    if collection not in collections:
        raise HTTPException(status_code=404, detail=f"Collection '{collection}' not found.")

    # Scroll all points and count by filename
    scroll_response = client.scroll(
        collection_name=collection,
        limit=1000,
        with_payload=True,
        with_vectors=False,
    )

    file_counts = {}
    for point in scroll_response[0]:
        filename = point.payload.get("filename", "unknown")
        file_counts[filename] = file_counts.get(filename, 0) + 1

    documents = [
        {"filename": name, "chunks": count}
        for name, count in file_counts.items()
    ]

    return {"collection": collection, "documents": documents, "total": len(documents)}


@app.delete("/api/collections/{collection}")
async def delete_collection(collection: str):
    """Delete an entire collection and all its data."""
    client = get_qdrant()

    collections = [c.name for c in client.get_collections().collections]
    if collection not in collections:
        raise HTTPException(status_code=404, detail=f"Collection '{collection}' not found.")

    client.delete_collection(collection_name=collection)
    return {"status": "deleted", "collection": collection}


@app.post("/api/collections/{collection}/clear")
async def clear_collection(collection: str):
    """Remove all points from a collection (keeps the collection)."""
    client = get_qdrant()

    collections = [c.name for c in client.get_collections().collections]
    if collection not in collections:
        raise HTTPException(status_code=404, detail=f"Collection '{collection}' not found.")

    # Delete all points by filtering with a match-all condition
    client.delete(
        collection_name=collection,
        points_selector=Filter(must=[]),
    )
    return {"status": "cleared", "collection": collection}


@app.get("/api/stats")
async def get_stats():
    """Get system statistics."""
    client = get_qdrant()
    collections = client.get_collections().collections

    total_points = 0
    collection_names = []
    for col in collections:
        info = client.get_collection(col.name)
        total_points += info.points_count or 0
        collection_names.append(col.name)

    # Count uploaded files
    upload_dir = get_upload_dir()
    upload_files = []
    if os.path.exists(upload_dir):
        upload_files = os.listdir(upload_dir)

    return {
        "total_collections": len(collections),
        "total_vectors": total_points,
        "total_uploads": len(upload_files),
        "collections": collection_names,
    }
