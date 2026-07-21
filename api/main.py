"""RegEngine — FastAPI Application.

This is the main entry point for the backend API.
"""

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .models import QueryRequest, QueryResponse, UploadResponse, HealthResponse

app = FastAPI(
    title="RegEngine API",
    description="RAG Engine — Retrieval-Augmented Generation",
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


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Check if all services are running."""
    return HealthResponse(
        status="ok",
        qdrant_connected=False,  # TODO: check Qdrant connection
        version="0.1.0",
    )


@app.post("/api/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload a document for ingestion into the RAG pipeline."""
    # TODO: Implement document upload
    # 1. Save file temporarily
    # 2. Run ingestion pipeline
    # 3. Store vectors in Qdrant
    return UploadResponse(
        filename=file.filename,
        chunks_stored=0,
        collection="default",
    )


@app.post("/api/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """Ask a question and get an answer with sources."""
    # TODO: Implement RAG query
    # 1. Embed the question
    # 2. Search Qdrant for similar vectors
    # 3. Build context from retrieved chunks
    # 4. Generate answer with LLM
    return QueryResponse(
        answer="TODO: Implement RAG query pipeline",
        sources=[],
        confidence=0.0,
    )


@app.get("/api/collections")
async def list_collections():
    """List all document collections in Qdrant."""
    # TODO: Query Qdrant for collections
    return {"collections": []}


@app.get("/api/stats")
async def get_stats():
    """Get system statistics."""
    # TODO: Return actual stats
    return {
        "total_documents": 0,
        "total_chunks": 0,
        "collections": [],
    }
