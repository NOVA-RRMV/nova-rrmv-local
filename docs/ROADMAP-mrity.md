# Mrity — Your Roadmap

> API + Coordination — keeping everything connected

---

## Phase 1: Foundation (Weeks 1-3)

| # | Task | What to Do | Done? |
|---|------|-----------|-------|
| 1 | Project setup | Help everyone clone repo and run Docker | ⬜ |
| 2 | Config setup | Create `.env` file with API keys | ⬜ |
| 3 | API skeleton | Write FastAPI routes in `api/main.py` | ⬜ |
| 4 | Connect ingestion | Wire up `/api/upload` to Rakhi's loader | ⬜ |
| 5 | Connect retrieval | Wire up `/api/query` to Viraj's search | ⬜ |
| 6 | Integration test | Test: upload PDF → stored in Qdrant | ⬜ |

**You're done when:** A PDF can be uploaded through API and stored in database.

---

## Phase 2: Core Features (Weeks 4-6)

| # | Task | What to Do | Done? |
|---|------|-----------|-------|
| 1 | LLM connection | Add OpenAI/Ollama for answer generation | ⬜ |
| 2 | Query endpoint | Build `/api/query` — question → answer with sources | ⬜ |
| 3 | Error handling | Make sure API returns useful error messages | ⬜ |
| 4 | API docs | Keep `/docs` endpoint updated | ⬜ |
| 5 | Help Megha | Connect her dashboard to your API | ⬜ |

**You're done when:** Ask a question → get a real answer with source citations.

---

## Phase 3: Polish + Demo (Weeks 7-9)

| # | Task | What to Do | Done? |
|---|------|-----------|-------|
| 1 | Error handling | Handle: no file, bad format, empty DB, API down | ⬜ |
| 2 | Rate limiting | Prevent spam uploads/queries | ⬜ |
| 3 | Help everyone | Review PRs, fix integration issues | ⬜ |
| 4 | Demo prep | Make sure full flow works end-to-end | ⬜ |
| 5 | Report | Write project report/documentation | ⬜ |

**You're done when:** Demo runs smoothly, report is written.

---

## Your Branch

```bash
git checkout feature/api-layer
```

## Your Files

```
api/
├── __init__.py
├── config.py        ← Settings (you maintain this)
├── main.py          ← Routes (your main work)
└── models.py        ← Data schemas
```

## Daily Check-in

- [ ] Pulled latest from develop?
- [ ] Working on your branch only?
- [ ] Pushed code before end of day?
- [ ] Reviewed anyone's PR who asked?
