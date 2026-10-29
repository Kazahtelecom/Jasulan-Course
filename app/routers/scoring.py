"""Router for student profiles, multi-user management, and scoring summaries."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.student import Student
from app.services.scoring import ScoringService

router = APIRouter(prefix="/api/students", tags=["Students & Scoring"])


def get_current_student(
    request: Request,
    db: Session = Depends(get_db),
) -> Student:
    """Extract active student from X-Student-Id header or query parameter."""
    header_val = request.headers.get("X-Student-Id")
    query_val = request.query_params.get("student")
    username = header_val or query_val or ScoringService.DEFAULT_USERNAME
    return ScoringService.get_or_create_student(db, username=username)


@router.get("")
def list_students() -> list[dict[str, str]]:
    """List the 4 fixed student profiles in the study group."""
    return ScoringService.get_known_students()


@router.get("/current")
def get_current_student_info(
    student: Student = Depends(get_current_student),
) -> dict[str, Any]:
    """Return currently active student profile info."""
    return {
        "id": student.id,
        "username": student.username,
        "full_name": student.full_name,
    }


@router.get("/scores")
def get_student_scores(
    student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Return comprehensive score breakdown for the active student (strictly read-only)."""
    return {
        "student": {
            "id": student.id,
            "username": student.username,
            "full_name": student.full_name,
        },
        "week1": ScoringService.get_progress_summary(db, student.id, week_number=1),
        "week2": ScoringService.get_progress_summary(db, student.id, week_number=2),
        "week3": ScoringService.get_progress_summary(db, student.id, week_number=3),
        "exam": ScoringService.get_exam_progress_summary(db, student.id),
    }
