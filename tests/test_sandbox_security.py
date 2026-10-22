"""Security tests for sandbox isolation, AST whitelist, and exploit attempts."""

import pytest

from app.content.week_1 import PRACTICE_TASKS as W1_TASKS
from app.content.week_2 import PRACTICE_TASKS as W2_TASKS
from app.services.ast_validator import ASTValidator
from app.services.runner import RunnerService


def test_subclasses_exploit_blocked() -> None:
    """Verify that trying to break sandbox via __subclasses__ is blocked by ASTValidator."""
    exploit_payloads = [
        "().__class__.__subclasses__()",
        "[].__class__.__base__.__subclasses__()",
        "object.__subclasses__()",
        "x = ''.__class__.__mro__[1].__subclasses__()",
    ]
    for code in exploit_payloads:
        is_safe, error = ASTValidator.validate(code)
        assert is_safe is False, f"Expected exploit to be blocked: {code}"
        assert "Forbidden system attribute access" in str(error) or "Forbidden" in str(error)


def test_dunder_and_builtins_blocked() -> None:
    """Verify system attributes and __builtins__ identifiers are blocked."""
    exploit_payloads = [
        "__builtins__['open']('/etc/passwd')",
        "getattr(object, '__subclasses__')",
        "d = {'a': 1}; d.__dict__",
        "f = lambda: 1; f.__globals__",
        "f.__code__",
    ]
    for code in exploit_payloads:
        is_safe, error = ASTValidator.validate(code)
        assert is_safe is False, f"Expected exploit to be blocked: {code}"


def test_forbidden_modules_and_calls_blocked() -> None:
    """Verify modules like importlib, pathlib, ctypes and calls like open, eval are blocked."""
    exploit_payloads = [
        "import importlib\nimportlib.import_module('os')",
        "from pathlib import Path\nPath('.').read_text()",
        "import ctypes",
        "open('test.txt', 'w')",
        "eval('1+1')",
        "exec('x = 10')",
        "compile('x = 1', '<string>', 'exec')",
    ]
    for code in exploit_payloads:
        is_safe, error = ASTValidator.validate(code)
        assert is_safe is False, f"Expected exploit to be blocked: {code}"


def test_code_size_limit_15kb() -> None:
    """Verify that code submissions larger than 15 KB are rejected before AST parsing."""
    large_code = "# Comment\n" + ("x = 1\n" * 3000)
    assert len(large_code.encode("utf-8")) > 15 * 1024

    is_safe, error = ASTValidator.validate(large_code)
    assert is_safe is False
    assert "Code size exceeds maximum limit of 15 KB" in str(error)


def test_infinite_loop_timeout() -> None:
    """Verify RunnerService times out safely without hanging server."""
    code = """
class InfiniteWorker:
    def work(self) -> None:
        while True:
            pass
"""
    test_code = """
from solution import InfiniteWorker

def test_infinite():
    w = InfiniteWorker()
    w.work()
"""
    result = RunnerService.run_code(code=code, test_code=test_code, timeout=1.5)
    assert result.status == "TIMEOUT"
    assert result.passed is False
    assert "timed out" in result.output.lower()


def test_all_reference_solutions_pass_ast_whitelist() -> None:
    """Verify 0 false positives: all 6 reference solutions from Week 1 & 2 pass ASTValidator."""
    all_tasks = W1_TASKS + W2_TASKS
    assert len(all_tasks) == 6

    for task in all_tasks:
        sol = task["reference_solution"]
        is_safe, error = ASTValidator.validate(sol)
        assert is_safe is True, f"Reference solution for task {task['id']} failed validation: {error}"
