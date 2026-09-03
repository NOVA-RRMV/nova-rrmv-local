"""Pytest configuration — shared fixtures and mocks."""

import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock
import pytest

# ── Repo root on sys.path so absolute imports work ──────────────────────────
REPO_ROOT = Path(__file__).parent.parent.resolve()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


# ── Sample text fixtures ─────────────────────────────────────────────────────
@pytest.fixture
def sample_python_doc() -> str:
    """Multi-paragraph Python tutorial excerpt (~600 chars)."""
    return (
        "Python is a great programming language.\\n"
        "It supports object-oriented programming.\\n\\n"
        "You can define a class like this:\\n"
        "class MyClass:\\n"
        "    def __init__(self, value):\\n"
        "        self.value = value\\n\\n"
        "Classes can inherit from other classes.\\n"
        "Multiple inheritance is also supported.\\n\\n"
        "Error handling is done with try-except blocks.\\n"
        "You can catch specific exceptions."
    )


@pytest.fixture
def short_text() -> str:
    """Text shorter than chunk_size (<< 500 chars)."""
    return "Python is awesome."


@pytest.fixture
def empty_text() -> str:
    """Empty string."""
    return ""


@pytest.fixture
def single_line_repeat_text() -> str:
    """Pathological text: same separator repeated many times."""
    return "word. " * 200  # 1000 chars of "word. "


@pytest.fixture
def unicode_text() -> str:
    """Text with unicode characters."""
    return "नमस्ते Python 🚀 —café résumé"


@pytest.fixture
def mixed_newlines_text() -> str:
    """Text with \\n and \\n\\n separators."""
    return "Line one\nLine two\n\nLine three\nLine four\n\n\nLine five"


# ── Mock settings ─────────────────────────────────────────────────────────────
@pytest.fixture
def mock_settings():
    """Patched Settings so no real .env is needed."""
    with patch.dict(os.environ, {
        "OPENAI_API_KEY": "sk-test-key",
        "QDRANT_URL": "http://localhost:6333",
        "QDRANT_API_KEY": "",
        "APP_ENV": "testing",
        "LOG_LEVEL": "DEBUG",
    }, clear=True):
        # Re-load config so it picks up the patched env
        # (api.config reads env at import time — we mock at usage site instead)
        yield


# ── Mock Qdrant client ──────────────────────────────────────────────────────
@pytest.fixture
def mock_qdrant_client():
    """A mock QdrantClient that records calls instead of hitting the network."""
    mock = MagicMock()
    mock.get_collections.return_value = MagicMock(
        collections=[MagicMock(name="default")]
    )
    mock.query_points.return_value = MagicMock(
        points=[
            MagicMock(
                id="pt-1",
                score=0.92,
                payload={"text": "Python classes are great.", "filename": "test.txt"},
            ),
            MagicMock(
                id="pt-2",
                score=0.87,
                payload={"text": "Object-oriented programming in Python.", "filename": "test.txt"},
            ),
        ]
    )
    return mock


# ── Mock SentenceTransformer ─────────────────────────────────────────────────
@pytest.fixture
def mock_embedder(monkeypatch):
    """Stub embed_text so no real model is loaded."""
    call_record = []

    def fake_embed_text(texts, model_name="all-MiniLM-L6-v2"):
        call_record.append((texts, model_name))
        # Return deterministic 384-dim vectors (list of lists of floats)
        dim = 384
        return [[0.1] * dim for _ in texts]

    def fake_embed_query(query, model_name="all-MiniLM-L6-v2"):
        return [0.1] * 384

    # Patch at the source module so all code paths see it
    import ingestion.embedder as embedder_mod
    monkeypatch.setattr(embedder_mod, "embed_text", fake_embed_text)
    monkeypatch.setattr(embedder_mod, "embed_query", fake_embed_query)
    return call_record
