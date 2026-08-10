# Plan: 1 delete-task

Issue: #1
Author: plan-architect (reviewed by <your handle>)
Status: approved

## Understanding
TaskBoard needs task deletion end to end. Storage stays file-based per
docs/adr/0001-file-storage.md, which this plan must not violate.
Constraint: any task that introduces a database, ORM, or external service
would violate ADR 0001 and requires a superseding ADR first.

## Task breakdown

| # | Task | Files touched | Acceptance criteria |
|---|------|---------------|---------------------|
| 1 | Add delete_task to storage and DELETE endpoint with tests | backend/app/storage.py, backend/app/main.py, backend/tests/test_tasks.py | DELETE returns 204 and removes the task; unknown id returns 404; pytest passes with new tests for both |
| 2 | Add per-task delete control in the UI | frontend/src/App.jsx | Delete control visible per task; clicking calls DELETE and the task disappears from the list; npm run build succeeds |

## Out of scope
- Bulk delete or multi-select.
- Undo/restore functionality.
- Any storage format change.

## Risks and rollback
Each task is one PR; a bad merge is reverted with a revert PR, never a
history rewrite. Task 2 depends on task 1 being merged; if task 1 is
reverted, task 2 must be reverted with it.
