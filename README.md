# adf-studio: agentic development tutorial repo

A small TaskBoard app (React + FastAPI + file storage) wired with everything
needed to develop it USING AI agents on GitHub: an agent roster, instruction
hierarchy, plan templates, ADRs, CI gates, an agent-executing Actions
workflow, and a natural-language agentic workflow.

The point is not the app. The point is the workflow around it.

Start here: docs/TUTORIAL.md
Labs (fill-in exercises): labs/README.md, checked by scripts/verify_labs.py, answers in solutions/

Quick start (the app itself):
  cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8000
  cd frontend && npm install && npm run dev     # http://localhost:5173
  cd backend && python -m pytest tests/ -q
