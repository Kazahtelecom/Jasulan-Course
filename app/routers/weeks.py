"""Generic router and controller handlers for educational curriculum weeks."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session

from app.config import settings
from app.database.session import get_db
from app.modules.registry import week_registry
from app.routers.scoring import get_current_student
from app.services.runner import RunnerService
from app.services.scoring import ScoringService

router = APIRouter(prefix="/api/weeks", tags=["Weeks Generic"])
templates = Jinja2Templates(directory=str(settings.templates_dir))


class CodeSubmissionRequest(BaseModel):
    code: str

    @field_validator("code")
    @classmethod
    def validate_code_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Code submission cannot be empty")
        return v


class QuizSubmissionRequest(BaseModel):
    answers: dict[str, int]

    @field_validator("answers")
    @classmethod
    def validate_answers_not_empty(cls, v: dict[str, int]) -> dict[str, int]:
        if not v:
            raise ValueError("Quiz answers dictionary cannot be empty")
        return v


def render_week_page(
    week_number: int,
    request: Request,
    db: Session,
) -> HTMLResponse:
    """Render unified learning platform template for specified week."""
    module = week_registry.get(week_number)
    if not module:
        raise HTTPException(status_code=404, detail=f"Week module {week_number} not found")

    student = get_current_student(request, db)
    progress = ScoringService.get_progress_summary(db, student.id, week_number=week_number)
    ctx = module.build_context(student=student, progress=progress, request=request)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=ctx,
    )


def get_week_progress_data(
    week_number: int,
    request: Request,
    db: Session,
) -> dict[str, Any]:
    """Retrieve read-only progress summary for a given week."""
    module = week_registry.get(week_number)
    if not module:
        raise HTTPException(status_code=404, detail=f"Week module {week_number} not found")

    student = get_current_student(request, db)
    return ScoringService.get_progress_summary(db, student.id, week_number=week_number)


def run_practice_task_code(
    week_number: int,
    task_id: str,
    payload: CodeSubmissionRequest,
    request: Request,
    db: Session,
) -> dict[str, Any]:
    """Run student code for a practice task in sandbox."""
    module = week_registry.get(week_number)
    if not module:
        raise HTTPException(status_code=404, detail=f"Week module {week_number} not found")

    task = module.get_practice_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Unknown practice task '{task_id}' in week {week_number}")

    student = get_current_student(request, db)
    run_res = RunnerService.run_code(
        code=payload.code,
        test_code=task["test_code"],
    )

    progress = ScoringService.record_task_submission(
        db=db,
        student_id=student.id,
        task_id=task_id,
        code=payload.code,
        passed=run_res.passed,
        output=run_res.output,
        status=run_res.status,
        week_number=week_number,
    )

    return {
        "status": run_res.status,
        "passed": run_res.passed,
        "output": run_res.output,
        "execution_time_ms": run_res.execution_time_ms,
        "progress": progress,
    }


def check_quiz_answers(
    week_number: int,
    payload: QuizSubmissionRequest,
    request: Request,
    db: Session,
) -> dict[str, Any]:
    """Check quiz answers and update score with high-water mark."""
    module = week_registry.get(week_number)
    if not module:
        raise HTTPException(status_code=404, detail=f"Week module {week_number} not found")

    student = get_current_student(request, db)
    eval_result = module.evaluate_quiz(payload.answers)
    score = eval_result["score"]
    progress = ScoringService.record_quiz_submission(
        db=db,
        student_id=student.id,
        quiz_score=score,
        week_number=week_number,
    )

    return {
        **eval_result,
        "pass_threshold": ScoringService.PASS_THRESHOLD,
        "is_passed": score >= ScoringService.PASS_THRESHOLD,
        "progress": progress,
    }


def mark_theory_complete(
    week_number: int,
    request: Request,
    db: Session,
) -> dict[str, Any]:
    """Mark reading lecture theory as completed for a week."""
    module = week_registry.get(week_number)
    if not module:
        raise HTTPException(status_code=404, detail=f"Week module {week_number} not found")

    student = get_current_student(request, db)
    progress = ScoringService.record_theory_completed(
        db=db,
        student_id=student.id,
        week_number=week_number,
    )
    return {
        "status": "COMPLETED",
        "week_number": week_number,
        "theory_completed": True,
        "progress": progress,
    }


@router.get("/{week_number}/progress")
def api_get_progress(
    week_number: int,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    return get_week_progress_data(week_number, request, db)


@router.post("/{week_number}/practice/{task_id}/run")
def api_run_practice(
    week_number: int,
    task_id: str,
    payload: CodeSubmissionRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    return run_practice_task_code(week_number, task_id, payload, request, db)


@router.post("/{week_number}/quiz/check")
def api_check_quiz(
    week_number: int,
    payload: QuizSubmissionRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    return check_quiz_answers(week_number, payload, request, db)


@router.post("/{week_number}/theory/complete")
def api_complete_theory(
    week_number: int,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    return mark_theory_complete(week_number, request, db)
