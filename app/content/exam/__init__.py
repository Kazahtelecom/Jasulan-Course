"""Exam content package: Overview, Quiz, and Practice tasks."""

from __future__ import annotations

from typing import Any

from app.content.exam.practice import PRACTICE_TASKS as EXAM_PRACTICE_TASKS
from app.content.exam.quiz import (
    EXAM_QUIZ_MAX_SCORE,
    EXAM_QUIZ_QUESTIONS,
    POINTS_PER_QUESTION,
    evaluate_exam_quiz,
)

EXAM_OVERVIEW: dict[str, Any] = {
    "title": "🏆 Итоговый Экзамен по курсу ООП",
    "subtitle": "Комплексная аттестация по материалам Недель 1–3 на сквозном домене транспортной системы Avtobys",
    "badge": "Финальная аттестация (40 баллов)",
    "description": (
        "Итоговый экзамен объединяет все темы курса: базовое ООП, инварианты и инкапсуляцию (Неделя 1), "
        "принципы SOLID и Dependency Injection (Неделя 2), а также паттерны проектирования GoF и "
        "Чистую Архитектуру (Неделя 3). Экзамен состоит из 20 концептуальных вопросов (20 баллов) "
        "и 2 боевых задач в тренажёре IDE (20 баллов). В сумме с 60 баллами за семестр формируется 100-балльная оценка."
    ),
    "rules": [
        "1. Экзамен состоит из двух частей: Теоретический квиз (20 вопросов по 1.0 б. = 20.0 б.) и Практика (2 задачи по 10.0 б. = 20.0 б.).",
        "2. Общий максимум за экзамен — 40.0 баллов. Порог сдачи экзамена — 20.0 баллов из 40.0.",
        "3. Общая итоговая оценка курса рассчитывается как сумма трёх недель (по 20.0 б. каждая = 60.0 б.) и экзамена (40.0 б.) до 100.0 баллов. Порог зачёта курса — 50.0 баллов.",
        "4. Режим честности: в практических задачах экзамена кнопка «Показать готовое решение» скрыта.",
        "5. Защита High-Water Mark: при повторной отправке решений сохраняется наивысший достигнутый результат.",
    ],
    "structure": [
        {
            "name": "Часть 1: Теоретическое тестирование",
            "score": "20.0 баллов (20 вопросов по 1.0 б.)",
            "scope": "Недели 1–3 (Лекции 1–9: инварианты, SOLID, паттерны GoF, Clean Architecture)",
        },
        {
            "name": "Часть 2: Практические задачи",
            "score": "20.0 баллов (2 задачи по 10.0 б.)",
            "scope": "Задача 1 (Domain Model & SOLID) + Задача 2 (GoF Builder, Adapter, Facade & Clean Arch)",
        },
    ],
    "max_score": 40.0,
    "pass_threshold": 20.0,
    "course_total_max": 100.0,
    "course_pass_threshold": 50.0,
}

__all__ = [
    "EXAM_OVERVIEW",
    "EXAM_QUIZ_QUESTIONS",
    "EXAM_QUIZ_MAX_SCORE",
    "POINTS_PER_QUESTION",
    "evaluate_exam_quiz",
    "EXAM_PRACTICE_TASKS",
]
