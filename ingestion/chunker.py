"""Text chunker — split documents into manageable pieces."""

from typing import Optional


def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    separators: Optional[list[str]] = None,
) -> list[dict]:
    """Split text into overlapping chunks.

    Args:
        text: The full document text.
        chunk_size: Target size of each chunk (in characters).
        chunk_overlap: Overlap between consecutive chunks.
        separators: Priority list of separators to split on.

    Returns:
        List of chunk dicts with 'text', 'start', 'end' keys.
    """
    if separators is None:
        separators = ["\n\n", "\n", ". ", " ", ""]

    chunks = []
    start = 0

    while start < len(text):
        # Find the best end position for this chunk
        end = min(start + chunk_size, len(text))

        # If we're not at the end, try to split at a separator
        if end < len(text):
            best_end = end
            for sep in separators:
                # Look for the last occurrence of the separator in the chunk
                pos = text.rfind(sep, start, end)
                if pos > start:
                    best_end = pos + len(sep)
                    break
            end = best_end

        chunk_text_content = text[start:end].strip()
        if chunk_text_content:
            chunks.append({
                "text": chunk_text_content,
                "start": start,
                "end": end,
                "index": len(chunks),
            })

        # Move forward with overlap
        start = end - chunk_overlap
        if start <= (chunks[-1]["start"] if chunks else 0):
            start = end

    return chunks
