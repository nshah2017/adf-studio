# ADR 0001: Store tasks as a JSON file on the file system

Status: accepted
Date: 2026-08-01

## Context
TaskBoard is a teaching application. The goal is to demonstrate agentic
development concepts, not persistence engineering. The data set is one small
list owned by one process.

## Decision
Persist tasks in data/tasks.json through the single storage module
backend/app/storage.py. No database, no ORM, no external service.

## Consequences
- Setup stays at zero configuration, which keeps agent environments simple.
- No concurrency safety. Acceptable for a single-user teaching app.
- Any agent or human proposing a database must write a superseding ADR and
  get it approved BEFORE implementation. Agents: read this file before
  planning storage changes. This is long-term memory doing its job.
