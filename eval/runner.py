"""Evaluation Runner — test RagEngine pipeline quality.

Runs the full RAG pipeline (search → context → answer) against
a set of test queries and scores the quality using eval/metrics.py.

Usage:
    python -m eval.runner              # run all test cases
    python -m eval.runner --quick      # fewer test cases
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from eval.metrics import run_evaluation

# ─── Test Queries ──────────────────────────────────────────

TEST_QUERIES = [
    {
        "query": "What is RagEngine?",
        "expected_keywords": ["rag", "retrieval", "document"],
    },
    {
        "query": "How do I upload a document?",
        "expected_keywords": ["upload", "file"],
    },
    {
        "query": "What databases does it use?",
        "expected_keywords": ["qdrant", "vector", "database"],
    },
]

QUICK_QUERIES = TEST_QUERIES[:1]


def search_qdrant(query: str, collection: str = "default", top_k: int = 5) -> list[dict]:
    """Search Qdrant for similar chunks."""
    try:
        from ingestion.embedder import embed_text
        from qdrant_client import QdrantClient

        # Get Qdrant client
        try:
            from api.config import settings
            url = getattr(settings, "QDRANT_URL", None) or getattr(settings, "qdrant_url", "http://localhost:6333")
            api_key = getattr(settings, "QDRANT_API_KEY", None) or getattr(settings, "qdrant_api_key", None)
            client = QdrantClient(url=url, api_key=api_key or None)
        except ImportError:
            client = QdrantClient(url="http://localhost:6333")

        # Embed query
        query_vector = embed_text([query])[0]

        # Search
        results = client.query_points(
            collection_name=collection,
            query=query_vector,
            limit=top_k,
            score_threshold=0.3,
        )

        chunks = []
        for point in results.points:
            payload = point.payload or {}
            chunks.append({
                "text": payload.get("text", ""),
                "score": point.score,
                "filename": payload.get("filename", "unknown"),
            })
        return chunks
    except Exception as e:
        print(f"    Search error: {e}")
        return []


def generate_answer(query: str, context: str) -> str:
    """Generate an answer (mock for now, or use LLM)."""
    # Check for OpenAI key
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
            from retrieval.context import build_prompt
            client = openai.OpenAI(api_key=openai_key)
            prompt = build_prompt(query, context)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
            )
            return response.choices[0].message.content
        except Exception:
            pass

    # Mock answer — just summarize the context
    return f"Based on the retrieved documents, this question relates to: {context[:200]}"


def run_tests(quick: bool = False, collection: str = "default") -> dict:
    """Run evaluation tests on the RAG pipeline."""
    queries = QUICK_QUERIES if quick else TEST_QUERIES

    print("=" * 60)
    print("  RAG ENGINE — EVALUATION RUNNER")
    print("=" * 60)
    print(f"  Collection: {collection}")
    print(f"  Test queries: {len(queries)}")
    print("=" * 60)

    all_results = []

    for i, test in enumerate(queries, 1):
        query = test["query"]
        expected = test.get("expected_keywords", [])

        print(f"\n  Test {i}: '{query}'")
        print(f"  Expected keywords: {expected}")

        # Step 1: Search
        chunks = search_qdrant(query, collection)
        print(f"    Retrieved: {len(chunks)} chunks")

        if not chunks:
            print("    ⚠️ No chunks retrieved (collection empty?)")
            continue

        # Step 2: Generate answer
        context = " ".join([c.get("text", "") for c in chunks])
        answer = generate_answer(query, context)

        # Step 3: Evaluate
        scores = run_evaluation(query, chunks, answer)
        print(f"    Relevance: {scores['relevance']:.3f}")
        print(f"    Faithfulness: {scores['faithfulness']:.3f}")
        print(f"    Completeness: {scores['completeness']:.3f}")

        # Keyword coverage
        answer_lower = answer.lower()
        covered = [kw for kw in expected if kw in answer_lower]
        coverage = len(covered) / len(expected) if expected else 1.0
        print(f"    Keyword coverage: {coverage:.0%}")

        all_results.append({
            "query": query,
            **scores,
            "keyword_coverage": coverage,
        })

    # Summary
    print("\n" + "=" * 60)
    print("  EVALUATION SUMMARY")
    print("=" * 60)

    if all_results:
        avg_relevance = sum(r["relevance"] for r in all_results) / len(all_results)
        avg_faithful = sum(r["faithfulness"] for r in all_results) / len(all_results)
        avg_complete = sum(r["completeness"] for r in all_results) / len(all_results)
        avg_coverage = sum(r["keyword_coverage"] for r in all_results) / len(all_results)

        print(f"  Avg Relevance:     {avg_relevance:.3f}")
        print(f"  Avg Faithfulness:  {avg_faithful:.3f}")
        print(f"  Avg Completeness:  {avg_complete:.3f}")
        print(f"  Avg Keyword Cov:   {avg_coverage:.0%}")
        print("=" * 60)
    else:
        print("  No tests completed (collection empty?)")
        print("=" * 60)

    return {
        "results": all_results,
        "total_tests": len(queries),
        "collection": collection,
    }


if __name__ == "__main__":
    quick = "--quick" in sys.argv
    run_tests(quick=quick)
