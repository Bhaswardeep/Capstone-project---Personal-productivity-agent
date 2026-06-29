"""FastAPI application entry point."""

from fastapi import FastAPI

from backend.api.ai import router as ai_router
from backend.api.auth import router as auth_router
from backend.api.dashboard import router as dashboard_router
from backend.api.tasks import router as tasks_router
from backend.database.database import create_database

app = FastAPI(title="Personal Productivity Agent")

create_database()

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(ai_router)
app.include_router(dashboard_router)
