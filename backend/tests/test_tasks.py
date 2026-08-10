"""API tests. These are the machine-checkable half of every agent task's
success criteria: an agent PR that breaks them fails the required check."""
from fastapi.testclient import TestClient

from app import storage
from app.main import app

client = TestClient(app)


def setup_function():
    storage._write([])  # reset the file store between tests


def test_list_starts_empty():
    assert client.get("/api/tasks").json() == []


def test_create_and_list():
    r = client.post("/api/tasks", json={"title": "write tutorial"})
    assert r.status_code == 201
    assert r.json()["title"] == "write tutorial"
    assert len(client.get("/api/tasks").json()) == 1


def test_create_rejects_empty_title():
    assert client.post("/api/tasks", json={"title": "  "}).status_code == 422


def test_toggle():
    tid = client.post("/api/tasks", json={"title": "x"}).json()["id"]
    assert client.patch(f"/api/tasks/{tid}").json()["done"] is True
    assert client.patch(f"/api/tasks/{tid}").json()["done"] is False


def test_toggle_unknown_404():
    assert client.patch("/api/tasks/nope").status_code == 404
