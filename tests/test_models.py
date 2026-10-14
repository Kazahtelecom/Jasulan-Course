"""Tests for SQLAlchemy database models."""

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Student, Submission, TopicProgress


def test_create_and_query_student(db_session: Session) -> None:
    """Verify Student creation, indexing, and retrieval."""
    student = Student(username="student1", full_name="Иван Иванов")
    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)

    assert student.id is not None
    assert student.username == "student1"
    assert student.full_name == "Иван Иванов"
    assert student.created_at is not None

    queried = db_session.scalar(select(Student).where(Student.username == "student1"))
    assert queried is not None
    assert queried.id == student.id


def test_student_unique_username(db_session: Session) -> None:
    """Verify unique constraint on student username."""
    s1 = Student(username="duplicate_user", full_name="User One")
    db_session.add(s1)
    db_session.commit()

    s2 = Student(username="duplicate_user", full_name="User Two")
    db_session.add(s2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_topic_progress_relationship(db_session: Session) -> None:
    """Verify TopicProgress creation and relationship with Student."""
    student = Student(username="progress_user", full_name="Пётр Петров")
    db_session.add(student)
    db_session.commit()

    progress = TopicProgress(
        student_id=student.id,
        topic_id="week1_encapsulation",
        is_completed=True,
        score=95.0,
    )
    db_session.add(progress)
    db_session.commit()
    db_session.refresh(progress)

    assert progress.id is not None
    assert progress.student_id == student.id
    assert progress.student.username == "progress_user"
    assert progress.is_completed is True
    assert progress.score == 95.0


def test_submission_relationship_and_cascade(db_session: Session) -> None:
    """Verify Submission creation, relationship, and cascade delete."""
    student = Student(username="sub_user", full_name="Сергей Сергеев")
    db_session.add(student)
    db_session.commit()

    submission = Submission(
        student_id=student.id,
        task_id="w1_task1_passenger",
        code="class Passenger: pass",
        status="PASSED",
        test_output="1 passed in 0.05s",
    )
    db_session.add(submission)
    db_session.commit()
    db_session.refresh(submission)

    assert submission.id is not None
    assert submission.student_id == student.id
    assert submission.status == "PASSED"

    assert len(student.submissions) == 1
    assert student.submissions[0].id == submission.id

    db_session.delete(student)
    db_session.commit()

    sub_after = db_session.scalar(select(Submission).where(Submission.id == submission.id))
    assert sub_after is None
