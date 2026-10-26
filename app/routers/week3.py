"""FastAPI router for Week 3 (delegates to WeekRegistry)."""

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

router = APIRouter(tags=["Week 3"])


def build_week3_context(request: Request, db: Session) -> dict[str, Any]:
    """Build template context for Week 3 via WeekRegistry."""
    mod = week_registry.get(3)
    if not mod:
        raise RuntimeError("Week 3 module not registered")
    student = get_current_student(request, db)
    progress = ScoringService.get_progress_summary(db, student.id, week_number=3)
    return mod.build_context(student=student, progress=progress, request=request)


@router.get("/week3", response_class=HTMLResponse)
def week3_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """Render Week 3 learning platform."""
    return render_week_page(3, request, db)


@router.get("/api/week3/progress")
def get_week3_progress(request: Request, db: Session = Depends(get_db)) -> dict[str, Any]:
    """Return student progress for Week 3 (strictly read-only)."""
    return get_week_progress_data(3, request, db)


@router.post("/api/week3/practice/{task_id}/run")
def run_week3_practice_task(
    task_id: str,
    payload: CodeSubmissionRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Execute student code for a Week 3 practice task."""
    return run_practice_task_code(3, task_id, payload, request, db)


@router.post("/api/week3/quiz/check")
def check_week3_quiz(
    payload: QuizSubmissionRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Evaluate Week 3 quiz submission."""
    return check_quiz_answers(3, payload, request, db)


@router.post("/api/week3/quiz/evaluate")
def evaluate_week3_quiz_endpoint(
    payload: QuizSubmissionRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Alias for check_quiz endpoint for backward compatibility."""
    return check_quiz_answers(3, payload, request, db)


@router.post("/api/week3/theory/complete")
def complete_week3_theory_endpoint(
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Mark Week 3 theory as completed."""
    return mark_theory_complete(3, request, db)
