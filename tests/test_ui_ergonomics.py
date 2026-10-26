"""Tests for trainer UI ergonomics (header collapse, fullscreen, splitter, line numbers, font size) and quiz balance."""

from collections import Counter
from pathlib import Path

from fastapi.testclient import TestClient

from app.content.week_1 import PRACTICE_TASKS as WEEK1_TASKS
from app.content.week_1 import QUIZ_QUESTIONS as WEEK1_QUIZ
from app.content.week_2 import PRACTICE_TASKS as WEEK2_TASKS
from app.content.week_2 import QUIZ_QUESTIONS as WEEK2_QUIZ
from app.content.week_3 import PRACTICE_TASKS as WEEK3_TASKS
from app.content.week_3 import QUIZ_QUESTIONS as WEEK3_QUIZ


def _read_static_asset(rel_path: str) -> str:
    root = Path(__file__).resolve().parent.parent
    return (root / "app" / "static" / rel_path).read_text(encoding="utf-8")


def test_collapsible_header(client: TestClient) -> None:
    """AC-1: Verify collapsible top header controls in HTML, JS, and CSS for /week1 and /week2."""
    for path in ("/week1", "/week2", "/week3"):
        res = client.get(path)
        assert res.status_code == 200
        html = res.text
        assert 'id="main-site-header"' in html
        assert 'id="header-collapsible-body"' in html
        assert 'id="header-collapse-toggle"' in html
        assert 'id="header-collapse-label"' in html
        assert 'onclick="toggleHeaderCollapse()"' in html

    js = _read_static_asset("js/app.js")
    assert "function toggleHeaderCollapse()" in js
    assert "function applyHeaderCollapseState(" in js
    assert "weboop_header_collapsed" in js
    assert "header-collapsed" in js

    css = _read_static_asset("css/style.css")
    assert "#main-site-header.header-collapsed #header-collapsible-body" in css


def test_practice_fullscreen_and_splitter(client: TestClient) -> None:
    """AC-2: Verify fullscreen Zen mode and resizable split columns for all Week 1 & Week 2 tasks."""
    week_configs = [
        ("/week1", [t["id"] for t in WEEK1_TASKS]),
        ("/week2", [t["id"] for t in WEEK2_TASKS]),
        ("/week3", [t["id"] for t in WEEK3_TASKS]),
    ]

    for path, task_ids in week_configs:
        res = client.get(path)
        assert res.status_code == 200
        html = res.text

        for tid in task_ids:
            assert f'id="split-layout-{tid}"' in html
            assert f'id="task-pane-{tid}"' in html
            assert f'id="split-resizer-{tid}"' in html
            assert f'id="editor-pane-{tid}"' in html
            assert f'id="fullscreen-btn-{tid}"' in html
            assert f'id="fullscreen-btn-label-{tid}"' in html
            assert f"togglePracticeFullscreen('{tid}')" in html
            assert f"setPracticeSplitRatio('{tid}', 25)" in html
            assert f"setPracticeSplitRatio('{tid}', 35)" in html
            assert f"setPracticeSplitRatio('{tid}', 50)" in html

    js = _read_static_asset("js/app.js")
    assert "function togglePracticeFullscreen(taskId)" in js
    assert "function exitAllPracticeFullscreen()" in js
    assert "function setPracticeSplitRatio(taskId, ratioPercent)" in js
    assert "function initPracticeSplitResizers()" in js
    assert "weboop_split_width" in js
    assert "practice-fullscreen-active" in js

    css = _read_static_asset("css/style.css")
    assert ".practice-fullscreen-active" in css
    assert ".practice-split-resizer" in css


def test_editor_line_numbers_and_fontsize(client: TestClient) -> None:
    """AC-3: Verify IDE line numbers gutter, live line count, Tab indent, and A-/A+ font scaling."""
    week_configs = [
        ("/week1", [t["id"] for t in WEEK1_TASKS]),
        ("/week2", [t["id"] for t in WEEK2_TASKS]),
        ("/week3", [t["id"] for t in WEEK3_TASKS]),
    ]

    for path, task_ids in week_configs:
        res = client.get(path)
        assert res.status_code == 200
        html = res.text

        assert 'onclick="changeEditorFontSize(-1)"' in html
        assert 'onclick="changeEditorFontSize(1)"' in html
        assert "code-editor-workspace" in html
        assert "line-numbers-gutter" in html

        for tid in task_ids:
            assert f'id="line-numbers-{tid}"' in html
            assert f'id="editor-{tid}"' in html
            assert f'id="line-count-label-{tid}"' in html

    js = _read_static_asset("js/app.js")
    assert "function updateLineNumbers(taskId)" in js
    assert "function changeEditorFontSize(delta)" in js
    assert "function applyEditorFontSize(sizePx)" in js
    assert "weboop_editor_font_size" in js
    assert "updateLineNumbers(taskId);" in js

    css = _read_static_asset("css/style.css")
    assert ".code-editor-workspace" in css
    assert ".line-numbers-gutter" in css


def test_quiz_balance_and_traps(client: TestClient) -> None:
    """AC-4: Verify option length balance (max/min <= 1.65), index distribution (0..3), and non-longest correct options."""
    for week_label, questions, api_path in (
        ("Week 1", WEEK1_QUIZ, "/api/week1/quiz/check"),
        ("Week 2", WEEK2_QUIZ, "/api/week2/quiz/check"),
        ("Week 3", WEEK3_QUIZ, "/api/week3/quiz/check"),
    ):
        assert len(questions) == 10, f"{week_label} must have 10 questions"

        index_counts = Counter(q["correct_index"] for q in questions)
        for idx in (0, 1, 2, 3):
            count = index_counts.get(idx, 0)
            assert 2 <= count <= 3, (
                f"{week_label}: correct_index {idx} used {count} times (expected 2..3)"
            )

        not_strictly_longest_count = 0
        for q in questions:
            opts = q["options"]
            assert len(opts) == 4, f"{q['id']} must have 4 options"
            lengths = [len(o.strip()) for o in opts]
            min_len = min(lengths)
            max_len = max(lengths)
            assert min_len >= 60, f"{q['id']} has overly short option ({min_len} chars)"

            ratio = max_len / min_len
            assert ratio <= 1.65, (
                f"{week_label} {q['id']} length ratio {ratio:.2f} exceeds 1.65 ({lengths})"
            )

            correct_len = lengths[q["correct_index"]]
            is_strictly_longest = (correct_len == max_len) and (lengths.count(max_len) == 1)
            if not is_strictly_longest:
                not_strictly_longest_count += 1

        assert not_strictly_longest_count >= 5, (
            f"{week_label}: correct option is not strictly longest in only "
            f"{not_strictly_longest_count}/10 questions (expected >= 5)"
        )

        # Verify API evaluation still awards 20.0 for all correct answers
        perfect_payload = {q["id"]: q["correct_index"] for q in questions}
        res = client.post(api_path, json={"answers": perfect_payload})
        assert res.status_code == 200
        data = res.json()
        assert data["correct_count"] == 10
        assert data["score"] == 20.0
        assert data["max_score"] == 20.0
