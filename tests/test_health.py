"""Tests for health and foundation API endpoints."""

from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    """Verify GET /api/health returns 200 and expected component readiness."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["db"] == "connected"
    assert data["runner"] == "ready"


def test_index_dashboard(client: TestClient) -> None:
    """Verify root / returns HTML dashboard with Zero-Build CDN scripts."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.text
    assert "Web-OOP" in html
    assert "cdn.tailwindcss.com" in html
    assert "cdn.jsdelivr.net/npm/mermaid" in html
    assert "Passenger" in html
    assert "Validator" in html


def test_runner_smoke_api(client: TestClient) -> None:
    """Verify POST /api/runner/smoke executes reference test successfully."""
    response = client.post("/api/runner/smoke")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "PASSED"
    assert data["passed"] is True
    assert data["execution_time_ms"] > 0
    assert "passed" in data["output"].lower()


def test_swagger_docs(client: TestClient) -> None:
    """Verify /docs Swagger documentation is available."""
    response = client.get("/docs")
    assert response.status_code == 200
