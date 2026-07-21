# Megha — Your Roadmap

> Dashboard UI — making it look good and easy to use

---

## Phase 1: Foundation (Weeks 1-3)

| # | Task | What to Do | Done? |
|---|------|-----------|-------|
| 1 | Project setup | Clone repo, run Docker | ⬜ |
| 2 | Learn Streamlit | Read Streamlit docs, try examples | ⬜ |
| 3 | Basic UI | Create a simple page with title + text input | ⬜ |
| 4 | Chat layout | Build chat-style message display | ⬜ |
| 5 | Connect API | Make UI talk to Mrity's API (localhost:8000) | ⬜ |

**You're done when:** You can type a question in the UI and see a response (even if placeholder).

---

## Phase 2: Core Features (Weeks 4-6)

| # | Task | What to Do | Done? |
|---|------|-----------|-------|
| 1 | Chat interface | Working chat: type question → see answer | ⬜ |
| 2 | File upload | Drag-and-drop upload page in sidebar | ⬜ |
| 3 | Source display | Show which documents the answer came from | ⬜ |
| 4 | Collections | Dropdown to select which docs to search | ⬜ |
| 5 | Error messages | Show friendly errors (not crashes) | ⬜ |
| 6 | Loading spinners | Show "Searching..." while waiting | ⬜ |

**You're done when:** Full chat interface works with upload + sources + errors.

---

## Phase 3: Polish + Demo (Weeks 7-9)

| # | Task | What to Do | Done? |
|---|------|-----------|-------|
| 1 | Colors & theme | Make it look professional | ⬜ |
| 2 | Responsive | Works on different screen sizes | ⬜ |
| 3 | History | Show previous questions/answers | ⬜ |
| 4 | Welcome page | Nice landing page with project description | ⬜ |
| 5 | Demo ready | Make it look presentation-ready | ⬜ |

**You're done when:** Dashboard looks professional and demo-ready.

---

## Your Branch

```bash
git checkout feature/dashboard
```

## Your Files

```
dashboard/
└── app.py           ← Your main Streamlit app
```

## How to Run Your Code

```bash
# Start just the dashboard
streamlit run dashboard/app.py

# Or with Docker (starts everything)
docker-compose up dashboard
```

## How to Test Your Code

```bash
# 1. Start the API first
docker-compose up backend

# 2. In another terminal, start dashboard
streamlit run dashboard/app.py

# 3. Open http://localhost:8501
# 4. Try uploading a file and asking a question
```

## Daily Check-in

- [ ] Pulled latest from develop?
- [ ] Working on your branch only?
- [ ] Pushed code before end of day?
- [ ] Tested UI looks correct before pushing?
