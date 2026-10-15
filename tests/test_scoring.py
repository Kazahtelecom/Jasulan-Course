"""Tests for ScoringService, High-Water Mark rules, and TopicProgress persistence."""

from sqlalchemy.orm import Session

from app.models.submission import Submission
from app.services.scoring import ScoringService


def test_extract_passed_test_count_patterns():
    """Verify regex extraction of passed test counts from pytest outputs."""
    # Summary pattern
    assert ScoringService.extract_passed_test_count("= 7 passed in 0.12s =", 7) == 7
    assert ScoringService.extract_passed_test_count("= 5 passed, 2 failed in 0.20s =", 7) == 5
    assert ScoringService.extract_passed_test_count("= 10 passed in 0.35s =", 10) == 10

    # Line-by-line PASSED markers
    verbose_out = "test.py::test_one PASSED\ntest.py::test_two PASSED\ntest.py::test_three FAILED"
    assert ScoringService.extract_passed_test_count(verbose_out, 7) == 2

    # Zero or failure
    assert ScoringService.extract_passed_test_count("= 2 failed in 0.05s =", 7) == 0
    assert ScoringService.extract_passed_test_count("", 7) == 0
    assert ScoringService.extract_passed_test_count("SyntaxError: invalid syntax", 7) == 0


def test_get_or_create_student(db_session: Session):
    """Verify student creation and retrieval idempotence."""
    student1 = ScoringService.get_or_create_student(
        db_session,
        username="test_stud",
        full_name="Тестовый Студент",
    )
    assert student1.id is not None
    assert student1.username == "test_stud"

    student2 = ScoringService.get_or_create_student(db_session, username="test_stud")
    assert student2.id == student1.id


def test_scoring_aggregation_and_high_water_mark(db_session: Session):
    """Verify component addition, completion threshold, and protection against score decrease."""
    student = ScoringService.get_or_create_student(db_session, username="zhasulan_test")

    # Step 1: Submit Quiz (award 3.0 points)
    _, prog1 = ScoringService.record_and_update_progress(
        db=db_session,
        student_id=student.id,
        task_id="week_1_quiz",
        code="{'q1': 1}",
        status="PASSED",
        score=3.0,
    )
    assert prog1.score == 3.0
    assert prog1.is_completed is False

    # Step 2: Submit Practice (award 7.0 points) -> Total 10.0
    _, prog2 = ScoringService.record_and_update_progress(
        db=db_session,
        student_id=student.id,
        task_id="week_1_practice",
        code="class TransitCard: pass",
        status="PASSED",
        score=7.0,
    )
    assert prog2.score == 10.0
    assert prog2.is_completed is False

    # Step 3: Submit Lab (award 8.0 points) -> Total 18.0 -> Passes threshold (>= 12)
    _, prog3 = ScoringService.record_and_update_progress(
        db=db_session,
        student_id=student.id,
        task_id="week_1_lab",
        code="class SingleTripTicket: pass",
        status="FAILED",
        score=8.0,
    )
    assert prog3.score == 18.0
    assert prog3.is_completed is True

    # Step 4: Regressive attempt on Lab (student introduces a bug, gets only 2.0 points)
    # The score in TopicProgress MUST stay at 18.0 (High-Water Mark policy)
    _, prog4 = ScoringService.record_and_update_progress(
        db=db_session,
        student_id=student.id,
        task_id="week_1_lab",
        code="broken code",
        status="FAILED",
        score=2.0,
    )
    assert prog4.score == 18.0
    assert prog4.is_completed is True

    # Step 5: Perfect attempt on Lab (10.0 points) -> Total 20.0
    _, prog5 = ScoringService.record_and_update_progress(
        db=db_session,
        student_id=student.id,
        task_id="week_1_lab",
        code="perfect code",
        status="PASSED",
        score=10.0,
    )
    assert prog5.score == 20.0
    assert prog5.is_completed is True


def test_submissions_logged_in_database(db_session: Session):
    """Verify that every attempt logs a record in the Submission table."""
    student = ScoringService.get_or_create_student(db_session, username="sub_test")

    sub, prog = ScoringService.record_and_update_progress(
        db=db_session,
        student_id=student.id,
        task_id="week_1_practice",
        code="class Card: pass",
        status="PASSED",
        score=5.0,
        details={"passed_tests": 5, "total_tests": 7},
        raw_output="5 passed in 0.1s",
    )

    saved_sub = db_session.get(Submission, sub.id)
    assert saved_sub is not None
    assert saved_sub.student_id == student.id
    assert saved_sub.task_id == "week_1_practice"
    assert "class Card: pass" in saved_sub.code
    assert "5.0" in saved_sub.test_output
