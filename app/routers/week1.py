"""FastAPI router for Week 1 educational platform and API endpoints."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import settings
from app.content.week_1 import (
    PRACTICE_TASKS,
    QUIZ_QUESTIONS,
    THEORY_SECTIONS,
    WALKTHROUGH_EXAMPLE,
    WEEK1_OVERVIEW,
    evaluate_quiz,
    get_practice_task,
)
from app.database.session import get_db
from app.services.runner import RunnerService
from app.services.scoring import ScoringService

router = APIRouter(tags=["Week 1"])
templates = Jinja2Templates(directory=str(settings.templates_dir))


class CodeSubmissionRequest(BaseModel):
    code: str


class QuizSubmissionRequest(BaseModel):
    answers: dict[str, int]


def build_platform_context(request: Request, db: Session) -> dict[str, Any]:
    """Build template context for the unified Web-OOP learning platform."""
    student = ScoringService.get_or_create_student(db)
    progress = ScoringService.get_progress_summary(db, student.id)
    return {
        "request": request,
        "app_name": settings.app_name,
        "version": settings.app_version,
        "active_week": 1,
        "student": student,
        "progress": progress,
        "overview": WEEK1_OVERVIEW,
        "theory_sections": THEORY_SECTIONS,
        "walkthrough": WALKTHROUGH_EXAMPLE,
        "practice_tasks": PRACTICE_TASKS,
        "quiz_questions": QUIZ_QUESTIONS,
    }


@router.get("/week1", response_class=HTMLResponse)
def week1_page(
    request: Request,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    """Render the unified learning platform on /week1."""
    ctx = build_platform_context(request, db)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=ctx,
    )


@router.get("/api/week1/progress")
def get_week1_progress(db: Session = Depends(get_db)) -> dict[str, Any]:
    """Return current student progress for Week 1."""
    student = ScoringService.get_or_create_student(db)
    return ScoringService.get_progress_summary(db, student.id)


@router.post("/api/week1/practice/{task_id}/run")
def run_practice_task(
    task_id: str,
    payload: CodeSubmissionRequest,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Execute student code for one of the 3 connected practice tasks."""
    task = get_practice_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Unknown practice task: {task_id}")

    student = ScoringService.get_or_create_student(db)
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
    )

    return {
        "task_id": task_id,
        "status": run_res.status,
        "passed": run_res.passed,
        "output": run_res.output,
        "execution_time_ms": run_res.execution_time_ms,
        "progress": progress,
    }


@router.post("/api/week1/quiz/check")
def check_week1_quiz(
    payload: QuizSubmissionRequest,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Evaluate final Week 1 quiz answers and persist score."""
    student = ScoringService.get_or_create_student(db)
    quiz_eval = evaluate_quiz(payload.answers)
    progress = ScoringService.record_quiz_submission(
        db=db,
        student_id=student.id,
        quiz_score=quiz_eval["score"],
    )
    return {
        **quiz_eval,
        "progress": progress,
    }
