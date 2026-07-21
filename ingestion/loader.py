"""Document loaders — read different file formats into text."""

import os
from pathlib import Path


def load_document(file_path: str) -> str:
    """Load a document and return its text content.

    Supports: .txt, .md, .pdf, .docx

    Args:
        file_path: Path to the document.

    Returns:
        Extracted text content.

    Raises:
        ValueError: If file format is not supported.
    """
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension in [".txt", ".md"]:
        return _load_text(file_path)
    elif extension == ".pdf":
        return _load_pdf(file_path)
    elif extension == ".docx":
        return _load_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {extension}")


def _load_text(file_path: str) -> str:
    """Load plain text files."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def _load_pdf(file_path: str) -> str:
    """Load PDF files using pypdf."""
    from pypdf import PdfReader

    reader = PdfReader(file_path)
    text_parts = []
    for page in reader.pages:
        text_parts.append(page.extract_text())
    return "\n\n".join(text_parts)


def _load_docx(file_path: str) -> str:
    """Load Word documents using python-docx."""
    from docx import Document

    doc = Document(file_path)
    return "\n\n".join([para.text for para in doc.paragraphs if para.text])
