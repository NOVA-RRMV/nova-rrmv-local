# RegEngine Roadmap — Easy Guide

> Simple, step-by-step plan for our final year project.
> No jargon. Just what to do and when.

---

## What Are We Building?

We are building a **RAG Engine** — a system that:
1. Takes your documents (PDF, Word, text files)
2. Reads them and breaks them into small pieces
3. Stores those pieces in a database
4. When you ask a question, it finds the best pieces
5. Gives you an answer with sources

Think of it like a **smart search engine for your own documents**.

---

## Team Roles (5 Members — Everyone is Equal)

| Who | Focus Area | What They Do |
|-----|-----------|-------------|
| **Mrity** | API + Coordination | Sets up the server, connects everyone's work, keeps things on track |
| **Rakhi** | Document Ingestion | Takes files and makes them readable by the system. Handles PDF, Word, text files. |
| **Viraj** | Search Engine | Builds the search part. When someone asks a question, finds the best matching pieces. |
| **Megha** | Dashboard (UI) | Builds the website where users type questions and see answers. Makes it look good. |
| **Everyone** | Testing + MCP | We all test. We all review each other's code. We all make it better. |

---

## Timeline — 3 Phases

### Phase 1: Foundation (Weeks 1-3)
> "Get the basics working"

**Goal:** Upload a PDF → system reads it → stores it in database

| Task | Who | Days | Done? |
|------|-----|------|-------|
| Set up Docker on everyone's computer | All | Day 1 | ⬜ |
| Clone the repo and run it | All | Day 1 | ⬜ |
| Understand the code structure | All | Day 2 | ⬜ |
| Build document loader (PDF reader) | Rakhi | Day 3-5 | ⬜ |
| Build text chunker (split into pieces) | Rakhi | Day 6-8 | ⬜ |
| Set up Qdrant database | Viraj | Day 3-5 | ⬜ |
| Build embedding pipeline (text → numbers) | Viraj | Day 6-8 | ⬜ |
| Connect loader → chunker → database | Rakhi + Viraj | Day 9-10 | ⬜ |
| Basic API endpoints working | Mrity | Day 5-10 | ⬜ |
| First integration test (upload → stored) | All | Day 10 | ⬜ |

**Phase 1 Checkpoint:**
- [ ] Can upload a PDF through the API
- [ ] File gets stored in Qdrant database
- [ ] Database shows the document chunks

---

### Phase 2: Core Features (Weeks 4-6)
> "Make it actually useful"

**Goal:** Ask a question → get an answer with sources

| Task | Who | Days | Done? |
|------|-----|------|-------|
| Build vector search (find similar chunks) | Viraj | Day 1-5 | ⬜ |
| Build context assembly (format results) | Viraj | Day 6-7 | ⬜ |
| Connect LLM for answer generation | Mrity | Day 3-7 | ⬜ |
| Build chat interface (Streamlit) | Megha | Day 1-7 | ⬜ |
| Add file upload page | Megha | Day 3-5 | ⬜ |
| Add source display (show where answer came from) | Megha | Day 6-7 | ⬜ |
| End-to-end test (upload → ask → answer) | All | Day 8-10 | ⬜ |
| Write evaluation metrics | All | Day 5-10 | ⬜ |

**Phase 2 Checkpoint:**
- [ ] Can upload documents through the website
- [ ] Can ask questions and get answers
- [ ] Answers show which documents they came from
- [ ] Search finds relevant content

---

### Phase 3: Polish + Demo (Weeks 7-9)
> "Make it presentable and ready to show"

**Goal:** Professional demo-ready system

| Task | Who | Days | Done? |
|------|-----|------|-------|
| UI polish (colors, layout, responsive) | Megha | Day 1-5 | ⬜ |
| Error handling (what if upload fails?) | Mrity | Day 1-3 | ⬜ |
| Performance testing (how fast?) | All | Day 1-5 | ⬜ |
| MCP server (connect to AI tools) | All | Day 3-7 | ⬜ |
| Multiple document support | Rakhi | Day 3-5 | ⬜ |
| Search improvements (better results) | Viraj | Day 3-7 | ⬜ |
| Demo video / presentation | All | Day 8-10 | ⬜ |
| Final testing | All | Day 8-10 | ⬜ |
| Report / documentation | Mrity | Day 7-10 | ⬜ |

**Phase 3 Checkpoint:**
- [ ] System handles errors gracefully
- [ ] Works with multiple documents
- [ ] Fast enough for demo
- [ ] Demo video ready
- [ ] Report written

---

## How We Work Together

### Daily Rules
1. **Morning:** Check what you need to do today
2. **Work:** Code on YOUR branch only
3. **Evening:** Push your code to GitHub before going to sleep
4. **Weekly:** Saturday meeting — everyone shows what they built

### Git Rules (Very Important!)
```
❌ NEVER push directly to main or develop
✅ Always work on your feature branch
✅ Always create a Pull Request when done
✅ Wait for Mrity to review and approve
```

### How to Start Your Day
```bash
# 1. Get latest code
git checkout develop
git pull origin develop

# 2. Go to your branch
git checkout feature/your-branch-name

# 3. Merge latest develop into your branch
git merge develop

# 4. Start coding!
```

### When You Finish a Task
```bash
# 1. Save your work
git add .
git commit -m "feat: describe what you did"

# 2. Push to GitHub
git push origin feature/your-branch-name

# 3. Go to GitHub and create a Pull Request
#    Base: develop ← Compare: feature/your-branch-name

# 4. Wait for Mrity to review
```

---

## Commands Cheat Sheet

| What | Command |
|------|---------|
| Start Docker | `docker-compose up --build` |
| Stop Docker | `docker-compose down` |
| Check status | `docker-compose ps` |
| View logs | `docker-compose logs -f backend` |
| Run tests | `pytest` |
| See branches | `git branch -a` |
| Switch branch | `git checkout branch-name` |
| Pull latest | `git pull origin develop` |
| Push code | `git push origin your-branch` |

---

## Branch Names

| Person | Branch |
|--------|--------|
| Mrity | `feature/api-layer` |
| Rakhi | `feature/ingestion-pipeline` |
| Viraj | `feature/retrieval-engine` |
| Megha | `feature/dashboard` |

---

## Help! I'm Stuck

1. **Can't run Docker?** → Ask Mrity, probably need to install something
2. **Code doesn't work?** → Check the error message, Google it, then ask
3. **Git confused?** → Don't panic. Run `git status` to see what's happening
4. **Don't know what to do?** → Check this roadmap, pick your next task
5. **Something else?** → Ask in the team group

---

## Important Links

| What | Link |
|------|------|
| GitHub Repo | https://github.com/NOVA-RRMV/nova-rrmv-local |
| API Docs (when running) | http://localhost:8000/docs |
| Dashboard (when running) | http://localhost:8501 |
| Qdrant Dashboard | http://localhost:6333/dashboard |

---

*Last updated: July 2026*
*Team: Nova RRMV*
