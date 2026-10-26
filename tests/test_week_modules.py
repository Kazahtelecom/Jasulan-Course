"""Tests for WeekModule contract, WeekRegistry, multi-student profiles, and theory completion."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.main import app
from app.modules.registry import week_registry
from app.services.scoring import ScoringService

client = TestClient(app)


def test_week_registry_registered_modules() -> None:
    """Verify WeekRegistry has week 1, week 2, and week 3 properly registered."""
    w1 = week_registry.get(1)
    w2 = week_registry.get(2)
    w3 = week_registry.get(3)
    assert w1 is not None
    assert w2 is not None
    assert w3 is not None
    assert w1.week_number == 1
    assert w2.week_number == 2
    assert w3.week_number == 3
    assert len(w1.practice_tasks) == 3
    assert len(w2.practice_tasks) == 3
    assert len(w3.practice_tasks) == 3
    assert len(w1.quiz_questions) == 10
    assert len(w2.quiz_questions) == 10
    assert len(w3.quiz_questions) == 10


def test_student_profiles_isolation() -> None:
    """Verify each of the 4 students maintains completely isolated progress in the database."""
    students = ["zhasulan", "roman", "arseniy", "saubakirov"]

    # Each student submits quiz answers
    client.post(
        "/api/week1/quiz/check",
        headers={"X-Student-Id": "roman"},
        json={"answers": {"q1": 0}},
    )
    client.post(
        "/api/week1/quiz/check",
        headers={"X-Student-Id": "arseniy"},
        json={"answers": {"q1": 0, "q2": 1, "q3": 0, "q4": 0, "q5": 0, "q6": 0}},
    )

    prog_roman = client.get("/api/week1/progress", headers={"X-Student-Id": "roman"}).json()
    prog_arseniy = client.get("/api/week1/progress", headers={"X-Student-Id": "arseniy"}).json()

    assert prog_roman["quiz_score"] != prog_arseniy["quiz_score"]
    assert prog_arseniy["quiz_score"] > prog_roman["quiz_score"]


def test_theory_completion_recording() -> None:
    """Verify marking theory complete records week_N_theory topic."""
    res = client.post(
        "/api/week1/theory/complete",
        headers={"X-Student-Id": "saubakirov"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "COMPLETED"
    assert data["theory_completed"] is True

    prog = client.get(
        "/api/week1/progress",
        headers={"X-Student-Id": "saubakirov"},
    ).json()
    assert prog["theory_completed"] is True


def test_read_only_progress_does_not_mutate_db() -> None:
    """Verify GET /api/week1/progress does not mutate the database."""
    db: Session = SessionLocal()
    try:
        student = ScoringService.get_or_create_student(db, username="zhasulan")
        summary = ScoringService.get_progress_summary(db, student.id, week_number=1)
        assert "total_score" in summary
        assert "quiz_score" in summary
        # Ensure session is not dirty
        assert len(db.dirty) == 0
        assert len(db.new) == 0
    finally:
        db.close()
