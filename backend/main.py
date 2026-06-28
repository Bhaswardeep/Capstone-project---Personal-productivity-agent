"""FastAPI application entry point."""

from fastapi import FastAPI

from backend.api.auth import router as auth_router
from backend.database.database import create_database

app = FastAPI(title="Personal Productivity Agent")

create_database()

app.include_router(auth_router)
