# Dataset: Python Official Documentation (Tutorial + Selected Library Reference)

## What this is
A cleaned, plain-text subset of Python's official documentation, used as
the demo corpus for the Self-Auditing, Adaptive RAG Engine project.

## Source
- Origin: python/cpython on GitHub (same repo that generates docs.python.org)
- Original format: reStructuredText (.rst)
- License: Python Software Foundation License (see cpython repo's LICENSE)

## How it was produced
1. Sparse-cloned Doc/tutorial/ and 4 files from Doc/library/ from cpython.
2. Converted each .rst file to plain text with pandoc.
3. Script: scripts/source_documents.py (rerunnable for more docs later).

## Contents
- 21 files, ~63,000 words total
- 17 files: every chapter of The Python Tutorial
- 4 files: library reference pages (functions, collections, os.path, json)
- See MANIFEST.tsv for per-file word counts.