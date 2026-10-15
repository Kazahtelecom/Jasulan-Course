"""Tests for Week 1 course content integrity and reference solutions."""

import re

from app.content.week_1.lab import LAB_TASK
from app.content.week_1.lecture import LECTURE_DATA
from app.content.week_1.practice import PRACTICE_TASK
from app.content.week_1.quiz import QUIZ_QUESTIONS, check_quiz_answers
from app.services.runner import RunnerService


def test_lecture_content_structure():
    """Verify lecture title, sections narrative, and Mermaid diagrams."""
    assert "title" in LECTURE_DATA
    assert "summary" in LECTURE_DATA
    assert len(LECTURE_DATA["sections"]) == 5

    section_ids = [s["id"] for s in LECTURE_DATA["sections"]]
    assert "chaos_to_structure" in section_ids
    assert "identity_state_behavior" in section_ids
    assert "anemic_vs_rich" in section_ids
    assert "invariants_and_properties" in section_ids
    assert "domain_exceptions" in section_ids

    # Mermaid diagrams presence
    diagrams = LECTURE_DATA.get("mermaid_diagrams", {})
    assert "class_diagram" in diagrams
    assert "sequence_diagram" in diagrams
    assert "TransitCard" in diagrams["class_diagram"]
    assert "SingleTripTicket" in diagrams["class_diagram"]
    assert "Bus" in diagrams["class_diagram"]
    assert "sequenceDiagram" in diagrams["sequence_diagram"]


def test_quiz_questions_bank():
    """Verify quiz questions structure, options, and explanations."""
    assert len(QUIZ_QUESTIONS) == 5

    for q in QUIZ_QUESTIONS:
        assert "id" in q
        assert "question" in q
        assert "options" in q
        assert len(q["options"]) == 4
        assert 0 <= q["correct_option"] < 4
        assert "explanations" in q
        for idx in range(len(q["options"])):
            assert idx in q["explanations"]
            assert len(q["explanations"][idx]) > 0


def test_quiz_answer_evaluation():
    """Verify scoring logic for full, partial, and zero correct answers."""
    # Full correct
    all_correct = {q["id"]: q["correct_option"] for q in QUIZ_QUESTIONS}
    res_full = check_quiz_answers(all_correct)
    assert res_full["score"] == 3.0
    assert res_full["correct_count"] == 5
    assert res_full["max_score"] == 3.0

    # 4 out of 5 correct (4/5 * 3.0 = 2.4)
    partial = dict(all_correct)
    first_qid = QUIZ_QUESTIONS[0]["id"]
    wrong_opt = (QUIZ_QUESTIONS[0]["correct_option"] + 1) % 4
    partial[first_qid] = wrong_opt
    res_partial = check_quiz_answers(partial)
    assert res_partial["score"] == 2.4
    assert res_partial["correct_count"] == 4

    # Empty
    res_empty = check_quiz_answers({})
    assert res_empty["score"] == 0.0
    assert res_empty["correct_count"] == 0


def test_practice_secret_tests_and_reference_solution():
    """Verify practice secret tests count and verify that reference solution passes all 7 tests."""
    secret_tests = PRACTICE_TASK["secret_tests"]
    test_matches = re.findall(r"def (test_\w+)\(", secret_tests)
    assert len(test_matches) == 7
    assert PRACTICE_TASK["test_count"] == 7

    # Run reference solution in isolated RunnerService
    result = RunnerService.run_code(
        code=PRACTICE_TASK["reference_solution"],
        test_code=secret_tests,
    )
    assert result.passed is True
    assert result.status == "PASSED"
    assert "7 passed" in result.output


def test_lab_secret_tests_and_reference_solution():
    """Verify lab secret tests count and verify that reference solution passes all 10 tests."""
    secret_tests = LAB_TASK["secret_tests"]
    test_matches = re.findall(r"def (test_\w+)\(", secret_tests)
    assert len(test_matches) == 10
    assert LAB_TASK["test_count"] == 10

    # Run reference solution in isolated RunnerService
    result = RunnerService.run_code(
        code=LAB_TASK["reference_solution"],
        test_code=secret_tests,
    )
    assert result.passed is True
    assert result.status == "PASSED"
    assert "10 passed" in result.output
