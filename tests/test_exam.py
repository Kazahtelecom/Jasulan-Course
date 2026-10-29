"""Comprehensive acceptance tests for the Final Exam Module and 100-point Assessment Engine."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.content.exam import (
    EXAM_OVERVIEW,
    EXAM_PRACTICE_TASKS,
    EXAM_QUIZ_MAX_SCORE,
    EXAM_QUIZ_QUESTIONS,
    evaluate_exam_quiz,
)
from app.database.session import Base, get_db
from app.main import app
from app.models.student import Student
from app.services.ast_validator import ASTValidator
from app.services.runner import RunnerService
from app.services.scoring import ScoringService


@pytest.fixture
def db_session() -> Session:
    """Create an isolated in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session: Session) -> TestClient:
    """Create FastAPI test client with injected test DB session."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


# =============================================================================
# AC-1: Теоретический квиз экзамена (20 вопросов, 20.0 баллов)
# =============================================================================
def test_exam_quiz_balance_and_evaluation() -> None:
    """Verify that exam quiz has 20 questions, balanced lengths, equal indices, and correct scoring."""
    assert len(EXAM_QUIZ_QUESTIONS) == 20, f"Expected 20 questions, got {len(EXAM_QUIZ_QUESTIONS)}"

    index_distribution: dict[int, int] = {0: 0, 1: 0, 2: 0, 3: 0}

    for q in EXAM_QUIZ_QUESTIONS:
        options = q["options"]
        assert len(options) == 4, f"Question {q['id']} must have exactly 4 options"

        lengths = [len(opt) for opt in options]
        ratio = max(lengths) / min(lengths)
        assert ratio <= 1.65, (
            f"Question {q['id']} length ratio {ratio:.3f} exceeds threshold 1.65: lengths={lengths}"
        )

        corr_idx = q["correct_index"]
        assert corr_idx in (0, 1, 2, 3), f"Invalid correct_index {corr_idx} in {q['id']}"
        index_distribution[corr_idx] += 1

    # Check balanced index distribution: 5 of each index 0, 1, 2, 3
    assert all(count == 5 for count in index_distribution.values()), (
        f"Option indices are not equally distributed: {index_distribution}"
    )

    # Test full 20/20 evaluation
    perfect_answers = {q["id"]: q["correct_index"] for q in EXAM_QUIZ_QUESTIONS}
    eval_perfect = evaluate_exam_quiz(perfect_answers)
    assert eval_perfect["correct_count"] == 20
    assert eval_perfect["score"] == 20.0
    assert eval_perfect["max_score"] == 20.0
    assert eval_perfect["is_passed"] is True
    assert eval_perfect["total_questions"] == 20

    # Test partial evaluation (10 out of 20 = 10.0 pts -> not passed because threshold is 12.0)
    half_answers = {}
    for i, q in enumerate(EXAM_QUIZ_QUESTIONS):
        if i < 10:
            half_answers[q["id"]] = q["correct_index"]
        else:
            half_answers[q["id"]] = (q["correct_index"] + 1) % 4
    eval_half = evaluate_exam_quiz(half_answers)
    assert eval_half["correct_count"] == 10
    assert eval_half["score"] == 10.0
    assert eval_half["is_passed"] is False

    # Test passing threshold (12 out of 20 = 12.0 pts -> passed)
    pass_answers = {}
    for i, q in enumerate(EXAM_QUIZ_QUESTIONS):
        if i < 12:
            pass_answers[q["id"]] = q["correct_index"]
        else:
            pass_answers[q["id"]] = (q["correct_index"] + 1) % 4
    eval_pass = evaluate_exam_quiz(pass_answers)
    assert eval_pass["correct_count"] == 12
    assert eval_pass["score"] == 12.0
    assert eval_pass["is_passed"] is True


# =============================================================================
# AC-2: Боевые задачи экзамена в песочнице AST (2 задачи, 20.0 баллов)
# =============================================================================
def test_exam_practice_tasks_in_sandbox() -> None:
    """Verify that both exam coding tasks pass AST whitelist and run cleanly in RunnerService."""
    assert len(EXAM_PRACTICE_TASKS) == 2, f"Expected 2 tasks, got {len(EXAM_PRACTICE_TASKS)}"

    task_ids = [t["id"] for t in EXAM_PRACTICE_TASKS]
    assert "exam_task_1" in task_ids
    assert "exam_task_2" in task_ids

    for task in EXAM_PRACTICE_TASKS:
        ref_sol = task["reference_solution"]
        test_code = task["test_code"]

        # Validate AST whitelist
        is_safe, error = ASTValidator.validate(ref_sol)
        assert is_safe, f"ASTValidator failed for {task['id']}: {error}"

        # Execute in sandbox
        res = RunnerService.run_code(code=ref_sol, test_code=test_code, timeout=5.0)
        assert res.passed, f"Task {task['id']} failed in sandbox. Status={res.status}, Output=\n{res.output}"
        assert res.status == "PASSED"
        assert res.execution_time_ms < 5000.0, f"Task {task['id']} exceeded 5.0s: {res.execution_time_ms}ms"


# =============================================================================
# AC-3: Скоринг и 100-балльная итоговая ведомость курса
# =============================================================================
def test_scoring_grand_total_100(db_session: Session) -> None:
    """Verify ScoringService exam scores, 100-point course grand total, and High-Water Mark."""
    student = ScoringService.get_or_create_student(db_session, "zhasulan")

    # Initial state: 0
    init_prog = ScoringService.get_exam_progress_summary(db_session, student.id)
    assert init_prog["exam_total"] == 0.0
    assert init_prog["grand_total"] == 0.0
    assert init_prog["is_course_completed"] is False

    # Simulate Week 1, Week 2, Week 3 scores (20.0 pts each = 60.0 pts semester total)
    ScoringService.record_quiz_submission(db_session, student.id, 20.0, week_number=1)
    ScoringService.record_quiz_submission(db_session, student.id, 18.0, week_number=2)
    ScoringService.record_quiz_submission(db_session, student.id, 20.0, week_number=3)

    mid_prog = ScoringService.get_exam_progress_summary(db_session, student.id)
    assert mid_prog["week1_score"] == 20.0
    assert mid_prog["week2_score"] == 18.0
    assert mid_prog["week3_score"] == 20.0
    assert mid_prog["semester_score"] == 58.0

    # Submit Exam Task 1 (10.0 pts)
    t1_prog = ScoringService.record_exam_task_submission(
        db=db_session,
        student_id=student.id,
        task_id="exam_task_1",
        code="# test",
        passed=True,
        output="PASSED",
        status="PASSED",
    )
    assert t1_prog["tasks"]["exam_task_1"]["score"] == 10.0
    assert t1_prog["tasks"]["exam_task_1"]["is_completed"] is True
    assert t1_prog["tasks_score"] == 10.0
    assert t1_prog["exam_total"] == 10.0

    # High-Water Mark test for task: submitting failed run does NOT drop score below 10.0
    t1_failed = ScoringService.record_exam_task_submission(
        db=db_session,
        student_id=student.id,
        task_id="exam_task_1",
        code="# broken",
        passed=False,
        output="FAILED",
        status="FAILED",
    )
    assert t1_failed["tasks"]["exam_task_1"]["score"] == 10.0

    # Submit Exam Task 2 (10.0 pts)
    t2_prog = ScoringService.record_exam_task_submission(
        db=db_session,
        student_id=student.id,
        task_id="exam_task_2",
        code="# test2",
        passed=True,
        output="PASSED",
        status="PASSED",
    )
    assert t2_prog["tasks_score"] == 20.0
    assert t2_prog["exam_total"] == 20.0
    assert t2_prog["is_exam_completed"] is True

    # Submit Exam Quiz (18.0 pts)
    quiz_prog = ScoringService.record_exam_quiz_submission(
        db=db_session,
        student_id=student.id,
        quiz_score=18.0,
    )
    assert quiz_prog["quiz_score"] == 18.0
    assert quiz_prog["exam_total"] == 38.0  # 18.0 quiz + 20.0 tasks

    # High-Water Mark test for quiz: submitting lower score (e.g. 10.0) does NOT overwrite 18.0
    lower_quiz_prog = ScoringService.record_exam_quiz_submission(
        db=db_session,
        student_id=student.id,
        quiz_score=10.0,
    )
    assert lower_quiz_prog["quiz_score"] == 18.0
    assert lower_quiz_prog["exam_total"] == 38.0

    # Grand total: Semester 58.0 + Exam 38.0 = 96.0 / 100.0 (Grade A)
    assert lower_quiz_prog["grand_total"] == 96.0
    assert lower_quiz_prog["grand_total_max"] == 100.0
    assert lower_quiz_prog["is_course_completed"] is True
    assert "A" in lower_quiz_prog["grade_letter"]


# =============================================================================
# AC-4: Режим честности (скрытие готовых решений) и навигация UI
# =============================================================================
def test_exam_ui_integrity(client: TestClient) -> None:
    """Verify that /exam page renders cleanly with exam tab and strictly WITHOUT solution buttons or data-solution."""
    res = client.get("/exam")
    assert res.status_code == 200
    html = res.text

    # Header navigation has exam tab
    assert "🏆 Экзамен" in html
    assert 'href="/exam"' in html

    # Academic honesty: NO "Вставить готовое решение" button
    assert "Вставить готовое решение" not in html
    assert "fillSolutionCode" not in html

    # Academic honesty: NO data-solution attribute containing answers in textarea
    assert 'data-solution="' not in html

    # Check for exam sections
    assert "Часть 1: Тестирование" in html or "Часть 1 · Тестирование" in html
    assert "Часть 2: Практика" in html or "Часть 2 · Практика" in html
    assert "Итоговая Ведомость" in html or "Официальная ведомость" in html

    # UML diagram viewer is accessible on exam page
    assert 'id="uml-diagram-section"' in html
    assert 'id="uml-fullscreen-modal"' in html

    # Check that standard week pages also have the 🏆 Экзамен tab link
    w1_res = client.get("/week1")
    assert w1_res.status_code == 200
    assert 'href="/exam"' in w1_res.text


# =============================================================================
# AC-5: Изоляция 4 студентов и эндпоинты API экзамена
# =============================================================================
def test_multi_student_isolation_and_exam_endpoints(client: TestClient) -> None:
    """Verify independent SQLite tracking across all 4 students and API endpoints."""
    students = ["zhasulan", "roman", "arseniy", "saubakirov"]

    # Test /api/exam/progress endpoint for all 4 students
    for u in students:
        resp = client.get("/api/exam/progress", headers={"X-Student-Id": u})
        assert resp.status_code == 200
        data = resp.json()
        assert data["exam_total"] == 0.0
        assert data["grand_total_max"] == 100.0

    # Student 1 (zhasulan) completes quiz with 20.0 pts
    q_answers = {q["id"]: q["correct_index"] for q in EXAM_QUIZ_QUESTIONS}
    resp1 = client.post(
        "/api/exam/quiz/check",
        json={"answers": q_answers},
        headers={"X-Student-Id": "zhasulan"},
    )
    assert resp1.status_code == 200
    data1 = resp1.json()
    assert data1["score"] == 20.0
    assert data1["progress"]["quiz_score"] == 20.0
    assert data1["progress"]["exam_total"] == 20.0

    # Student 2 (roman) still has 0.0 pts (isolation check)
    resp2 = client.get("/api/exam/progress", headers={"X-Student-Id": "roman"})
    assert resp2.status_code == 200
    assert resp2.json()["exam_total"] == 0.0
    assert resp2.json()["quiz_score"] == 0.0

    # Student 2 (roman) solves exam_task_1 via API runner
    task1 = next(t for t in EXAM_PRACTICE_TASKS if t["id"] == "exam_task_1")
    resp_task = client.post(
        "/api/exam/practice/exam_task_1/run",
        json={"code": task1["reference_solution"]},
        headers={"X-Student-Id": "roman"},
    )
    assert resp_task.status_code == 200
    task_res = resp_task.json()
    assert task_res["passed"] is True
    assert task_res["progress"]["tasks"]["exam_task_1"]["score"] == 10.0
    assert task_res["progress"]["exam_total"] == 10.0

    # Student 3 (arseniy) and Student 4 (saubakirov) remain untouched at 0.0
    for u in ("arseniy", "saubakirov"):
        p = client.get("/api/exam/progress", headers={"X-Student-Id": u}).json()
        assert p["exam_total"] == 0.0
        assert p["quiz_score"] == 0.0
        assert p["tasks"]["exam_task_1"]["score"] == 0.0

    # Comprehensive /api/students/scores check includes exam
    scores_resp = client.get("/api/students/scores", headers={"X-Student-Id": "roman"})
    assert scores_resp.status_code == 200
    s_data = scores_resp.json()
    assert "week1" in s_data
    assert "week2" in s_data
    assert "week3" in s_data
    assert "exam" in s_data
    assert s_data["exam"]["tasks"]["exam_task_1"]["score"] == 10.0
