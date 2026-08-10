# ADR 0002: Add a created-at timestamp to tasks

Status: accepted
Date: 2026-08-08

## Context
Tasks need a creation time for ordering and future reporting. ADR 0001 fixes
storage as a single JSON file behind app/storage.py; this ADR only extends
the record shape, it does not reopen the storage decision.

## Decision
Add a created_at field, ISO 8601 UTC (e.g. 2026-08-08T14:00:00Z), set in the
storage layer inside create_task so every write path gets it. Existing
records without the field are treated as created_at null; no backfill.

## Consequences
- Benefit: stable ordering and auditability of task creation.
- Cost: readers must tolerate null created_at on legacy records; tests cover
  both shapes.
- Future agents: set timestamps only in storage.py (never in endpoints), and
  read this ADR plus 0001 before any change to the task record shape.
