"""Main FastAPI application entry point."""

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.database.session import engine, get_db, init_db
from app.routers import health_router, runner_router, scoring, week1, week2, week3, weeks

templates = Jinja2Templates(directory=str(settings.templates_dir))


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan managing DB initialization and WAL configuration."""
    settings.static_dir.mkdir(parents=True, exist_ok=True)
    settings.templates_dir.mkdir(parents=True, exist_ok=True)
    init_db()

    # Enable WAL mode and busy timeout for concurrent safety in SQLite
    with engine.connect() as conn:
        try:
            conn.execute(text("PRAGMA journal_mode=WAL;"))
            conn.execute(text("PRAGMA busy_timeout=5000;"))
            conn.commit()
        except Exception:
            pass

    yield


is_public = os.environ.get("PUBLIC_MODE", "0").lower() in ("1", "true")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url=None if is_public else "/docs",
    redoc_url=None if is_public else "/redoc",
)

# Mount static files
settings.static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")

# Include routers
app.include_router(health_router)
app.include_router(runner_router)
app.include_router(scoring.router)
app.include_router(weeks.router)
app.include_router(week1.router)
app.include_router(week2.router)
app.include_router(week3.router)


@app.get("/", response_class=HTMLResponse)
def index(
    request: Request,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    """Render the unified Web-OOP learning platform (defaults to Week 1)."""
    return weeks.render_week_page(1, request, db)
