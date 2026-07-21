# Git Workflow — Nova RRMV

## Branch Strategy

```
main (protected)
  ├── develop (integration branch)
  │     ├── feature/ingestion-pipeline
  │     ├── feature/retrieval-engine
  │     ├── feature/api-layer
  │     ├── feature/dashboard
  │     ├── feature/eval-pipeline
  │     └── feature/mcp-server
  └── hotfix/xxx (emergency fixes)
```

## Rules

1. **Never push directly to `main`** — it's protected
2. **`develop`** is the integration branch — all features merge here first
3. **Each person works on their own feature branch**
4. **Always create a PR** to merge — even for small changes
5. **At least 1 review** before merging to develop
6. **Mrity (coordinator)** merges develop → main for releases

## Day-to-Day Workflow

```bash
# 1. Start your day — get latest changes
git checkout develop
git pull origin develop

# 2. Create your feature branch (if not already on it)
git checkout -b feature/your-feature-name

# 3. Do your work, commit often
git add .
git commit -m "feat: add document loader for PDF files"

# 4. Push and create a PR
git push origin feature/your-feature-name
# Then create PR on GitHub: feature/your-feature-name → develop

# 5. After review, merge to develop
# Then delete your feature branch
git branch -d feature/your-feature-name
```

## Commit Message Format

Use **Conventional Commits**:

```
feat:     new feature
fix:      bug fix
docs:     documentation only
style:    formatting, no code change
refactor: code restructure, no feature change
test:     adding tests
chore:    build, config, dependencies
```

Examples:
```
feat: add PDF document loader
fix: handle empty chunks in retrieval
docs: update architecture diagram
test: add unit tests for chunker
chore: update docker-compose with health checks
```

## PR Template

```markdown
## What does this PR do?
Brief description.

## How to test?
Steps to verify.

## Screenshots (if UI change)
Before → After

## Checklist
- [ ] Code works locally
- [ ] No hardcoded values
- [ ] Comments added for complex logic
- [ ] Updated docs if needed
```

## Who Works on What

| Member | Feature Branch | Focus Area |
|--------|---------------|--------|
| Mrity | `feature/api-layer` | API + Integration |
| Rakhi | `feature/ingestion-pipeline` | Document processing |
| Viraj | `feature/retrieval-engine` | Vector search |
| Megha | `feature/dashboard` | Web UI |

## Timeline (Suggested)

| Week | Milestone |
|------|-----------|
| 1-2 | Project setup, Docker running, everyone can contribute |
| 3-4 | Ingestion pipeline working (upload PDF → stored in Qdrant) |
| 5-6 | Retrieval working (ask question → get relevant chunks) |
| 7-8 | API complete, dashboard MVP |
| 9-10 | Eval pipeline, MCP server |
| 11-12 | Integration, testing, demo prep |
