"""Tests for Week 1 HTTP routes, page templates, and API endpoints."""

from fastapi.testclient import TestClient

from app.content.week_1.lab import LAB_TASK
from app.content.week_1.practice import PRACTICE_TASK
from app.content.week_1.quiz import QUIZ_QUESTIONS


def test_week1_page_render(client: TestClient):
    """Verify that GET /week1 renders the full 4-tab Zero-Build page."""
    response = client.get("/week1")
    assert response.status_code == 200
    html = response.text

    # Verify tabs exist
    assert "tab-lecture" in html
    assert "tab-quiz" in html
    assert "tab-practice" in html
    assert "tab-lab" in html

    # Verify scripts & CDN
    assert "cdn.tailwindcss.com" in html
    assert "mermaid" in html
    assert "/static/js/week1.js" in html

    # Verify student identity & score header
    assert "header-score-badge" in html
    assert "header-status-badge" in html


def test_index_dashboard_renders_week1_module(client: TestClient):
    """Verify that the main dashboard includes the Week 1 educational module card."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.text

    assert "Неделя 1: Основы ООП, инкапсуляция и защита инвариантов" in html
    assert 'href="/week1"' in html
    assert "week1-total-score" in html
    assert "week1-status-badge" in html


def test_quiz_endpoint(client: TestClient):
    """Verify POST /api/week1/quiz/check scoring and feedback generation."""
    # Submit perfect answers
    answers = {q["id"]: q["correct_option"] for q in QUIZ_QUESTIONS}
    response = client.post("/api/week1/quiz/check", json={"answers": answers})
    assert response.status_code == 200
    data = response.json()

    assert data["score"] == 3.0
    assert data["correct_count"] == 5
    assert data["total_week_score"] == 3.0
    assert data["is_completed"] is False  # 3.0 < 12.0
    assert "q1" in data["details"]
    assert data["details"]["q1"]["is_correct"] is True


def test_practice_run_endpoint(client: TestClient):
    """Verify POST /api/week1/practice/run executes in sandbox and updates score."""
    # Test valid reference solution
    response = client.post(
        "/api/week1/practice/run",
        json={"code": PRACTICE_TASK["reference_solution"]},
    )
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "PASSED"
    assert data["passed"] is True
    assert data["passed_tests"] == 7
    assert data["score"] == 7.0
    assert data["total_week_score"] == 7.0

    # Test security violation rejection
    bad_response = client.post(
        "/api/week1/practice/run",
        json={"code": "import os\nos.system('echo hacked')"},
    )
    assert bad_response.status_code == 200
    bad_data = bad_response.json()
    assert bad_data["status"] == "SECURITY_VIOLATION"
    assert bad_data["passed"] is False
    assert bad_data["score"] == 0.0


def test_lab_run_endpoint(client: TestClient):
    """Verify POST /api/week1/lab/run executes in sandbox and passes completion threshold."""
    # First submit quiz (3.0) and practice (7.0)
    quiz_ans = {q["id"]: q["correct_option"] for q in QUIZ_QUESTIONS}
    client.post("/api/week1/quiz/check", json={"answers": quiz_ans})
    client.post("/api/week1/practice/run", json={"code": PRACTICE_TASK["reference_solution"]})

    # Now submit perfect lab (10.0) -> Total 20.0 -> is_completed = True
    response = client.post(
        "/api/week1/lab/run",
        json={"code": LAB_TASK["reference_solution"]},
    )
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "PASSED"
    assert data["passed"] is True
    assert data["passed_tests"] == 10
    assert data["score"] == 10.0
    assert data["total_week_score"] == 20.0
    assert data["is_completed"] is True


def test_week1_progress_api_endpoint(client: TestClient):
    """Verify GET /api/week1/progress returns full progress object."""
    response = client.get("/api/week1/progress")
    assert response.status_code == 200
    data = response.json()

    assert data["topic_id"] == "week_1"
    assert data["max_score"] == 20.0
    assert data["passing_threshold"] == 12.0
    assert "score" in data
    assert "is_completed" in data
