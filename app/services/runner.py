"""RunnerService for isolated execution of tests in a sandbox."""

import os
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

from app.config import settings
from app.services.ast_validator import ASTValidator


@dataclass
class RunResult:
    status: str
    output: str
    execution_time_ms: float
    passed: bool


class RunnerService:
    """Safely executes student solution against test suite in isolated sandbox."""

    @classmethod
    def run_code(
        cls,
        code: str,
        test_code: str,
        timeout: float | None = None,
    ) -> RunResult:
        if timeout is None:
            timeout = settings.runner_timeout_seconds

        is_safe, error = ASTValidator.validate(code)
        if not is_safe:
            return RunResult(
                status="SECURITY_VIOLATION",
                output=f"Security violation rejected: {error}",
                execution_time_ms=0.0,
                passed=False,
            )

        start_time = time.perf_counter()
        tmp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)

        try:
            tmp_path = Path(tmp_dir.name)
            solution_file = tmp_path / "solution.py"
            test_file = tmp_path / "test_solution.py"

            solution_file.write_text(code, encoding="utf-8")
            test_file.write_text(test_code, encoding="utf-8")

            # Minimal sanitized environment
            safe_env = {
                "SYSTEMROOT": os.environ.get("SYSTEMROOT", "C:\\Windows"),
                "PATH": os.environ.get("PATH", ""),
                "TEMP": str(tmp_path),
                "TMP": str(tmp_path),
            }

            cmd = [
                sys.executable,
                "-I",
                "-m",
                "pytest",
                "-o",
                "pythonpath=.",
                "test_solution.py",
                "-v",
            ]

            proc = subprocess.run(
                cmd,
                cwd=str(tmp_path),
                capture_output=True,
                text=True,
                env=safe_env,
                timeout=timeout,
            )

            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            combined_output = f"{proc.stdout}\n{proc.stderr}".strip()

            if proc.returncode == 0:
                return RunResult(
                    status="PASSED",
                    output=combined_output,
                    execution_time_ms=elapsed_ms,
                    passed=True,
                )
            else:
                return RunResult(
                    status="FAILED",
                    output=combined_output,
                    execution_time_ms=elapsed_ms,
                    passed=False,
                )

        except subprocess.TimeoutExpired as exc:
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            stdout_str = exc.stdout if isinstance(exc.stdout, str) else ""
            stderr_str = exc.stderr if isinstance(exc.stderr, str) else ""
            combined = f"{stdout_str}\n{stderr_str}".strip()
            msg = f"Execution timed out (limit: {timeout}s)"
            if combined:
                msg = f"{msg}\n{combined}"
            return RunResult(
                status="TIMEOUT",
                output=msg,
                execution_time_ms=elapsed_ms,
                passed=False,
            )
        except Exception as exc:
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            return RunResult(
                status="ERROR",
                output=f"Runner execution error: {exc}",
                execution_time_ms=elapsed_ms,
                passed=False,
            )
        finally:
            try:
                tmp_dir.cleanup()
            except Exception:
                pass
