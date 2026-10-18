"""Main FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings
from app.database.session import get_db, init_db
from app.routers import health_router, runner_router, week1, week2

templates = Jinja2Templates(directory=str(settings.templates_dir))


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan managing DB initialization."""
    settings.static_dir.mkdir(parents=True, exist_ok=True)
    settings.templates_dir.mkdir(parents=True, exist_ok=True)
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Mount static files
settings.static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")

# Include routers
app.include_router(health_router)
app.include_router(runner_router)
app.include_router(week1.router)
app.include_router(week2.router)


@app.get("/", response_class=HTMLResponse)
def index(
    request: Request,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    """Render the unified Web-OOP learning platform."""
    ctx = week1.build_platform_context(request, db)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=ctx,
    )

