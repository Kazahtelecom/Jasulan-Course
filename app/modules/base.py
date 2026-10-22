"""Base contract and data structures for educational week modules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from app.config import settings


@dataclass(frozen=True)
class WeekModule:
    """Represents a self-contained curriculum week in the Web-OOP platform."""

    week_number: int
    title: str
    overview: dict[str, Any]
    theory_sections: list[dict[str, Any]]
    walkthrough: dict[str, Any]
    practice_tasks: list[dict[str, Any]]
    quiz_questions: list[dict[str, Any]]
    evaluate_quiz_fn: Callable[[dict[str, int]], dict[str, Any]]

    def get_practice_task(self, task_id: str) -> dict[str, Any] | None:
        """Find a practice task by its identifier."""
        for task in self.practice_tasks:
            if task.get("id") == task_id:
                return task
        return None

    def evaluate_quiz(self, answers: dict[str, int]) -> dict[str, Any]:
        """Evaluate quiz answers using the week's evaluation function."""
        return self.evaluate_quiz_fn(answers)

    def build_context(
        self,
        student: Any,
        progress: dict[str, Any],
        request: Any = None,
    ) -> dict[str, Any]:
        """Build template rendering context for this week."""
        return {
            "request": request,
            "app_name": settings.app_name,
            "version": settings.app_version,
            "active_week": self.week_number,
            "student": student,
            "progress": progress,
            "overview": self.overview,
            "theory_sections": self.theory_sections,
            "walkthrough": self.walkthrough,
            "practice_tasks": self.practice_tasks,
            "quiz_questions": self.quiz_questions,
        }
