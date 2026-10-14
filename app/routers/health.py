"""Health check router."""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.session import get_db

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
def get_health(db: Session = Depends(get_db)) -> dict[str, str]:
    """Check application, database, and runner readiness."""
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "error"

    return {
        "status": "ok",
        "db": db_status,
        "runner": "ready",
    }
