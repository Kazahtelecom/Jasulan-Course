"""Scoring and progress persistence service for Week 1 (Quiz-only grading)."""

from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.models.progress import TopicProgress
from app.models.student import Student
from app.models.submission import Submission


class ScoringService:
    """Manages student progress: 100% of points come from the final Quiz (20.0 max, pass >= 12.0).

    Practice tasks are ungraded interactive training steps.
    """

    DEFAULT_USERNAME = "zhasulan"
    DEFAULT_FULL_NAME = "Жасулан Куандыков"

    TOPIC_OVERALL = "week_1"
    TOPIC_TASK_1 = "week_1_task_1"
    TOPIC_TASK_2 = "week_1_task_2"
    TOPIC_TASK_3 = "week_1_task_3"
    TOPIC_QUIZ = "week_1_quiz"

    QUIZ_MAX_SCORE = 20.0
    TOTAL_MAX_SCORE = 20.0
    PASS_THRESHOLD = 12.0

    @classmethod
    def get_or_create_student(cls, db: Session) -> Student:
        """Retrieve or create the default student profile."""
        student = db.query(Student).filter(Student.username == cls.DEFAULT_USERNAME).first()
        if not student:
            student = Student(
                username=cls.DEFAULT_USERNAME,
                full_name=cls.DEFAULT_FULL_NAME,
            )
            db.add(student)
            db.commit()
            db.refresh(student)
        return student

    @classmethod
    def _get_or_create_topic(cls, db: Session, student_id: int, topic_id: str) -> TopicProgress:
        record = (
            db.query(TopicProgress)
            .filter(
                TopicProgress.student_id == student_id,
                TopicProgress.topic_id == topic_id,
            )
            .first()
        )
        if not record:
            record = TopicProgress(
                student_id=student_id,
                topic_id=topic_id,
                is_completed=False,
                score=0.0,
            )
            db.add(record)
            db.flush()
        return record

    @classmethod
    def record_task_submission(
        cls,
        db: Session,
        student_id: int,
        task_id: str,
        code: str,
        passed: bool,
        output: str,
        status: str,
    ) -> dict[str, Any]:
        """Record an ungraded training task run (does not require or affect week points)."""
        topic_key = f"week_1_{task_id}"

        sub = Submission(
            student_id=student_id,
            task_id=topic_key,
            code=code,
            status=status,
            test_output=output,
        )
        db.add(sub)

        topic_rec = cls._get_or_create_topic(db, student_id, topic_key)
        topic_rec.score = 0.0
        if passed:
            topic_rec.is_completed = True

        cls._recalculate_overall(db, student_id)
        db.commit()
        return cls.get_progress_summary(db, student_id)

    @classmethod
    def record_quiz_submission(
        cls,
        db: Session,
        student_id: int,
        quiz_score: float,
    ) -> dict[str, Any]:
        """Update quiz score (sole graded component) with high-water mark protection."""
        bounded_score = min(cls.QUIZ_MAX_SCORE, max(0.0, round(quiz_score, 1)))
        quiz_rec = cls._get_or_create_topic(db, student_id, cls.TOPIC_QUIZ)
        if bounded_score > quiz_rec.score:
            quiz_rec.score = bounded_score
        if quiz_rec.score >= cls.PASS_THRESHOLD:
            quiz_rec.is_completed = True

        cls._recalculate_overall(db, student_id)
        db.commit()
        return cls.get_progress_summary(db, student_id)

    @classmethod
    def _recalculate_overall(cls, db: Session, student_id: int) -> TopicProgress:
        qz = cls._get_or_create_topic(db, student_id, cls.TOPIC_QUIZ)
        overall = cls._get_or_create_topic(db, student_id, cls.TOPIC_OVERALL)

        # Total score equals quiz score exclusively (0..20.0)
        overall.score = round(min(cls.TOTAL_MAX_SCORE, qz.score), 1)
        overall.is_completed = overall.score >= cls.PASS_THRESHOLD
        db.flush()
        return overall

    @classmethod
    def get_progress_summary(cls, db: Session, student_id: int) -> dict[str, Any]:
        """Return Week 1 progress breakdown (Quiz = 100% of grade, Practice = trainer)."""
        t1 = cls._get_or_create_topic(db, student_id, cls.TOPIC_TASK_1)
        t2 = cls._get_or_create_topic(db, student_id, cls.TOPIC_TASK_2)
        t3 = cls._get_or_create_topic(db, student_id, cls.TOPIC_TASK_3)
        qz = cls._get_or_create_topic(db, student_id, cls.TOPIC_QUIZ)
        overall = cls._recalculate_overall(db, student_id)
        db.commit()

        tasks_completed = sum(1 for t in (t1, t2, t3) if t.is_completed)
        percent = min(100, int(round((overall.score / cls.TOTAL_MAX_SCORE) * 100)))

        return {
            "total_score": round(overall.score, 1),
            "max_score": cls.TOTAL_MAX_SCORE,
            "pass_threshold": cls.PASS_THRESHOLD,
            "is_completed": overall.is_completed,
            "progress_percent": percent,
            "tasks_completed": tasks_completed,
            "tasks_total": 3,
            "quiz_score": round(qz.score, 1),
            "quiz_max": cls.QUIZ_MAX_SCORE,
            "quiz_completed": qz.is_completed,
            "tasks": {
                "task_1": {"is_completed": t1.is_completed},
                "task_2": {"is_completed": t2.is_completed},
                "task_3": {"is_completed": t3.is_completed},
            },
        }
