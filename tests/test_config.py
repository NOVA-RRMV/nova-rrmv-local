"""Tests for api/config.py — Settings initialization and defaults."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from api.config import settings, Settings

def test_settings_class_exists():
    assert Settings is not None

def test_qdrant_url_present_and_default():
    # After mock patch in conftest, should have the mocked value or default
    assert hasattr(settings, "QDRANT_URL")
    # Default is localhost:6333 when not overridden
    assert "6333" in settings.QDRANT_URL or settings.QDRANT_URL == "http://localhost:6333"

def test_default_chunk_size():
    assert settings.CHUNK_SIZE == 500

def test_default_chunk_overlap():
    assert settings.CHUNK_OVERLAP == 50

def test_default_embedding_model():
    assert settings.EMBEDDING_MODEL == "all-MiniLM-L6-v2"

def test_default_top_k():
    assert settings.TOP_K == 5

def test_default_similarity_threshold():
    assert settings.SIMILARITY_THRESHOLD == 0.5

def test_upload_dir_exists():
    import os
    assert os.path.isdir(settings.UPLOAD_DIR) or settings.UPLOAD_DIR == "uploads"

def test_app_env_default_or_mocked():
    assert settings.APP_ENV in ("development", "testing", "production")

