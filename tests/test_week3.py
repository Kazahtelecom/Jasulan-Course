"""Tests for Week 3 module: GoF Patterns and Clean Architecture (Quiz 20.0 max, ungraded Practice)."""

from pathlib import Path

from fastapi.testclient import TestClient

from app.content.week_1 import QUIZ_QUESTIONS as WEEK1_QUIZ_QUESTIONS
from app.content.week_2 import QUIZ_QUESTIONS as WEEK2_QUIZ_QUESTIONS
from app.content.week_3 import (
    PRACTICE_TASKS,
    QUIZ_MAX_SCORE,
    QUIZ_QUESTIONS,
    THEORY_SECTIONS,
    WALKTHROUGH_EXAMPLE,
    evaluate_quiz,
)
from app.services.runner import RunnerService


def test_week3_page_and_navigation_layout(client: TestClient) -> None:
    """Verify /week3 renders Dark Cyberpunk platform, week switcher, 5 tabs, and local assets."""
    res = client.get("/week3")
    assert res.status_code == 200
    html = res.text

    assert 'data-active-week="3"' in html
    assert 'href="/week1"' in html
    assert 'href="/week2"' in html
    assert 'href="/week3"' in html
    assert "Неделя 1 · Инкапсуляция" in html
    assert "Неделя 2 · SOLID и DI" in html
    assert "Неделя 3 · Паттерны GoF" in html

    for tab_label in ("Главная", "Теория", "Практика", "Тестирование", "Результаты"):
        assert tab_label in html
    for panel_id in (
        "panel-home",
        "panel-theory",
        "panel-practice",
        "panel-quiz",
        "panel-results",
    ):
        assert panel_id in html

    assert "Вставить готовое решение" in html
    assert "mermaid.min.js" not in html

    images_dir = Path(__file__).resolve().parent.parent / "app" / "static" / "images"
    for image_name in ("week3_hero.jpg", "gof_patterns.jpg", "clean_arch_layers.jpg"):
        img_path = images_dir / image_name
        assert img_path.is_file(), f"Missing Week 3 asset: {img_path}"
        assert img_path.stat().st_size > 10_240, f"Asset too small: {img_path}"
        assert f"/static/images/{image_name}" in html
        img_res = client.get(f"/static/images/{image_name}")
        assert img_res.status_code == 200


def test_week3_theory_and_walkthrough() -> None:
    """Verify 4 progressive GoF & Clean Arch theory sections and 4-step TicketIssuer/Facade walkthrough."""
    assert len(THEORY_SECTIONS) == 4
    expected_ids = [
        "w3_step_1_creational",
        "w3_step_2_structural",
        "w3_step_3_behavioral",
        "w3_step_4_clean_arch",
    ]
    assert [sec["id"] for sec in THEORY_SECTIONS] == expected_ids
    for sec in THEORY_SECTIONS:
        assert sec["bad_code"].strip()
        assert sec["good_code"].strip()
        assert sec["lead"].strip()
        assert len(sec["anatomy_cards"]) >= 1

    assert len(WALKTHROUGH_EXAMPLE["steps"]) == 4
    assert "class TicketIssuer" in WALKTHROUGH_EXAMPLE["code"]
    assert "class TransitTerminalFacade" in WALKTHROUGH_EXAMPLE["code"]
    assert "def tap(" in WALKTHROUGH_EXAMPLE["code"]


def test_week3_practice_trainer_and_zero_score(client: TestClient) -> None:
    """Verify 3 connected practice steps pass with reference solutions and award 0.0 points."""
    assert len(PRACTICE_TASKS) == 3
    assert [t["id"] for t in PRACTICE_TASKS] == ["w3_task_1", "w3_task_2", "w3_task_3"]

    for task in PRACTICE_TASKS:
        assert task["max_score"] == 0.0
        starter_res = RunnerService.run_code(
            code=task["starter_code"],
            test_code=task["test_code"],
        )
        assert starter_res.passed is False

        run_res = client.post(
            f"/api/week3/practice/{task['id']}/run",
            json={"code": task["reference_solution"]},
        )
        assert run_res.status_code == 200
        body = run_res.json()
        assert body["passed"] is True, f"{task['id']} failed: {body['output']}"
        assert body["status"] == "PASSED"
        assert body["progress"]["tasks"][task["id"]]["is_completed"] is True
        assert body["progress"]["total_score"] == 0.0

    prog = client.get("/api/week3/progress").json()
    assert prog["week_number"] == 3
    assert prog["tasks_completed"] == 3
    assert prog["total_score"] == 0.0
    assert prog["is_completed"] is False


