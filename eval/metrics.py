"""Evaluation metrics — measure RAG quality."""


def relevance_score(query: str, chunks: list[dict]) -> float:
    """Score how relevant retrieved chunks are to the query.

    Uses the similarity scores from Qdrant as a baseline.

    Args:
        query: The original query.
        chunks: Retrieved chunks with 'score' key.

    Returns:
        Average relevance score (0.0 to 1.0).
    """
    if not chunks:
        return 0.0
    scores = [c.get("score", 0) for c in chunks]
    return sum(scores) / len(scores)


def faithfulness_score(answer: str, context: str) -> float:
    """Check if the answer is grounded in the context.

    Simple heuristic: check what percentage of answer sentences
    can be found or paraphrased in the context.

    Args:
        answer: The generated answer.
        context: The context used to generate it.

    Returns:
        Faithfulness score (0.0 to 1.0).
    """
    # Simple word-overlap heuristic
    answer_words = set(answer.lower().split())
    context_words = set(context.lower().split())

    if not answer_words:
        return 0.0

    overlap = answer_words & context_words
    return len(overlap) / len(answer_words)


def completeness_score(answer: str, question: str) -> float:
    """Check if the answer addresses the question.

    Simple heuristic: check if key question words appear in the answer.

    Args:
        answer: The generated answer.
        question: The original question.

    Returns:
        Completeness score (0.0 to 1.0).
    """
    question_words = set(question.lower().split()) - {"what", "how", "why", "when", "where", "who", "is", "are", "the", "a", "an", "to", "in", "of", "and", "or"}
    answer_words = set(answer.lower().split())

    if not question_words:
        return 1.0

    covered = question_words & answer_words
    return len(covered) / len(question_words)


def run_evaluation(query: str, chunks: list[dict], answer: str) -> dict:
    """Run full evaluation on a query-answer pair.

    Args:
        query: The original query.
        chunks: Retrieved chunks.
        answer: The generated answer.

    Returns:
        Dict with all evaluation metrics.
    """
    context = " ".join([c.get("text", "") for c in chunks])

    return {
        "relevance": relevance_score(query, chunks),
        "faithfulness": faithfulness_score(answer, context),
        "completeness": completeness_score(answer, query),
    }
