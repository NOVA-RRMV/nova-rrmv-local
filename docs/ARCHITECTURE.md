# RegEngine — Architecture Deep Dive

## How a RAG Engine Works

```
USER QUESTION
     │
     ▼
┌─────────────┐    "What is the warranty policy?"
│  Dashboard  │
└──────┬──────┘
       │ POST /api/query
       ▼
┌─────────────┐
│  FastAPI    │
│  (Backend)  │
└──────┬──────┘
       │
       ├─── STEP 1: Embed the question
       │    "warranty policy" → [0.12, -0.34, 0.56, ...]
       │
       ├─── STEP 2: Search Qdrant for similar vectors
       │    → Finds top 5 matching document chunks
       │
       ├─── STEP 3: Build prompt with context
       │    "Based on these documents: {chunks}, answer: {question}"
       │
       └─── STEP 4: Send to LLM → Get answer
                       → Return to user
```

---

## Module Breakdown

### 1. Ingestion Pipeline (`ingestion/`)

**Job:** Take raw documents → turn them into searchable vectors

```
PDF/DOCX/TXT → Loader → Chunker → Embedder → Qdrant
```

| File | Purpose |
|------|---------|
| `loader.py` | Read different file formats (PDF, DOCX, TXT, MD) |
| `chunker.py` | Split documents into ~500 token chunks with overlap |
| `embedder.py` | Convert text chunks to vectors using sentence-transformers |
| `pipeline.py` | Orchestrate: load → chunk → embed → store |

**Key decisions:**
- Chunk size: 500 tokens (sweet spot for retrieval quality)
- Overlap: 50 tokens (prevents cutting mid-sentence)
- Embedding model: `all-MiniLM-L6-v2` (fast, good quality, free)

### 2. Retrieval Engine (`retrieval/`)

**Job:** Given a question, find the most relevant document chunks

```
Question → Embed → Qdrant Search → Context Assembly
```

| File | Purpose |
|------|---------|
| `search.py` | Query Qdrant, return top-K results |
| `reranker.py` | Re-order results by relevance (optional) |
| `context.py` | Format retrieved chunks into LLM-ready prompt |

**Key decisions:**
- Top-K: 5 chunks (balance between context and noise)
- Similarity threshold: 0.7 minimum (ignore irrelevant results)

### 3. API Layer (`api/`)

**Job:** HTTP interface for everything

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Check if services are running |
| `/api/upload` | POST | Upload documents for ingestion |
| `/api/query` | POST | Ask a question, get an answer |
| `/api/collections` | GET | List stored document collections |
| `/api/stats` | GET | System stats (doc count, etc.) |

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app, routes, middleware |
| `models.py` | Pydantic request/response schemas |
| `config.py` | Environment variables, settings |

### 4. Dashboard (`dashboard/`)

**Job:** User-friendly interface

| Page | Purpose |
|------|---------|
| Chat | Ask questions, see answers with sources |
| Upload | Drag-and-drop document upload |
| Collections | Browse stored documents |
| Settings | API keys, model selection |

**Tech:** Streamlit for MVP (fast to build), can upgrade to React later.

### 5. Evaluation Pipeline (`eval/`)

**Job:** Measure how good the RAG system is

| Metric | What it measures |
|--------|-----------------|
| Relevance | Are retrieved chunks relevant to the question? |
| Faithfulness | Does the answer match the source documents? |
| Accuracy | Is the answer actually correct? |

| File | Purpose |
|------|---------|
| `metrics.py` | Custom evaluation metrics |
| `test_data.py` | Sample questions + expected answers |
| `run_eval.py` | Run evaluation pipeline |

### 6. MCP Server (`mcp_server/`)

**Job:** Expose RegEngine as an AI tool (for Claude, etc.)

This lets AI assistants use RegEngine as a tool — they can search your documents and get answers.

---

## Data Flow

```
                    ┌──────────────────────────────────┐
                    │         DOCUMENT UPLOAD           │
                    │                                    │
  User uploads PDF ──▶ Loader reads text ──▶ Chunker splits
                    │                                    │
                    │  Chunks ──▶ Embedder ──▶ Qdrant   │
                    └──────────────────────────────────┘

                    ┌──────────────────────────────────┐
                    │          QUERY FLOW               │
                    │                                    │
  User asks question ──▶ Embedder embeds question       │
                    │                                    │
                    │  ──▶ Qdrant finds top-5 chunks    │
                    │                                    │
                    │  ──▶ Context builds prompt        │
                    │                                    │
                    │  ──▶ LLM generates answer         │
                    │                                    │
                    │  ──▶ Response with sources ──▶ User│
                    └──────────────────────────────────┘
```

---

## Docker Services

| Service | Port | Purpose |
|---------|------|---------|
| qdrant | 6333, 6334 | Vector database |
| backend | 8000 | FastAPI server |
| dashboard | 8501 | Streamlit UI |

---

## Environment Variables

```bash
# .env file
OPENAI_API_KEY=sk-...           # For LLM generation
QDRANT_URL=http://qdrant:6333   # Vector DB connection
APP_ENV=development              # development / production
LOG_LEVEL=INFO                   # DEBUG / INFO / WARNING
```
