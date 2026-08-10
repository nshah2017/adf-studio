# TaskBoard: instructions for AI agents

TaskBoard is a task tracker: React (Vite) frontend in frontend/, FastAPI
backend in backend/, persistence as JSON on the file system in data/.

## How work happens here (the contributor model)
- Every task starts from an issue created with the "Agent task" template,
  which requires inputs, outputs, and success criteria before any agent runs.
- Plan before acting. Non-trivial tasks produce a plan artifact in plans/
  (copy plans/PLAN_TEMPLATE.md) and get plan approval before implementation.
- One task per pull request. Small, reviewable diffs.
- All agent work lands on copilot/ branches as draft PRs, passes CI and
  Copilot code review, then human review. No exceptions.

## Commands
- Backend: cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8000
- Backend tests: cd backend && python -m pytest tests/ -q  (must pass before any PR is marked ready)
- Frontend: cd frontend && npm install && npm run dev

## Conventions
- Decisions with lasting consequences get an ADR in docs/adr/ (copy the format
  of 0001). Read existing ADRs before proposing architecture changes.
- Do not introduce a database, ORM, or external service without an approved
  ADR superseding 0001.
- Never commit anything into data/ except a reset []: it is runtime state.
- Never touch files outside the scope named in the task issue.
