"""Negative test cases for API payload validation and edge conditions."""

import os
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_empty_code_submission_returns_422() -> None:
    """Verify empty or whitespace-only code returns HTTP 422 Unprocessable Entity."""
    res1 = client.post("/api/week1/practice/task_1/run", json={"code": ""})
    assert res1.status_code == 422

    res2 = client.post("/api/week1/practice/task_1/run", json={"code": "   \n  \t  "})
    assert res2.status_code == 422


def test_missing_payload_field_returns_422() -> None:
    """Verify missing required JSON body fields returns HTTP 422."""
    res = client.post("/api/week1/practice/task_1/run", json={})
    assert res.status_code == 422


def test_empty_quiz_answers_returns_422() -> None:
    """Verify empty answers dictionary returns HTTP 422."""
    res = client.post("/api/week1/quiz/check", json={"answers": {}})
    assert res.status_code == 422


def test_invalid_task_id_returns_404() -> None:
    """Verify non-existent practice task ID returns HTTP 404."""
    res = client.post(
        "/api/week1/practice/nonexistent_task_999/run",
        json={"code": "class A:\n    pass\n"},
    )
    assert res.status_code == 404
    assert "Unknown practice task" in res.json()["detail"]


def test_invalid_week_module_returns_404() -> None:
    """Verify non-existent week number returns HTTP 404."""
    res = client.get("/api/weeks/999/progress")
    assert res.status_code == 404


def test_smoke_endpoint_in_public_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify /api/runner/smoke returns 403 Forbidden when PUBLIC_MODE is enabled."""
    monkeypatch.setenv("PUBLIC_MODE", "1")
    res = client.post("/api/runner/smoke")
    assert res.status_code == 403
    assert "disabled in public mode" in res.json()["detail"]
