"""TaskBoard API. Three endpoints, file-system persistence.

Run: uvicorn app.main:app --reload --port 8000  (from backend/)
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from . import storage

app = FastAPI(title="TaskBoard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskIn(BaseModel):
    title: str


@app.get("/api/tasks")
def get_tasks():
    return storage.list_tasks()


@app.post("/api/tasks", status_code=201)
def add_task(body: TaskIn):
    title = body.title.strip()
    if not title:
        raise HTTPException(status_code=422, detail="title must not be empty")
    return storage.create_task(title)


@app.patch("/api/tasks/{task_id}")
def toggle(task_id: str):
    task = storage.toggle_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    return task
