"""Runner router for smoke testing and execution."""

import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.runner import RunnerService

router = APIRouter(prefix="/api/runner", tags=["runner"])

SMOKE_SOLUTION = """
class SmokeChecker:
    @staticmethod
    def is_healthy() -> bool:
        return True
"""

SMOKE_TEST = """
from solution import SmokeChecker

def test_smoke_checker():
    assert SmokeChecker.is_healthy() is True
"""


class RunnerSmokeResponse(BaseModel):
    status: str
    passed: bool
    execution_time_ms: float
    output: str


@router.post("/smoke", response_model=RunnerSmokeResponse)
def run_smoke_test() -> RunnerSmokeResponse:
    """Execute reference smoke test in sandbox to verify runner health.

    Disabled when PUBLIC_MODE is active.
    """
    if os.environ.get("PUBLIC_MODE", "0").lower() in ("1", "true"):
        raise HTTPException(status_code=403, detail="Smoke endpoint disabled in public mode")

    result = RunnerService.run_code(code=SMOKE_SOLUTION, test_code=SMOKE_TEST)
    return RunnerSmokeResponse(
        status=result.status,
        passed=result.passed,
        execution_time_ms=result.execution_time_ms,
        output=result.output,
    )
