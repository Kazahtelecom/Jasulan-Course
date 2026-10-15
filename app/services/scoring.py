"""Scoring and progress tracking service for Web-OOP platform."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.progress import TopicProgress
from app.models.student import Student
from app.models.submission import Submission

PASSING_SCORE_THRESHOLD: float = 12.0
MAX_WEEK1_SCORE: float = 20.0
MAX_QUIZ_SCORE: float = 3.0
MAX_PRACTICE_SCORE: float = 7.0
MAX_LAB_SCORE: float = 10.0


class ScoringService:
    """Service handling score computation, High-Water Mark rules, and progress persistence."""

    @staticmethod
    def get_or_create_student(
        db: Session,
        username: str = "zhasulan",
        full_name: str = "Жасұлан Саубакиров",
    ) -> Student:
        """Fetch existing student or create default student."""
        stmt = select(Student).where(Student.username == username)
        student = db.scalars(stmt).first()
        if student is None:
            student = Student(username=username, full_name=full_name)
            db.add(student)
            db.commit()
            db.refresh(student)
        return student

    @staticmethod
    def extract_passed_test_count(output: str, default_total: int) -> int:
        """Extract number of passed tests from pytest output string."""
        if not output:
            return 0

        # Pattern 1: look for explicit summary "N passed"
        summary_match = re.search(r"(\d+)\s+passed", output)
        if summary_match:
            return int(summary_match.group(1))

        # Pattern 2: count individual PASSED markers in verbose output
        passed_markers = len(re.findall(r"::test_\w+\s+PASSED", output))
        if passed_markers > 0:
            return min(passed_markers, default_total)

        return 0

    @classmethod
    def get_component_scores(cls, db: Session, student_id: int) -> dict[str, float]:
        """Calculate best scores for quiz, practice, and lab from student submissions."""
        stmt = select(Submission).where(
            Submission.student_id == student_id,
            Submission.task_id.in_(["week_1_quiz", "week_1_practice", "week_1_lab"]),
        )
        submissions = db.scalars(stmt).all()

        best_quiz = 0.0
        best_practice = 0.0
        best_lab = 0.0

        for sub in submissions:
            score = 0.0
            if sub.test_output:
                try:
                    payload = json.loads(sub.test_output)
                    if isinstance(payload, dict):
                        score = float(payload.get("score", 0.0))
                except (json.JSONDecodeError, ValueError, TypeError):
                    score = 0.0

            if sub.task_id == "week_1_quiz":
                best_quiz = max(best_quiz, min(score, MAX_QUIZ_SCORE))
            elif sub.task_id == "week_1_practice":
                best_practice = max(best_practice, min(score, MAX_PRACTICE_SCORE))
            elif sub.task_id == "week_1_lab":
                best_lab = max(best_lab, min(score, MAX_LAB_SCORE))

        total = round(best_quiz + best_practice + best_lab, 1)
        total = min(MAX_WEEK1_SCORE, max(0.0, total))

        return {
            "quiz": round(best_quiz, 1),
            "practice": round(best_practice, 1),
            "lab": round(best_lab, 1),
            "total": total,
        }

    @classmethod
    def record_and_update_progress(
        cls,
        db: Session,
        student_id: int,
        task_id: str,
        code: str,
        status: str,
        score: float,
        details: dict[str, Any] | None = None,
        raw_output: str | None = None,
    ) -> tuple[Submission, TopicProgress]:
        """Record submission in DB and update TopicProgress with High-Water Mark guarantee."""
        payload: dict[str, Any] = {
            "score": score,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        }
        if details:
            payload["details"] = details
        if raw_output:
            payload["raw_output"] = raw_output

        submission = Submission(
            student_id=student_id,
            task_id=task_id,
            code=code,
            status=status,
            test_output=json.dumps(payload, ensure_ascii=False),
        )
        db.add(submission)
        db.flush()

        component_scores = cls.get_component_scores(db, student_id)
        calculated_total = component_scores["total"]

        stmt = select(TopicProgress).where(
            TopicProgress.student_id == student_id,
            TopicProgress.topic_id == "week_1",
        )
        progress = db.scalars(stmt).first()

        if progress is None:
            progress = TopicProgress(
                student_id=student_id,
                topic_id="week_1",
                score=calculated_total,
                is_completed=(calculated_total >= PASSING_SCORE_THRESHOLD),
            )
            db.add(progress)
        else:
            # High-water mark rule: max(old_score, new_score)
            new_score = max(progress.score, calculated_total)
            progress.score = round(new_score, 1)
            if progress.score >= PASSING_SCORE_THRESHOLD:
                progress.is_completed = True

        db.commit()
        db.refresh(submission)
        db.refresh(progress)

        return submission, progress

    @classmethod
    def get_progress_data(cls, db: Session, student_id: int) -> dict[str, Any]:
        """Return full progress summary for Week 1."""
        component_scores = cls.get_component_scores(db, student_id)

        stmt = select(TopicProgress).where(
            TopicProgress.student_id == student_id,
            TopicProgress.topic_id == "week_1",
        )
        progress = db.scalars(stmt).first()

        current_score = progress.score if progress is not None else component_scores["total"]
        if progress is not None:
            is_completed = progress.is_completed
        else:
            is_completed = current_score >= PASSING_SCORE_THRESHOLD

        return {
            "topic_id": "week_1",
            "score": round(current_score, 1),
            "max_score": MAX_WEEK1_SCORE,
            "passing_threshold": PASSING_SCORE_THRESHOLD,
            "is_completed": is_completed,
            "quiz_score": component_scores["quiz"],
            "practice_score": component_scores["practice"],
            "lab_score": component_scores["lab"],
        }
