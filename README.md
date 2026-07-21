# RegEngine

> A Retrieval-Augmented Generation (RAG) Engine — built by Team Nova RRMV

RegEngine is a modular RAG system that ingests documents, embeds them into vector space, stores them in Qdrant, and retrieves relevant context to power LLM-generated answers. It includes a web dashboard, evaluation pipeline, and MCP server integration.

---

## Architecture Overview

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Dashboard   │────▶│  FastAPI API │────▶│  Qdrant DB   │
│  (Frontend)  │     │  (Backend)   │     │  (Vectors)   │
└──────────────┘     └──────┬───────┘     └──────────────┘
                            │
                  ┌─────────┴─────────┐
                  │                   │
            ┌─────▼─────┐      ┌─────▼──────┐
            │ Ingestion │      │  Retrieval │
            │  Pipeline │      │   Engine   │
            └───────────┘      └────────────┘
                  │                   │
            ┌─────▼─────┐      ┌─────▼──────┐
            │  LLM API  │      │  Eval      │
            │ (Generate)│      │  Pipeline  │
            └───────────┘      └────────────┘

            ┌───────────┐
            │ MCP Server│  (AI Tool Integration)
            └───────────┘
```

## Project Structure

```
root/
├── api/                # FastAPI backend (routes, models, config)
├── ingestion/          # Document loading, chunking, embedding
├── retrieval/          # Vector search, context assembly
├── eval/               # Evaluation metrics, benchmarks
├── dashboard/          # Web UI (Streamlit or React)
├── mcp_server/         # Model Context Protocol server
├── docker-compose.yml  # Service orchestration
├── Dockerfile          # Backend container
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Tech Stack

| Component       | Technology                  |
|----------------|----------------------------|
| Backend API    | Python 3.11 + FastAPI       |
| Vector DB      | Qdrant (Docker)             |
| Embeddings     | sentence-transformers       |
| LLM            | OpenAI / Ollama (local)     |
| Frontend       | Streamlit (MVP) / React     |
| Containers     | Docker + Docker Compose     |
| Eval           | Custom metrics + RAGAS      |

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/nova-rrmv/regengine.git
cd regengine

# 2. Start with Docker
docker-compose up --build

# 3. Access
# API:    http://localhost:8000/docs
# UI:     http://localhost:8501
# Qdrant: http://localhost:6333/dashboard
```

## Development Phases

| Phase | What | Owner | Status |
|-------|------|-------|--------|
| 1 | Project setup + Docker | Mrity | 🔄 In Progress |
| 2 | Ingestion pipeline | Rakhi | ⏳ Pending |
| 3 | Retrieval engine | Viraj | ⏳ Pending |
| 4 | API layer | Mrity | ⏳ Pending |
| 5 | Dashboard UI | Megha | ⏳ Pending |
| 6 | Eval pipeline | All | ⏳ Pending |
| 7 | MCP Server | All | ⏳ Pending |
| 8 | Integration + Testing | All | ⏳ Pending |

## Team: Nova RRMV

| Member | Focus Area | Branch |
|--------|-----------|--------|
| Mrity | API + coordination, integration | `feature/api-layer` |
| Rakhi | Document ingestion pipeline | `feature/ingestion-pipeline` |
| Viraj | Retrieval + vector search | `feature/retrieval-engine` |
| Megha | Dashboard UI | `feature/dashboard` |
| Shared | Evaluation + MCP server | `feature/eval-pipeline` / `feature/mcp-server` |

## License

MIT
