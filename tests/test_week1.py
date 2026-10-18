"""Tests for Week 1 module: Quiz-only grading (20.0 max) and ungraded Practice trainer."""

from fastapi.testclient import TestClient

from app.content.week_1 import (
    PRACTICE_TASKS,
    QUIZ_QUESTIONS,
    THEORY_SECTIONS,
    WALKTHROUGH_EXAMPLE,
    evaluate_quiz,
)
from app.services.runner import RunnerService


def test_week1_page_and_navigation_layout(client: TestClient) -> None:
    """Verify / and /week1 render Dark Cyberpunk platform with 5 sub-tabs and theory/walkthrough."""
    assert len(THEORY_SECTIONS) == 4
    assert len(WALKTHROUGH_EXAMPLE["steps"]) == 4
    assert "class Passenger:" in WALKTHROUGH_EXAMPLE["code"]
    assert "class Validator:" in WALKTHROUGH_EXAMPLE["code"]

    for path in ("/", "/week1"):
        res = client.get(path)
        assert res.status_code == 200
        html = res.text
        assert "Учебная платформа" in html
        assert "Учимся вместе" in html
        assert "Неделя 1 · Инкапсуляция" in html
        for tab_label in ("Главная", "Теория", "Практика", "Тестирование", "Результаты"):
            assert tab_label in html
        assert "Вставить готовое решение" in html
        assert "/static/images/week1_hero.jpg" in html
        assert "/static/images/oop_blueprint.jpg" in html
        assert "/static/images/oop_encapsulation.jpg" in html


def test_practice_reference_solutions_pass() -> None:
    """Verify all 3 connected SmartCard practice tasks pass with their reference solutions."""
    assert len(PRACTICE_TASKS) == 3
    for task in PRACTICE_TASKS:
        result = RunnerService.run_code(
            code=task["reference_solution"],
            test_code=task["test_code"],
        )
        assert result.passed is True, f"{task['id']} failed: {result.output}"
        assert result.status == "PASSED"


def test_practice_starter_code_fails_before_completion() -> None:
    """Verify starter templates do not pass before the student writes or inserts the solution."""
    for task in PRACTICE_TASKS:
        result = RunnerService.run_code(
            code=task["starter_code"],
            test_code=task["test_code"],
        )
        assert result.passed is False


def test_quiz_evaluation_logic() -> None:
    """Verify final quiz has 10 questions worth 2.0 points each (20.0 max)."""
    assert len(QUIZ_QUESTIONS) == 10
    perfect_answers = {q["id"]: q["correct_index"] for q in QUIZ_QUESTIONS}
    res = evaluate_quiz(perfect_answers)
    assert res["correct_count"] == 10
    assert res["score"] == 20.0
    assert res["max_score"] == 20.0


def test_quiz_only_scoring_and_ungraded_practice(client: TestClient) -> None:
    """Verify points come exclusively from Quiz (20.0 max, pass >= 12.0, HWM) and Practice is 0."""
    # 1. Initial progress
    prog = client.get("/api/week1/progress").json()
    assert prog["total_score"] == 0.0
    assert prog["max_score"] == 20.0
    assert prog["pass_threshold"] == 12.0
    assert prog["is_completed"] is False

    # 2. Running practice tasks marks trainer steps done, but requires/adds 0 points
    for task in PRACTICE_TASKS:
        run_res = client.post(
            f"/api/week1/practice/{task['id']}/run",
            json={"code": task["reference_solution"]},
        )
        assert run_res.status_code == 200
        body = run_res.json()
        assert body["passed"] is True

    prog_after_practice = client.get("/api/week1/progress").json()
    assert prog_after_practice["tasks_completed"] == 3
    assert prog_after_practice["total_score"] == 0.0
    assert prog_after_practice["is_completed"] is False

    # 3. Partial quiz pass: 6 correct answers out of 10 -> 12.0 points (passes threshold >= 12.0)
    six_correct = {
        q["id"]: (q["correct_index"] if idx < 6 else (q["correct_index"] + 1) % 4)
        for idx, q in enumerate(QUIZ_QUESTIONS)
    }
    quiz_res_6 = client.post("/api/week1/quiz/check", json={"answers": six_correct})
    assert quiz_res_6.status_code == 200
    data_6 = quiz_res_6.json()
    assert data_6["score"] == 12.0
    assert data_6["progress"]["total_score"] == 12.0
    assert data_6["progress"]["is_completed"] is True
    assert data_6["progress"]["progress_percent"] == 60

    # 4. High-Water Mark: lower attempt (2 correct = 4.0 pts) does not reduce saved 12.0 score
    two_correct = {
        q["id"]: (q["correct_index"] if idx < 2 else (q["correct_index"] + 1) % 4)
        for idx, q in enumerate(QUIZ_QUESTIONS)
    }
    quiz_res_2 = client.post("/api/week1/quiz/check", json={"answers": two_correct})
    assert quiz_res_2.status_code == 200
    data_2 = quiz_res_2.json()
    assert data_2["score"] == 4.0
    assert data_2["progress"]["total_score"] == 12.0
    assert data_2["progress"]["is_completed"] is True

    # 5. Complete final quiz (10 correct = 20.0 points -> 100% score and completed status)
    perfect_answers = {q["id"]: q["correct_index"] for q in QUIZ_QUESTIONS}
    quiz_res = client.post("/api/week1/quiz/check", json={"answers": perfect_answers})
    assert quiz_res.status_code == 200
    quiz_data = quiz_res.json()
    assert quiz_data["score"] == 20.0
    assert quiz_data["progress"]["total_score"] == 20.0
    assert quiz_data["progress"]["is_completed"] is True
    assert quiz_data["progress"]["progress_percent"] == 100
