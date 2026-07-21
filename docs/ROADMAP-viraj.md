# Viraj — Your Roadmap

> Search Engine — finding the right answers

---

## Phase 1: Foundation (Weeks 1-3)

| # | Task | What to Do | Done? |
|---|------|-----------|-------|
| 1 | Project setup | Clone repo, run Docker | ⬜ |
| 2 | Learn Qdrant | Read Qdrant docs, understand vectors | ⬜ |
| 3 | Set up Qdrant | Make sure Qdrant runs in Docker | ⬜ |
| 4 | Create collection | Set up a collection in Qdrant for our docs | ⬜ |
| 5 | Store vectors | Take embedded chunks from Rakhi, store in Qdrant | ⬜ |
| 6 | Test storage | Upload a PDF, verify it's in Qdrant | ⬜ |

**You're done when:** Documents can be stored in Qdrant and retrieved.

---

## Phase 2: Core Features (Weeks 4-6)

| # | Task | What to Do | Done? |
|---|------|-----------|-------|
| 1 | Vector search | Build search: question → find similar chunks | ⬜ |
| 2 | Top-K results | Return best 5 matches | ⬜ |
| 3 | Similarity threshold | Ignore low-quality matches | ⬜ |
| 4 | Context assembly | Format results for LLM (in `context.py`) | ⬜ |
| 5 | Test search | Try 10 different questions, check quality | ⬜ |

**You're done when:** Ask a question → system finds the 5 most relevant chunks.

---

## Phase 3: Polish + Demo (Weeks 7-9)

| # | Task | What to Do | Done? |
|---|------|-----------|-------|
| 1 | Better search | Improve results quality (tune parameters) | ⬜ |
| 2 | Reranking | Add second-pass ranking for better results | ⬜ |
| 3 | Multi-collection | Search across multiple document sets | ⬜ |
| 4 | Speed optimization | Make search faster | ⬜ |
| 5 | Help with demo | Test search for presentation | ⬜ |

**You're done when:** Search returns accurate, fast results every time.

---

## Your Branch

```bash
git checkout feature/retrieval-engine
```

## Your Files

```
retrieval/
├── __init__.py
├── search.py        ← Vector search (your main work)
└── context.py       ← Format results for LLM
```

## How to Test Your Code

```python
# Test search
from retrieval.search import search_similar
results = search_similar("what is the warranty policy?", collection="default")
for r in results:
    print(f"Score: {r['score']:.2f} | {r['text'][:100]}...")

# Test context building
from retrieval.context import build_context, build_prompt
context = build_context(results)
prompt = build_prompt("what is the warranty policy?", context)
print(prompt)
```

## Daily Check-in

- [ ] Pulled latest from develop?
- [ ] Working on your branch only?
- [ ] Pushed code before end of day?
- [ ] Tested your code before pushing?
