"""Tests for Week 2 module: SOLID and Dependency Injection (Quiz 20.0 max, ungraded Practice)."""

from pathlib import Path

from fastapi.testclient import TestClient

from app.content.week_1 import QUIZ_QUESTIONS as WEEK1_QUIZ_QUESTIONS
from app.content.week_2 import (
    PRACTICE_TASKS,
    QUIZ_MAX_SCORE,
    QUIZ_QUESTIONS,
    THEORY_SECTIONS,
    WALKTHROUGH_EXAMPLE,
    evaluate_quiz,
)
from app.services.runner import RunnerService


def test_week2_page_and_navigation_layout(client: TestClient) -> None:
    """Verify /week2 renders Dark Cyberpunk platform, week switcher, 5 tabs, and local assets."""
    res = client.get("/week2")
    assert res.status_code == 200
    html = res.text

    assert 'data-active-week="2"' in html
    assert 'href="/week1"' in html
    assert 'href="/week2"' in html
    assert "Неделя 1 · Инкапсуляция" in html
    assert "Неделя 2 · SOLID и DI" in html

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
    for image_name in ("week2_hero.jpg", "solid_modular.jpg", "di_ports.jpg"):
        img_path = images_dir / image_name
        assert img_path.is_file(), f"Missing Week 2 asset: {img_path}"
        assert img_path.stat().st_size > 10_240, f"Asset too small: {img_path}"
        assert f"/static/images/{image_name}" in html
        img_res = client.get(f"/static/images/{image_name}")
        assert img_res.status_code == 200


def test_week2_theory_and_walkthrough() -> None:
    """Verify 4 progressive SOLID & DI theory sections and 4-step TerminalValidator walkthrough."""
    assert len(THEORY_SECTIONS) == 4
    expected_ids = [
        "w2_step_1_srp",
        "w2_step_2_ocp",
        "w2_step_3_lsp_isp",
        "w2_step_4_dip_di",
    ]
    assert [sec["id"] for sec in THEORY_SECTIONS] == expected_ids
    for sec in THEORY_SECTIONS:
        assert sec["bad_code"].strip()
        assert sec["good_code"].strip()
        assert sec["lead"].strip()
        assert len(sec["anatomy_cards"]) >= 1

    assert len(WALKTHROUGH_EXAMPLE["steps"]) == 4
    assert "class TerminalValidator:" in WALKTHROUGH_EXAMPLE["code"]
    assert "def __init__(" in WALKTHROUGH_EXAMPLE["code"]


def test_week2_practice_trainer_and_zero_score(client: TestClient) -> None:
    """Verify 3 connected practice steps pass with reference solutions and award 0.0 points."""
    assert len(PRACTICE_TASKS) == 3
    assert [t["id"] for t in PRACTICE_TASKS] == ["w2_task_1", "w2_task_2", "w2_task_3"]

    for task in PRACTICE_TASKS:
        assert task["max_score"] == 0.0
        starter_res = RunnerService.run_code(
            code=task["starter_code"],
            test_code=task["test_code"],
        )
        assert starter_res.passed is False

        run_res = client.post(
            f"/api/week2/practice/{task['id']}/run",
            json={"code": task["reference_solution"]},
        )
        assert run_res.status_code == 200
        body = run_res.json()
        assert body["passed"] is True, f"{task['id']} failed: {body['output']}"
        assert body["status"] == "PASSED"
        assert body["progress"]["tasks"][task["id"]]["is_completed"] is True
        assert body["progress"]["total_score"] == 0.0

    prog = client.get("/api/week2/progress").json()
    assert prog["week_number"] == 2
    assert prog["tasks_completed"] == 3
    assert prog["total_score"] == 0.0
    assert prog["is_completed"] is False


def test_week2_quiz_grading_hwm_and_week1_independence(client: TestClient) -> None:
    """Verify 10-question quiz (20.0 max, pass >= 12.0, HWM) and isolated Week 1 / Week 2 state."""
    assert len(QUIZ_QUESTIONS) == 10
    assert QUIZ_MAX_SCORE == 20.0
    for idx, q in enumerate(QUIZ_QUESTIONS, start=1):
        assert q["id"] == f"w2_q{idx}"
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
    res_5 = client.post("/api/week2/quiz/check", json={"answers": five_correct})
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
    res_6 = client.post("/api/week2/quiz/check", json={"answers": six_correct})
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
    res_2 = client.post("/api/week2/quiz/check", json={"answers": two_correct})
    assert res_2.status_code == 200
    data_2 = res_2.json()
    assert data_2["score"] == 4.0
    assert data_2["progress"]["total_score"] == 12.0
    assert data_2["progress"]["is_completed"] is True

    # 4. Perfect score: 10/10 correct -> 20.0 points (100%)
    perfect_w2 = {q["id"]: q["correct_index"] for q in QUIZ_QUESTIONS}
    res_10 = client.post("/api/week2/quiz/check", json={"answers": perfect_w2})
    assert res_10.status_code == 200
    data_10 = res_10.json()
    assert data_10["score"] == 20.0
    assert data_10["progress"]["total_score"] == 20.0
    assert data_10["progress"]["is_completed"] is True
    assert data_10["progress"]["progress_percent"] == 100

    # 5. Week 1 progress remains untouched (0.0 points)
    w1_prog = client.get("/api/week1/progress").json()
    assert w1_prog["week_number"] == 1
    assert w1_prog["total_score"] == 0.0
    assert w1_prog["tasks_completed"] == 0
    assert w1_prog["is_completed"] is False

    # 6. Submitting Week 1 quiz (14.0 pts) does not overwrite Week 2 progress (20.0 pts)
    seven_w1 = {
        q["id"]: (q["correct_index"] if idx < 7 else (q["correct_index"] + 1) % 4)
        for idx, q in enumerate(WEEK1_QUIZ_QUESTIONS)
    }
    w1_quiz_res = client.post("/api/week1/quiz/check", json={"answers": seven_w1})
    assert w1_quiz_res.status_code == 200
    assert w1_quiz_res.json()["progress"]["total_score"] == 14.0

    w2_prog_after = client.get("/api/week2/progress").json()
    assert w2_prog_after["total_score"] == 20.0
    assert w2_prog_after["is_completed"] is True
