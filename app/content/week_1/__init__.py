"""Week 1 course content package: Object-Oriented Programming Fundamentals and Invariant Defense."""

from app.content.week_1.lab import LAB_TASK
from app.content.week_1.lecture import LECTURE_DATA
from app.content.week_1.practice import PRACTICE_TASK
from app.content.week_1.quiz import QUIZ_QUESTIONS, check_quiz_answers

__all__ = [
    "LECTURE_DATA",
    "QUIZ_QUESTIONS",
    "check_quiz_answers",
    "PRACTICE_TASK",
    "LAB_TASK",
]
