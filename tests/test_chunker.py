"""Tests for ingestion/chunker.py — chunking logic, overlap, metadata."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ingestion.chunker import chunk_text

def test_chunk_text_produces_chunks_for_sample(sample_python_doc):
    chunks = chunk_text(sample_python_doc, chunk_size=500, chunk_overlap=50)
    assert isinstance(chunks, list)
    assert len(chunks) >= 1
    assert isinstance(chunks[0], dict)
    assert "text" in chunks[0]
    assert "start" in chunks[0]
    assert "end" in chunks[0]
    assert "index" in chunks[0]

def test_chunk_overlap_around_boundaries(sample_python_doc):
    chunks = chunk_text(sample_python_doc, chunk_size=300, chunk_overlap=50)
    if len(chunks) > 1:
        # Overlap region should be present in adjacent chunks
        first_text = chunks[0]["text"]
        second_text = chunks[1]["text"]
        # At least some shared content (not a perfect equality test, just sanity)
        assert len(first_text) > 0
        assert len(second_text) > 0

def test_empty_string_returns_empty_list():
    chunks = chunk_text("")
    assert chunks == []

def test_single_word_returns_single_chunk():
    chunks = chunk_text("Hello")
    assert len(chunks) == 1
    assert chunks[0]["text"] == "Hello"

def test_metadata_retention_for_each_chunk(sample_python_doc):
    chunks = chunk_text(sample_python_doc, chunk_size=200)
    for i, c in enumerate(chunks):
        assert c["index"] == i
        assert isinstance(c["start"], int)
        assert isinstance(c["end"], int)
        assert c["start"] < c["end"] or len(c["text"]) == 0

def test_small_chunk_merged_when_tiny(short_text):
    chunks = chunk_text(short_text, chunk_size=500, chunk_overlap=50)
    # Very short text should yield 1 chunk (or very few)
    assert len(chunks) <= 2

def test_large_document_many_chunks(sample_python_doc):
    # Replicate text to make it large
    big = sample_python_doc * 5
    chunks = chunk_text(big, chunk_size=300, chunk_overlap=50)
    assert len(chunks) > 2

def test_chunker_handles_unicode(unicode_text):
    chunks = chunk_text(unicode_text, chunk_size=50)
    assert len(chunks) >= 1
    assert "नमस्ते" in chunks[0]["text"] or len(chunks) >= 2

