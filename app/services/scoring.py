"""Scoring and progress persistence service for Web-OOP platform."""

from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.models.progress import TopicProgress
from app.models.student import Student
from app.models.submission import Submission


class ScoringService:
    """Manages student progress: 100% of points come from the final Quiz (20.0 max, pass >= 12.0).

    Practice tasks are ungraded interactive training steps. Each week is tracked independently.
    """

    STUDENTS: list[dict[str, str]] = [
        {"username": "zhasulan", "full_name": "Жасулан Куандыков"},
        {"username": "roman", "full_name": "Иванов Роман"},
        {"username": "arseniy", "full_name": "Мухитов Арсений"},
        {"username": "saubakirov", "full_name": "Санжар Аубакиров"},
    ]

    DEFAULT_USERNAME = "zhasulan"
    DEFAULT_FULL_NAME = "Жасулан Куандыков"

    WEEK_TASK_IDS: dict[int, tuple[str, str, str]] = {
        1: ("task_1", "task_2", "task_3"),
        2: ("w2_task_1", "w2_task_2", "w2_task_3"),
    }

    QUIZ_MAX_SCORE = 20.0
    TOTAL_MAX_SCORE = 20.0
    PASS_THRESHOLD = 12.0

    @classmethod
    def get_known_students(cls) -> list[dict[str, str]]:
        """Return the fixed list of 4 students in the group."""
        return list(cls.STUDENTS)

    @classmethod
    def get_or_create_student(cls, db: Session, username: str = DEFAULT_USERNAME) -> Student:
        """Retrieve or create a student profile from the known list."""
        clean_user = username.lower().strip() if username else cls.DEFAULT_USERNAME
        matched_info = next(
            (s for s in cls.STUDENTS if s["username"] == clean_user),
            None,
        )
        if not matched_info:
            matched_info = cls.STUDENTS[0]

        student = db.query(Student).filter(Student.username == matched_info["username"]).first()
        if not student:
            student = Student(
                username=matched_info["username"],
                full_name=matched_info["full_name"],
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
        week_number: int = 1,
    ) -> dict[str, Any]:
        """Record an ungraded training task run."""
        topic_key = f"week_{week_number}_{task_id}"

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

        cls._recalculate_overall(db, student_id, week_number=week_number)
        db.commit()
        return cls.get_progress_summary(db, student_id, week_number=week_number)

    @classmethod
    def record_theory_completed(
        cls,
        db: Session,
        student_id: int,
        week_number: int = 1,
    ) -> dict[str, Any]:
        """Record reading the lecture theory for a given week."""
        topic_key = f"week_{week_number}_theory"
        rec = cls._get_or_create_topic(db, student_id, topic_key)
        rec.is_completed = True
        rec.score = 0.0
        db.commit()
        return cls.get_progress_summary(db, student_id, week_number=week_number)

    @classmethod
    def record_quiz_submission(
        cls,
        db: Session,
        student_id: int,
        quiz_score: float,
        week_number: int = 1,
    ) -> dict[str, Any]:
        """Update quiz score with high-water mark protection."""
        bounded_score = min(cls.QUIZ_MAX_SCORE, max(0.0, round(quiz_score, 1)))
        quiz_topic = f"week_{week_number}_quiz"
        quiz_rec = cls._get_or_create_topic(db, student_id, quiz_topic)
        if bounded_score > quiz_rec.score:
            quiz_rec.score = bounded_score
        if quiz_rec.score >= cls.PASS_THRESHOLD:
            quiz_rec.is_completed = True

        cls._recalculate_overall(db, student_id, week_number=week_number)
        db.commit()
        return cls.get_progress_summary(db, student_id, week_number=week_number)

    @classmethod
    def _recalculate_overall(
        cls,
        db: Session,
        student_id: int,
        week_number: int = 1,
    ) -> TopicProgress:
        qz = cls._get_or_create_topic(db, student_id, f"week_{week_number}_quiz")
        overall = cls._get_or_create_topic(db, student_id, f"week_{week_number}")

        overall.score = round(min(cls.TOTAL_MAX_SCORE, qz.score), 1)
        overall.is_completed = overall.score >= cls.PASS_THRESHOLD
        db.flush()
        return overall

    @classmethod
    def get_progress_summary(
        cls,
        db: Session,
        student_id: int,
        week_number: int = 1,
    ) -> dict[str, Any]:
        """Return week progress breakdown strictly READ-ONLY (no db.commit)."""
        task_ids = cls.WEEK_TASK_IDS.get(week_number, cls.WEEK_TASK_IDS[1])

        # Query existing topic progress records without mutating the DB
        records = (
            db.query(TopicProgress)
            .filter(TopicProgress.student_id == student_id)
            .all()
        )
        rec_map = {r.topic_id: r for r in records}

        qz_rec = rec_map.get(f"week_{week_number}_quiz")
        qz_score = round(qz_rec.score, 1) if qz_rec else 0.0
        qz_completed = bool(qz_rec.is_completed) if qz_rec else False

        theory_rec = rec_map.get(f"week_{week_number}_theory")
        theory_completed = bool(theory_rec.is_completed) if theory_rec else False

        total_score = round(min(cls.TOTAL_MAX_SCORE, qz_score), 1)
        is_completed = total_score >= cls.PASS_THRESHOLD

        tasks_map = {}
        tasks_completed = 0
        for tid in task_ids:
            trec = rec_map.get(f"week_{week_number}_{tid}")
            done = bool(trec.is_completed) if trec else False
            if done:
                tasks_completed += 1
            tasks_map[tid] = {"is_completed": done}

        percent = min(100, int(round((total_score / cls.TOTAL_MAX_SCORE) * 100)))

        return {
            "week_number": week_number,
            "total_score": total_score,
            "max_score": cls.TOTAL_MAX_SCORE,
            "pass_threshold": cls.PASS_THRESHOLD,
            "is_completed": is_completed,
            "progress_percent": percent,
            "tasks_completed": tasks_completed,
            "tasks_total": len(task_ids),
            "quiz_score": qz_score,
            "quiz_max": cls.QUIZ_MAX_SCORE,
            "quiz_completed": qz_completed,
            "theory_completed": theory_completed,
            "tasks": tasks_map,
        }
