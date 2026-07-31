"""MCP Server — expose RagEngine as an AI tool.

Implements:
- search_documents: search chunks in Qdrant
- ask_regengine: full RAG query (search + context + answer)
- list_collections: list Qdrant collections with counts
"""

import sys
import os
from pathlib import Path

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server.fastmcp import FastMCP

from qdrant_client import QdrantClient

# ─── Qdrant Connection ─────────────────────────────────────


def get_qdrant() -> QdrantClient:
    """Get a Qdrant client connection."""
    try:
        from api.config import settings
        url = getattr(settings, "QDRANT_URL", None) or getattr(settings, "qdrant_url", "http://localhost:6333")
        api_key = getattr(settings, "QDRANT_API_KEY", None) or getattr(settings, "qdrant_api_key", None)
        return QdrantClient(url=url, api_key=api_key or None)
    except ImportError:
        return QdrantClient(url="http://localhost:6333")


# Create MCP server instance
mcp = FastMCP("RagEngine")


@mcp.tool()
async def search_documents(query: str, collection: str = "default", top_k: int = 5) -> str:
    """Search through documents in RagEngine.

    Args:
        query: The search query.
        collection: The document collection to search.
        top_k: Number of results to return.

    Returns:
        Relevant document chunks matching the query.
    """
    try:
        from ingestion.embedder import embed_text

        # Embed the query
        query_vector = embed_text([query])[0]

        # Search Qdrant
        client = get_qdrant()
        try:
            results = client.query_points(
                collection_name=collection,
                query=query_vector,
                limit=top_k,
                score_threshold=0.5,
            )
        except Exception:
            return f"No collection '{collection}' found. Upload a document first."

        if not results or not results.points:
            return f"No results found for '{query}' in collection '{collection}'."

        # Format results
        output = []
        for i, point in enumerate(results.points, 1):
            payload = point.payload or {}
            text = payload.get("text", "No text")
            filename = payload.get("filename", "unknown")
            score = point.score
            output.append(
                f"[{i}] (score: {score:.3f}) from {filename}:\n{text[:300]}{'...' if len(text) > 300 else ''}"
            )

        return "\n\n".join(output)

    except Exception as e:
        return f"Error searching documents: {e}"


@mcp.tool()
async def ask_regengine(question: str, collection: str = "default") -> str:
    """Ask a question and get an answer from RagEngine.

    Args:
        question: The question to ask.
        collection: The document collection to query.

    Returns:
        Answer with source citations.
    """
    try:
        from ingestion.embedder import embed_text
        from retrieval.context import build_context, build_prompt

        # Embed the question
        query_vector = embed_text([question])[0]

        # Search Qdrant
        client = get_qdrant()
        try:
            results = client.query_points(
                collection_name=collection,
                query=query_vector,
                limit=5,
                score_threshold=0.5,
            )
        except Exception:
            return f"No collection '{collection}' found. Upload a document first."

        if not results or not results.points:
            return "No relevant documents found. Try uploading documents first."

        # Build context from results
        chunks = []
        for point in results.points:
            payload = point.payload or {}
            chunks.append({
                "text": payload.get("text", ""),
                "score": point.score,
                "filename": payload.get("filename", "unknown"),
            })

        context = build_context(chunks)

        # Generate answer with LLM
        answer = ""

        openai_key = os.getenv("OPENAI_API_KEY", "")
        if not openai_key:
            try:
                from api.config import settings
                openai_key = getattr(settings, "OPENAI_API_KEY", "") or ""
            except ImportError:
                pass

        if openai_key:
            try:
                import openai
                client_ai = openai.OpenAI(api_key=openai_key)
                prompt = build_prompt(question, context)
                response = client_ai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,
                )
                answer = response.choices[0].message.content
            except Exception as e:
                answer = f"(LLM error: {e})\n\nHere are the relevant sources:"
        else:
            answer = "No OpenAI API key configured. Here are the relevant sources:"

        # Append sources
        source_text = "\n\nSources:\n"
        for i, chunk in enumerate(chunks, 1):
            source_text += f"[{i}] {chunk['filename']} (score: {chunk['score']:.3f})\n"

        return answer + source_text

    except Exception as e:
        return f"Error answering question: {e}"


@mcp.tool()
async def list_collections() -> str:
    """List all available document collections in RagEngine.

    Returns:
        List of collection names and their document counts.
    """
    try:
        client = get_qdrant()
        collections = client.get_collections().collections

        if not collections:
            return "No collections found. Upload a document to create one."

        output = []
        for col in collections:
            try:
                info = client.get_collection(col.name)
                count = info.points_count
            except Exception:
                count = "unknown"
            output.append(f"- {col.name}: {count} points")

        return "\n".join(output)

    except Exception as e:
        return f"Error listing collections: {e}"


if __name__ == "__main__":
    mcp.run()
