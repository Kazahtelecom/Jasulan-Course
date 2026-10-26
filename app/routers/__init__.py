"""Routers package."""

from app.routers.health import router as health_router
from app.routers.runner import router as runner_router
from app.routers import week1, week2, week3

__all__ = ["health_router", "runner_router", "week1", "week2", "week3"]