def test_week3_quiz_grading_hwm_and_isolation(client: TestClient) -> None:
    """Verify 10-question quiz (20.0 max, pass >= 12.0, HWM) and isolated student state."""
    assert len(QUIZ_QUESTIONS) == 10
    assert QUIZ_MAX_SCORE == 20.0
    for idx, q in enumerate(QUIZ_QUESTIONS, start=1):
        assert q["id"] == f"w3_q{idx}"
        assert len(q["options"]) == 4

    perfect_eval = evaluate_quiz({q["id"]: q["correct_index"] for q in QUIZ_QUESTIONS})
    assert perfect_eval["correct_count"] == 10
    assert perfect_eval["score"] == 20.0
    assert perfect_eval["max_score"] == 20.0
    assert perfect_eval["points_per_question"] == 2.0

    # 1. Below pass threshold: 5/10 correct -> 10.0 points (is_completed == False)
    five_correct = {
        q["id"]: (q["correct_index"] if idx < 5 else (q["correct_index"] + 1) % 4)
        for idx, q in enumerate(QUIZ_QUESTIONS)
    }
    res_5 = client.post("/api/week3/quiz/check", json={"answers": five_correct})
    assert res_5.status_code == 200
    data_5 = res_5.json()
    assert data_5["score"] == 10.0
    assert data_5["progress"]["total_score"] == 10.0
    assert data_5["progress"]["is_completed"] is False
    assert data_5["progress"]["progress_percent"] == 50

    # 2. Pass threshold reached: 6/10 correct -> 12.0 points (is_completed == True)
    six_correct = {
        q["id"]: (q["correct_index"] if idx < 6 else (q["correct_index"] + 1) % 4)
        for idx, q in enumerate(QUIZ_QUESTIONS)
    }
    res_6 = client.post("/api/week3/quiz/check", json={"answers": six_correct})
    assert res_6.status_code == 200
    data_6 = res_6.json()
    assert data_6["score"] == 12.0
    assert data_6["progress"]["total_score"] == 12.0
    assert data_6["progress"]["is_completed"] is True
    assert data_6["progress"]["progress_percent"] == 60

    # 3. High-Water Mark: lower retry (2/10 = 4.0 pts) does not reduce saved 12.0 score
    two_correct = {
        q["id"]: (q["correct_index"] if idx < 2 else (q["correct_index"] + 1) % 4)
        for idx, q in enumerate(QUIZ_QUESTIONS)
    }
    res_2 = client.post("/api/week3/quiz/check", json={"answers": two_correct})
    assert res_2.status_code == 200
    data_2 = res_2.json()
    assert data_2["score"] == 4.0
    assert data_2["progress"]["total_score"] == 12.0
    assert data_2["progress"]["is_completed"] is True

    # 4. Perfect score: 10/10 correct -> 20.0 points (100%)
    perfect_w3 = {q["id"]: q["correct_index"] for q in QUIZ_QUESTIONS}
    res_10 = client.post("/api/week3/quiz/check", json={"answers": perfect_w3})
    assert res_10.status_code == 200
    data_10 = res_10.json()
    assert data_10["score"] == 20.0
    assert data_10["progress"]["total_score"] == 20.0
    assert data_10["progress"]["is_completed"] is True
    assert data_10["progress"]["progress_percent"] == 100

    # 5. Multi-student isolation: Roman submits quiz on week 3 without affecting default student
    res_roman = client.post(
        "/api/week3/quiz/check",
        headers={"X-Student-Id": "roman"},
        json={"answers": two_correct},
    )
    assert res_roman.status_code == 200
    assert res_roman.json()["score"] == 4.0
    assert res_roman.json()["progress"]["total_score"] == 4.0

    # Default student still has 20.0
    default_prog = client.get("/api/week3/progress").json()
    assert default_prog["total_score"] == 20.0


def test_week3_theory_complete_endpoint(client: TestClient) -> None:
    """Verify POST /api/week3/theory/complete marks theory complete in database."""
    res = client.post("/api/week3/theory/complete", headers={"X-Student-Id": "arseniy"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "COMPLETED"
    assert data["theory_completed"] is True

    prog = client.get("/api/week3/progress", headers={"X-Student-Id": "arseniy"}).json()
    assert prog["theory_completed"] is True
