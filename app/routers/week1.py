"""FastAPI router for Week 1 educational module and API endpoints."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import settings
from app.content.week_1.lab import LAB_TASK
from app.content.week_1.lecture import LECTURE_DATA
from app.content.week_1.practice import PRACTICE_TASK
from app.content.week_1.quiz import QUIZ_QUESTIONS, check_quiz_answers
from app.database.session import get_db
from app.services.runner import RunnerService
from app.services.scoring import ScoringService

router = APIRouter(tags=["Week 1"])
templates = Jinja2Templates(directory=str(settings.templates_dir))


class QuizCheckRequest(BaseModel):
    answers: dict[str, int]


class CodeRunRequest(BaseModel):
    code: str


@router.get("/week1", response_class=HTMLResponse)
def week1_page(
    request: Request,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    """Render unified 4-tab Week 1 page: Lecture, Quiz, Practice, Lab."""
    student = ScoringService.get_or_create_student(db)
    progress = ScoringService.get_progress_data(db, student.id)

    return templates.TemplateResponse(
        request=request,
        name="week1.html",
        context={
            "app_name": settings.app_name,
            "version": settings.app_version,
            "student": student,
            "progress": progress,
            "lecture": LECTURE_DATA,
            "quiz_questions": QUIZ_QUESTIONS,
            "practice": PRACTICE_TASK,
            "lab": LAB_TASK,
        },
    )


@router.get("/api/week1/progress")
def get_week1_progress(
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Retrieve current student progress and scores for Week 1."""
    student = ScoringService.get_or_create_student(db)
    return ScoringService.get_progress_data(db, student.id)


@router.post("/api/week1/quiz/check")
def check_quiz(
    payload: QuizCheckRequest,
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Validate submitted quiz answers and award 0..3 points."""
    student = ScoringService.get_or_create_student(db)
    quiz_result = check_quiz_answers(payload.answers)

    all_correct = quiz_result["correct_count"] == quiz_result["total_questions"]
    submission, progress = ScoringService.record_and_update_progress(
        db=db,
        student_id=student.id,
        task_id="week_1_quiz",
        code=str(payload.answers),
        status="PASSED" if all_correct else "SUBMITTED",
        score=quiz_result["score"],
        details=quiz_result,
    )

    return JSONResponse(
        content={
            "score": quiz_result["score"],
            "max_score": quiz_result["max_score"],
            "correct_count": quiz_result["correct_count"],
            "total_questions": quiz_result["total_questions"],
            "details": quiz_result["details"],
            "total_week_score": progress.score,
            "is_completed": progress.is_completed,
            "submission_id": submission.id,
        }
    )


@router.post("/api/week1/practice/run")
def run_practice(
    payload: CodeRunRequest,
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Execute practice solution against secret 7-test suite and award 0..7 points."""
    student = ScoringService.get_or_create_student(db)
    run_result = RunnerService.run_code(
        code=payload.code,
        test_code=PRACTICE_TASK["secret_tests"],
    )

    total_tests = PRACTICE_TASK["test_count"]
    if run_result.passed:
        passed_count = total_tests
    else:
        passed_count = ScoringService.extract_passed_test_count(
            run_result.output,
            default_total=total_tests,
        )

    score = float(min(passed_count, total_tests))

    submission, progress = ScoringService.record_and_update_progress(
        db=db,
        student_id=student.id,
        task_id="week_1_practice",
        code=payload.code,
        status=run_result.status,
        score=score,
        details={
            "passed_tests": passed_count,
            "total_tests": total_tests,
            "execution_time_ms": run_result.execution_time_ms,
        },
        raw_output=run_result.output,
    )

    return JSONResponse(
        content={
            "status": run_result.status,
            "passed": run_result.passed,
            "passed_tests": passed_count,
            "total_tests": total_tests,
            "score": score,
            "output": run_result.output,
            "execution_time_ms": run_result.execution_time_ms,
            "total_week_score": progress.score,
            "is_completed": progress.is_completed,
            "submission_id": submission.id,
        }
    )


@router.post("/api/week1/lab/run")
def run_lab(
    payload: CodeRunRequest,
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Execute lab solution against secret 10-test suite and award 0..10 points."""
    student = ScoringService.get_or_create_student(db)
    run_result = RunnerService.run_code(
        code=payload.code,
        test_code=LAB_TASK["secret_tests"],
    )

    total_tests = LAB_TASK["test_count"]
    if run_result.passed:
        passed_count = total_tests
    else:
        passed_count = ScoringService.extract_passed_test_count(
            run_result.output,
            default_total=total_tests,
        )

    score = float(min(passed_count, total_tests))

    submission, progress = ScoringService.record_and_update_progress(
        db=db,
        student_id=student.id,
        task_id="week_1_lab",
        code=payload.code,
        status=run_result.status,
        score=score,
        details={
            "passed_tests": passed_count,
            "total_tests": total_tests,
            "execution_time_ms": run_result.execution_time_ms,
        },
        raw_output=run_result.output,
    )

    return JSONResponse(
        content={
            "status": run_result.status,
            "passed": run_result.passed,
            "passed_tests": passed_count,
            "total_tests": total_tests,
            "score": score,
            "output": run_result.output,
            "execution_time_ms": run_result.execution_time_ms,
            "total_week_score": progress.score,
            "is_completed": progress.is_completed,
            "submission_id": submission.id,
        }
    )
