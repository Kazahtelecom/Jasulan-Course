"""Week 2 educational content package: SOLID Principles & Dependency Injection."""

from app.content.week_2.practice import PRACTICE_TASKS, get_practice_task
from app.content.week_2.quiz import QUIZ_MAX_SCORE, QUIZ_QUESTIONS, evaluate_quiz
from app.content.week_2.theory import THEORY_SECTIONS, WALKTHROUGH_EXAMPLE, WEEK2_OVERVIEW

__all__ = [
    "WEEK2_OVERVIEW",
    "THEORY_SECTIONS",
    "WALKTHROUGH_EXAMPLE",
    "PRACTICE_TASKS",
    "get_practice_task",
    "QUIZ_QUESTIONS",
    "QUIZ_MAX_SCORE",
    "evaluate_quiz",
]
