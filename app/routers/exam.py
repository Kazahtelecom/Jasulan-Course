"""Router and API controller for Final Exam Module and Comprehensive Assessment."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session

from app.config import settings
from app.content.exam import (
    EXAM_OVERVIEW,
    EXAM_PRACTICE_TASKS,
    EXAM_QUIZ_QUESTIONS,
    evaluate_exam_quiz,
)
from app.database.session import get_db
from app.routers.scoring import get_current_student
from app.services.runner import RunnerService
from app.services.scoring import ScoringService

router = APIRouter(tags=["Final Exam"])
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


@router.get("/exam", response_class=HTMLResponse)
def render_exam_page(
    request: Request,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    """Render the comprehensive Final Exam page for Web-OOP platform."""
    student = get_current_student(request, db)
    progress = ScoringService.get_exam_progress_summary(db, student.id)

    # In exam mode, we do NOT expose reference solutions in DOM attributes to protect academic integrity
    sanitized_tasks = []
    for task in EXAM_PRACTICE_TASKS:
        t_copy = dict(task)
        t_copy["reference_solution"] = ""  # Stripped for academic integrity
        sanitized_tasks.append(t_copy)

    ctx = {
        "request": request,
        "app_name": settings.app_name,
        "active_week": "exam",
        "is_exam": True,
        "student": student,
        "overview": EXAM_OVERVIEW,
        "progress": progress,
        "practice_tasks": sanitized_tasks,
        "quiz_questions": EXAM_QUIZ_QUESTIONS,
    }
    return templates.TemplateResponse(
        request=request,
        name="exam.html",
        context=ctx,
    )


@router.get("/api/exam/progress")
def get_exam_progress(
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Retrieve comprehensive exam progress and 100-point course total (strictly read-only)."""
    student = get_current_student(request, db)
    return ScoringService.get_exam_progress_summary(db, student.id)


@router.post("/api/exam/practice/{task_id}/run")
def run_exam_practice_task(
    task_id: str,
    payload: CodeSubmissionRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Execute exam coding task in sandbox and record score (10.0 pts per passed task)."""
    task = next((t for t in EXAM_PRACTICE_TASKS if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Exam practice task '{task_id}' not found")

    student = get_current_student(request, db)
    run_res = RunnerService.run_code(
        code=payload.code,
        test_code=task["test_code"],
    )

    prog_summary = ScoringService.record_exam_task_submission(
        db=db,
        student_id=student.id,
        task_id=task_id,
        code=payload.code,
        passed=run_res.passed,
        output=run_res.output,
        status=run_res.status,
    )

    return {
        "status": run_res.status,
        "output": run_res.output,
        "execution_time_ms": run_res.execution_time_ms,
        "passed": run_res.passed,
        "progress": prog_summary,
    }


@router.post("/api/exam/quiz/check")
@router.post("/api/exam/quiz/evaluate")
def check_exam_quiz(
    payload: QuizSubmissionRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Check final exam quiz answers and record score in SQLite WAL (up to 20.0 pts)."""
    eval_res = evaluate_exam_quiz(payload.answers)
    student = get_current_student(request, db)

    prog_summary = ScoringService.record_exam_quiz_submission(
        db=db,
        student_id=student.id,
        quiz_score=eval_res["score"],
    )

    return {
        **eval_res,
        "progress": prog_summary,
    }
