"""Runner router for smoke testing and execution."""

from fastapi import APIRouter
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
    """Execute reference smoke test in sandbox to verify runner health."""
    result = RunnerService.run_code(code=SMOKE_SOLUTION, test_code=SMOKE_TEST)
    return RunnerSmokeResponse(
        status=result.status,
        passed=result.passed,
        execution_time_ms=result.execution_time_ms,
        output=result.output,
    )
