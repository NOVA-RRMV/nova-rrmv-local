"""Context assembly — build LLM-ready prompts from retrieved chunks."""


def build_context(chunks: list[dict]) -> str:
    """Format retrieved chunks into a context string for the LLM.

    Args:
        chunks: List of chunks with 'text' and 'score' keys.

    Returns:
        Formatted context string.
    """
    if not chunks:
        return "No relevant context found."

    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        score = chunk.get("score", 0)
        text = chunk.get("text", "")
        context_parts.append(f"[Source {i} | Relevance: {score:.2f}]\n{text}")

    return "\n\n---\n\n".join(context_parts)


def build_prompt(question: str, context: str) -> str:
    """Build a complete prompt with context and question.

    Args:
        question: The user's question.
        context: The assembled context from retrieved chunks.

    Returns:
        Complete prompt string for the LLM.
    """
    return f"""You are a helpful assistant that answers questions based on the provided context.

INSTRUCTIONS:
- Answer the question using ONLY the provided context.
- If the context doesn't contain enough information, say "I don't have enough information to answer this question."
- Be concise and direct.
- Cite which source(s) you used.

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""
