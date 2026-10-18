"""Week 1 educational content package."""

from app.content.week_1.practice import PRACTICE_TASKS, get_practice_task
from app.content.week_1.quiz import QUIZ_MAX_SCORE, QUIZ_QUESTIONS, evaluate_quiz
from app.content.week_1.theory import THEORY_SECTIONS, WALKTHROUGH_EXAMPLE, WEEK1_OVERVIEW

__all__ = [
    "WEEK1_OVERVIEW",
    "THEORY_SECTIONS",
    "WALKTHROUGH_EXAMPLE",
    "PRACTICE_TASKS",
    "get_practice_task",
    "QUIZ_QUESTIONS",
    "QUIZ_MAX_SCORE",
    "evaluate_quiz",
]
