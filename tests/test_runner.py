"""Tests for RunnerService sandbox and AST security validator."""

from app.services.ast_validator import ASTValidator
from app.services.runner import RunnerService


def test_ast_validator_safe_oop_code() -> None:
    """Verify standard OOP constructs are accepted without false positives."""
    code = """
class BaseEntity:
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name


class Passenger(BaseEntity):
    def __init__(self, name: str, balance: float) -> None:
        super().__init__(name)
        self.balance = balance

    def top_up(self, amount: float) -> None:
        if amount > 0:
            self.balance += amount
"""
    is_safe, error = ASTValidator.validate(code)
    assert is_safe is True
    assert error is None


def test_ast_validator_forbidden_imports() -> None:
    """Verify ASTValidator blocks dangerous system imports."""
    forbidden_snippets = [
        "import os",
        "import sys",
        "import subprocess",
        "import shutil",
        "import socket",
        "from os import path",
        "from subprocess import Popen",
        "import os.path",
    ]
    for snippet in forbidden_snippets:
        is_safe, error = ASTValidator.validate(snippet)
        assert is_safe is False
        assert "Forbidden module import" in str(error)


def test_ast_validator_forbidden_calls() -> None:
    """Verify ASTValidator blocks dynamic code evaluation calls."""
    forbidden_calls = [
        "eval('2 + 2')",
        "exec('a = 5')",
        "__import__('os')",
    ]
    for call in forbidden_calls:
        is_safe, error = ASTValidator.validate(call)
        assert is_safe is False
        assert "Forbidden function call" in str(error)


def test_runner_successful_execution() -> None:
    """Verify valid solution passes test suite with PASSED status."""
    solution = """
class Calculator:
    def add(self, a: int, b: int) -> int:
        return a + b
"""
    test_code = """
from solution import Calculator

def test_add():
    calc = Calculator()
    assert calc.add(2, 3) == 5
"""
    result = RunnerService.run_code(solution, test_code)
    assert result.status == "PASSED"
    assert result.passed is True
    assert result.execution_time_ms > 0
    assert "1 passed" in result.output


def test_runner_failed_assertion() -> None:
    """Verify assertion failure in student code results in FAILED status."""
    solution = """
class Calculator:
    def add(self, a: int, b: int) -> int:
        return a - b  # Intentional bug
"""
    test_code = """
from solution import Calculator

def test_add():
    calc = Calculator()
    assert calc.add(2, 3) == 5
"""
    result = RunnerService.run_code(solution, test_code)
    assert result.status == "FAILED"
    assert result.passed is False
    assert "FAILED test_solution.py::test_add" in result.output


def test_runner_security_violation_rejection() -> None:
    """Verify malicious code is rejected before execution."""
    malicious_solution = """
import os

class Exploit:
    def run(self):
        return os.getcwd()
"""
    test_code = "def test_noop(): pass"
    result = RunnerService.run_code(malicious_solution, test_code)
    assert result.status == "SECURITY_VIOLATION"
    assert result.passed is False
    assert "Forbidden module import: 'os'" in result.output


def test_runner_timeout_enforcement() -> None:
    """Verify infinite loop execution is terminated strictly by timeout."""
    infinite_loop_solution = """
class LoopSolver:
    def solve(self):
        while True:
            pass
"""
    test_code = """
from solution import LoopSolver

def test_loop():
    solver = LoopSolver()
    solver.solve()
"""
    result = RunnerService.run_code(infinite_loop_solution, test_code, timeout=1.0)
    assert result.status == "TIMEOUT"
    assert result.passed is False
    assert "Execution timed out" in result.output
