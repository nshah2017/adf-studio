## Goal
Users can delete a task from the board, end to end.

## Inputs and scope
In scope: backend/app/main.py, backend/app/storage.py,
backend/tests/test_tasks.py, frontend/src/App.jsx.
Out of scope: any new dependency; any change to the storage format or
location; bulk delete; undo.

## Success criteria
1. DELETE /api/tasks/{id} returns 204 and the task no longer appears in GET /api/tasks.
2. DELETE with an unknown id returns 404.
3. pytest passes, with new tests covering both behaviors above.
4. The UI shows a delete control per task; clicking it removes the task from the list without a page reload.

## Risk level
Medium: it deletes user data, but single records with clear semantics; not
high because no bulk operations, config, or external systems are touched.
