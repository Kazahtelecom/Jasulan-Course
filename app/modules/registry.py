"""Central registry for Web-OOP educational week modules."""

from __future__ import annotations

from typing import Iterable

from app.content.week_1 import (
    PRACTICE_TASKS as W1_PRACTICE,
    QUIZ_QUESTIONS as W1_QUIZ,
    THEORY_SECTIONS as W1_THEORY,
    WALKTHROUGH_EXAMPLE as W1_WALKTHROUGH,
    WEEK1_OVERVIEW,
    evaluate_quiz as w1_evaluate_quiz,
)
from app.content.week_2 import (
    PRACTICE_TASKS as W2_PRACTICE,
    QUIZ_QUESTIONS as W2_QUIZ,
    THEORY_SECTIONS as W2_THEORY,
    WALKTHROUGH_EXAMPLE as W2_WALKTHROUGH,
    WEEK2_OVERVIEW,
    evaluate_quiz as w2_evaluate_quiz,
)
from app.modules.base import WeekModule


class WeekRegistry:
    """Registry managing available curriculum week modules."""

    def __init__(self) -> None:
        self._modules: dict[int, WeekModule] = {}

    def register(self, module: WeekModule) -> None:
        """Register a curriculum week module."""
        self._modules[module.week_number] = module

    def get(self, week_number: int) -> WeekModule | None:
        """Get a module by week number."""
        return self._modules.get(week_number)

    def get_all(self) -> list[WeekModule]:
        """Return all registered modules sorted by week number."""
        return [self._modules[k] for k in sorted(self._modules.keys())]

    def __contains__(self, week_number: int) -> bool:
        return week_number in self._modules


# Global registry instance with default curriculum weeks
week_registry = WeekRegistry()

# Register Week 1: Encapsulation & Basics
week_registry.register(
    WeekModule(
        week_number=1,
        title="Основы ООП и Инкапсуляция",
        overview=WEEK1_OVERVIEW,
        theory_sections=W1_THEORY,
        walkthrough=W1_WALKTHROUGH,
        practice_tasks=W1_PRACTICE,
        quiz_questions=W1_QUIZ,
        evaluate_quiz_fn=w1_evaluate_quiz,
    )
)

# Register Week 2: SOLID Principles & Dependency Injection
week_registry.register(
    WeekModule(
        week_number=2,
        title="Принципы SOLID и Dependency Injection",
        overview=WEEK2_OVERVIEW,
        theory_sections=W2_THEORY,
        walkthrough=W2_WALKTHROUGH,
        practice_tasks=W2_PRACTICE,
        quiz_questions=W2_QUIZ,
        evaluate_quiz_fn=w2_evaluate_quiz,
    )
)
