"""Tests for Web-OOP Header Ergonomics (OOP_20261105-211500_HDRERG).

Validates:
- AC-1: Theme settings button (#theme-settings-btn) relocated to Brand/Profile row next to student selector.
- AC-2: Bottom curtain handle (#header-collapse-handle) with indicator icon (#header-collapse-handle-icon).
- AC-3: Text collapse toggle button (#header-collapse-toggle) preserved and synchronized.
- AC-4: Exam subtabs concise labels and separated actions cluster.
- AC-5: JavaScript synchronization for header collapse state.
- AC-6: CSS styles for .header-collapse-handle-btn and hover glow.
- AC-7: Full test suite compatibility and zero regressions.
-"""

from pathlib import Path
from fastapi.testclient import TestClient

from app.main import app

CLIENT = TestClient(app)
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _read_asset(rel_path: str) -> str:
    return (PROJECT_ROOT / rel_path).read_text(encoding="utf-8")


def test_theme_btn_in_upper_brand_row():
    """AC-1: #theme-settings-btn is located in upper row next to #student-selector, not in Row 2."""
    header_html = _read_asset("app/templates/components/header.html")

    assert 'id="theme-settings-btn"' in header_html
    assert 'onclick="openThemeSettings()"' in header_html

    # Ensure theme button comes before week pills row (header-collapsible-body)
    student_sel_pos = header_html.find('id="student-selector"')
    theme_btn_pos = header_html.find('id="theme-settings-btn"')
    week_row_pos = header_html.find("Row 1: Week Selector Pills")
    row2_nav_pos = header_html.find("Row 2: Section Sub-Tabs")

    assert student_sel_pos != -1, "#student-selector must exist"
    assert theme_btn_pos != -1, "#theme-settings-btn must exist"
    assert week_row_pos != -1, "Week selector pills row must exist"

    # Theme button must be placed in profile cluster, before week row and before row 2
    assert student_sel_pos < theme_btn_pos < week_row_pos < row2_nav_pos

    # Verify theme button is present on all main endpoints
    for path in ("/week1", "/week2", "/week3", "/exam"):
        res = CLIENT.get(path)
        assert res.status_code == 200
        assert 'id="theme-settings-btn"' in res.text


def test_collapse_handle_exists():
    """AC-2: Bottom center handle (#header-collapse-handle) exists on header with icon (#header-collapse-handle-icon)."""
    header_html = _read_asset("app/templates/components/header.html")

    assert 'id="header-collapse-handle"' in header_html
    assert 'id="header-collapse-handle-icon"' in header_html
    assert "header-collapse-handle-btn" in header_html
    assert 'onclick="toggleHeaderCollapse()"' in header_html

    # Verify present on HTML response of all pages
    for path in ("/week1", "/week2", "/week3", "/exam"):
        res = CLIENT.get(path)
        assert res.status_code == 200
        assert 'id="header-collapse-handle"' in res.text
        assert 'id="header-collapse-handle-icon"' in res.text


def test_text_toggle_and_actions_cluster():
    """AC-3: Text collapse toggle button (#header-collapse-toggle) and UML button are preserved in fixed cluster."""
    header_html = _read_asset("app/templates/components/header.html")

    assert 'id="header-collapse-toggle"' in header_html
    assert 'id="header-collapse-label"' in header_html
    assert "openUmlDiagramSection()" in header_html

    for path in ("/week1", "/week2", "/week3", "/exam"):
        res = CLIENT.get(path)
        assert res.status_code == 200
        assert 'id="header-collapse-toggle"' in res.text
        assert 'id="header-collapse-label"' in res.text


def test_exam_subtabs_structure_and_no_overflow():
    """AC-4: Exam subtabs are concise and separated from fixed action buttons cluster."""
    header_html = _read_asset("app/templates/components/header.html")

    # Verify concise exam tab names
    assert "Инструкция" in header_html
    assert "Часть 1 · Тестирование (20 б.)" in header_html
    assert "Часть 2 · Практика (20 б.)" in header_html
    assert "Итоговая Ведомость (100 б.)" in header_html

    # Verify separated containers in Row 2 nav
    assert "flex-1 min-w-0 overflow-x-auto" in header_html or "overflow-x-auto min-w-0 flex-1" in header_html
    assert "shrink-0" in header_html


def test_css_collapse_handle_styles():
    """AC-6: style.css defines .header-collapse-handle-btn with positioning, hover, and clean mode rules."""
    css = _read_asset("app/static/css/style.css")

    assert ".header-collapse-handle-btn" in css
    assert "position: absolute;" in css
    assert "transform: translateX(-50%);" in css
    assert ".header-collapse-handle-btn:hover" in css
    assert "#main-site-header.header-collapsed .header-collapse-handle-btn" in css
    assert '[data-glow="clean"] .header-collapse-handle-btn:hover' in css


def test_js_collapse_state_synchronization():
    """AC-5: app.js updates both label and handle icon when toggling header collapse state."""
    js = _read_asset("app/static/js/app.js")

    assert "header-collapse-handle-icon" in js
    assert "header-collapse-handle" in js
    assert "header-collapse-label" in js
    assert "applyHeaderCollapseState(isCollapsed)" in js
    assert "toggleHeaderCollapse()" in js
    assert "weboop_header_collapsed" in js
