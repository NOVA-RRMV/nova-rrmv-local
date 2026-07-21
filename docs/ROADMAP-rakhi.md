# Rakhi — Your Roadmap

> Document Ingestion — making files readable by the system

---

## Phase 1: Foundation (Weeks 1-3)

| # | Task | What to Do | Done? |
|---|------|-----------|-------|
| 1 | Project setup | Clone repo, run Docker | ⬜ |
| 2 | Learn the code | Read `ingestion/loader.py`, `chunker.py`, `embedder.py` | ⬜ |
| 3 | Test PDF loader | Try loading a real PDF with `loader.py` | ⬜ |
| 4 | Test text chunker | Try chunking a real document | ⬜ |
| 5 | Fix loader bugs | Fix any issues found during testing | ⬜ |
| 6 | Fix chunker bugs | Make sure chunks are good size | ⬜ |
| 7 | Test pipeline | Run full: load → chunk → embed | ⬜ |

**You're done when:** Any PDF/DOCX/TXT file loads, chunks, and embeds correctly.

---

## Phase 2: Core Features (Weeks 4-6)

| # | Task | What to Do | Done? |
|---|------|-----------|-------|
| 1 | Add more formats | Support .docx, .md, .html files | ⬜ |
| 2 | Better chunking | Handle tables, lists, special formatting | ⬜ |
| 3 | Metadata extraction | Store page numbers, file name, section titles | ⬜ |
| 4 | Help Viraj | Test ingestion → storage → retrieval flow | ⬜ |

**You're done when:** System handles any common file format cleanly.

---

## Phase 3: Polish + Demo (Weeks 7-9)

| # | Task | What to Do | Done? |
|---|------|-----------|-------|
| 1 | Multiple documents | Handle uploading many files at once | ⬜ |
| 2 | Large files | Handle big PDFs without crashing | ⬜ |
| 3 | Progress indicator | Show "processing..." during upload | ⬜ |
| 4 | Help with demo | Test full flow for presentation | ⬜ |

**You're done when:** System handles any file type and size gracefully.

---

## Your Branch

```bash
git checkout feature/ingestion-pipeline
```

## Your Files

```
ingestion/
├── __init__.py
├── loader.py        ← File readers (your main work)
├── chunker.py       ← Text splitter (your main work)
├── embedder.py      ← Text to numbers
└── pipeline.py      ← Connects everything
```

## How to Test Your Code

```python
# Test the loader
from ingestion.loader import load_document
text = load_document("test.pdf")
print(text[:500])

# Test the chunker
from ingestion.chunker import chunk_text
chunks = chunk_text(text, chunk_size=500)
print(f"Got {len(chunks)} chunks")

# Test the pipeline
from ingestion.pipeline import ingest_document
result = ingest_document("test.pdf")
print(result)
```

## Daily Check-in

- [ ] Pulled latest from develop?
- [ ] Working on your branch only?
- [ ] Pushed code before end of day?
- [ ] Tested your code before pushing?
