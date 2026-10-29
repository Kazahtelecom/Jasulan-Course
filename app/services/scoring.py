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
        3: ("w3_task_1", "w3_task_2", "w3_task_3"),
    }

    QUIZ_MAX_SCORE = 20.0
    TOTAL_MAX_SCORE = 20.0
    PASS_THRESHOLD = 12.0

    # Final Exam Module Constants
    EXAM_QUIZ_MAX_SCORE = 20.0
    EXAM_TASK_MAX_SCORE = 10.0
    EXAM_TASKS_MAX_SCORE = 20.0
    EXAM_TOTAL_MAX_SCORE = 40.0
    EXAM_PASS_THRESHOLD = 20.0
    COURSE_TOTAL_MAX_SCORE = 100.0
    COURSE_PASS_THRESHOLD = 50.0

    EXAM_TASK_IDS: tuple[str, str] = ("exam_task_1", "exam_task_2")

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

    @classmethod
    def record_exam_task_submission(
        cls,
        db: Session,
        student_id: int,
        task_id: str,
        code: str,
        passed: bool,
        output: str,
        status: str,
    ) -> dict[str, Any]:
        """Record an exam coding task submission with 10.0 pts score."""
        topic_key = task_id if task_id.startswith("exam_") else f"exam_{task_id}"

        sub = Submission(
            student_id=student_id,
            task_id=topic_key,
            code=code,
            status=status,
            test_output=output,
        )
        db.add(sub)

        topic_rec = cls._get_or_create_topic(db, student_id, topic_key)
        # High-Water Mark protection: if passed, award 10.0 points
        if passed and topic_rec.score < cls.EXAM_TASK_MAX_SCORE:
            topic_rec.score = cls.EXAM_TASK_MAX_SCORE
            topic_rec.is_completed = True

        cls._recalculate_exam_overall(db, student_id)
        db.commit()
        return cls.get_exam_progress_summary(db, student_id)

    @classmethod
    def record_exam_quiz_submission(
        cls,
        db: Session,
        student_id: int,
        quiz_score: float,
    ) -> dict[str, Any]:
        """Record final exam quiz score with High-Water Mark protection."""
        bounded_score = min(cls.EXAM_QUIZ_MAX_SCORE, max(0.0, round(quiz_score, 1)))
        quiz_rec = cls._get_or_create_topic(db, student_id, "exam_quiz")
        if bounded_score > quiz_rec.score:
            quiz_rec.score = bounded_score
        if quiz_rec.score >= cls.PASS_THRESHOLD:
            quiz_rec.is_completed = True

        cls._recalculate_exam_overall(db, student_id)
        db.commit()
        return cls.get_exam_progress_summary(db, student_id)

    @classmethod
    def _recalculate_exam_overall(
        cls,
        db: Session,
        student_id: int,
    ) -> TopicProgress:
        """Recalculate overall exam score (Quiz 20 + Task 1 10 + Task 2 10 = 40 max)."""
        qz = cls._get_or_create_topic(db, student_id, "exam_quiz")
        t1 = cls._get_or_create_topic(db, student_id, "exam_task_1")
        t2 = cls._get_or_create_topic(db, student_id, "exam_task_2")
        overall = cls._get_or_create_topic(db, student_id, "exam_overall")

        total_exam = round(min(cls.EXAM_TOTAL_MAX_SCORE, qz.score + t1.score + t2.score), 1)
        overall.score = total_exam
        overall.is_completed = total_exam >= cls.EXAM_PASS_THRESHOLD
        db.flush()
        return overall

    @classmethod
    def _compute_letter_grade(cls, score: float) -> str:
        """Compute academic ECTS/Letter grade from 100-point total."""
        if score >= 90.0:
            return "A (Отлично)"
        if score >= 75.0:
            return "B (Хорошо)"
        if score >= 50.0:
            return "C (Удовлетворительно)"
        return "F (Не зачтено)"

    @classmethod
    def get_exam_progress_summary(
        cls,
        db: Session,
        student_id: int,
    ) -> dict[str, Any]:
        """Return comprehensive exam progress and 100-point course grand total strictly READ-ONLY."""
        records = (
            db.query(TopicProgress)
            .filter(TopicProgress.student_id == student_id)
            .all()
        )
        rec_map = {r.topic_id: r for r in records}

        qz_rec = rec_map.get("exam_quiz")
        qz_score = round(qz_rec.score, 1) if qz_rec else 0.0
        qz_completed = bool(qz_rec.is_completed) if qz_rec else False

        t1_rec = rec_map.get("exam_task_1")
        t1_score = round(t1_rec.score, 1) if t1_rec else 0.0
        t1_completed = bool(t1_rec.is_completed) if t1_rec else False

        t2_rec = rec_map.get("exam_task_2")
        t2_score = round(t2_rec.score, 1) if t2_rec else 0.0
        t2_completed = bool(t2_rec.is_completed) if t2_rec else False

        tasks_score = round(t1_score + t2_score, 1)
        exam_total = round(min(cls.EXAM_TOTAL_MAX_SCORE, qz_score + tasks_score), 1)
        is_exam_completed = exam_total >= cls.EXAM_PASS_THRESHOLD

        # Aggregate course semester weeks
        w1_rec = rec_map.get("week_1") or rec_map.get("week_1_quiz")
        w1_score = round(min(cls.TOTAL_MAX_SCORE, w1_rec.score), 1) if w1_rec else 0.0

        w2_rec = rec_map.get("week_2") or rec_map.get("week_2_quiz")
        w2_score = round(min(cls.TOTAL_MAX_SCORE, w2_rec.score), 1) if w2_rec else 0.0

        w3_rec = rec_map.get("week_3") or rec_map.get("week_3_quiz")
        w3_score = round(min(cls.TOTAL_MAX_SCORE, w3_rec.score), 1) if w3_rec else 0.0

        semester_score = round(w1_score + w2_score + w3_score, 1)
        grand_total = round(min(cls.COURSE_TOTAL_MAX_SCORE, semester_score + exam_total), 1)
        is_course_completed = grand_total >= cls.COURSE_PASS_THRESHOLD
        progress_percent = min(100, int(round((grand_total / cls.COURSE_TOTAL_MAX_SCORE) * 100)))

        return {
            "exam_total": exam_total,
            "exam_max": cls.EXAM_TOTAL_MAX_SCORE,
            "exam_pass_threshold": cls.EXAM_PASS_THRESHOLD,
            "is_exam_completed": is_exam_completed,
            "quiz_score": qz_score,
            "quiz_max": cls.EXAM_QUIZ_MAX_SCORE,
            "quiz_completed": qz_completed,
            "tasks_score": tasks_score,
            "tasks_max": cls.EXAM_TASKS_MAX_SCORE,
            "tasks": {
                "exam_task_1": {"score": t1_score, "is_completed": t1_completed},
                "exam_task_2": {"score": t2_score, "is_completed": t2_completed},
            },
            "week1_score": w1_score,
            "week2_score": w2_score,
            "week3_score": w3_score,
            "semester_score": semester_score,
            "semester_max": 60.0,
            "grand_total": grand_total,
            "grand_total_max": cls.COURSE_TOTAL_MAX_SCORE,
            "course_pass_threshold": cls.COURSE_PASS_THRESHOLD,
            "is_course_completed": is_course_completed,
            "progress_percent": progress_percent,
            "grade_letter": cls._compute_letter_grade(grand_total),
        }
