"""FastAPI router for Week 1 (delegates to WeekRegistry)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.registry import week_registry
from app.routers.scoring import get_current_student
from app.routers.weeks import (
    CodeSubmissionRequest,
    QuizSubmissionRequest,
    check_quiz_answers,
    get_week_progress_data,
    mark_theory_complete,
    render_week_page,
    run_practice_task_code,
)
from app.services.scoring import ScoringService

router = APIRouter(tags=["Week 1"])


def build_platform_context(request: Request, db: Session) -> dict[str, Any]:
    """Build template context for Week 1 via WeekRegistry."""
    mod = week_registry.get(1)
    if not mod:
        raise RuntimeError("Week 1 module not registered")
    student = get_current_student(request, db)
    progress = ScoringService.get_progress_summary(db, student.id, week_number=1)
    return mod.build_context(student=student, progress=progress, request=request)


@router.get("/week1", response_class=HTMLResponse)
def week1_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """Render Week 1 learning platform."""
    return render_week_page(1, request, db)


@router.get("/api/week1/progress")
def get_week1_progress(request: Request, db: Session = Depends(get_db)) -> dict[str, Any]:
    """Return student progress for Week 1 (strictly read-only)."""
    return get_week_progress_data(1, request, db)


@router.post("/api/week1/practice/{task_id}/run")
def run_practice_task(
    task_id: str,
    payload: CodeSubmissionRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Execute student code for a Week 1 practice task."""
    return run_practice_task_code(1, task_id, payload, request, db)


@router.post("/api/week1/quiz/check")
def check_quiz(
    payload: QuizSubmissionRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Evaluate Week 1 quiz submission."""
    return check_quiz_answers(1, payload, request, db)


@router.post("/api/week1/quiz/evaluate")
def evaluate_quiz_endpoint(
    payload: QuizSubmissionRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Alias for check_quiz endpoint for backward compatibility."""
    return check_quiz_answers(1, payload, request, db)


@router.post("/api/week1/theory/complete")
def complete_theory_endpoint(
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Mark Week 1 theory as completed."""
    return mark_theory_complete(1, request, db)
