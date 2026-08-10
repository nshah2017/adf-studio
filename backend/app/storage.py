"""File-system storage for tasks. Deliberately simple: one JSON file.

See docs/adr/0001-file-storage.md for why file storage was chosen (and the
conditions under which that decision should be revisited).
"""
import json
import uuid
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "tasks.json"


def _read() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text() or "[]")


def _write(tasks: list[dict]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(tasks, indent=2))


def list_tasks() -> list[dict]:
    return _read()


def create_task(title: str) -> dict:
    tasks = _read()
    task = {"id": str(uuid.uuid4())[:8], "title": title, "done": False}
    tasks.append(task)
    _write(tasks)
    return task


def toggle_task(task_id: str) -> dict | None:
    tasks = _read()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = not t["done"]
            _write(tasks)
            return t
    return None
