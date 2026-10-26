"""Week 3 educational content package: GoF Design Patterns & Clean Architecture."""

from app.content.week_3.practice import PRACTICE_TASKS, get_practice_task
from app.content.week_3.quiz import QUIZ_MAX_SCORE, QUIZ_QUESTIONS, evaluate_quiz
from app.content.week_3.theory import THEORY_SECTIONS, WALKTHROUGH_EXAMPLE, WEEK3_OVERVIEW

__all__ = [
    "WEEK3_OVERVIEW",
    "THEORY_SECTIONS",
    "WALKTHROUGH_EXAMPLE",
    "PRACTICE_TASKS",
    "get_practice_task",
    "QUIZ_QUESTIONS",
    "QUIZ_MAX_SCORE",
    "evaluate_quiz",
]
