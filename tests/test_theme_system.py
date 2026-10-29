"""
Test Suite for Web-OOP Phase A: Core Design System, SVG Logo, and Settings Panel
Validates AC-1 through AC-7:
- AC-1: CSS custom properties for 4 neon themes (cyber-gold, electric-cyan, matrix-emerald, synthwave-purple)
- AC-2: Clean vs Cyberpunk glow modes in CSS
- AC-3: Scalable isometric SVG cube logo in header
- AC-4: Settings trigger button and modal with palette swatches & glow mode switch
- AC-5: Zero-FOUC inline initialization script in <head>
- AC-6: Client-side JS theme controller in app.js
- AC-7: Full HTTP endpoint integration & regression test pass
"""

from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLIENT = TestClient(app)


def test_css_theme_variables():
    """AC-1: style.css defines tokens for all 4 color themes."""
    css_path = PROJECT_ROOT / "app" / "static" / "css" / "style.css"
    assert css_path.exists(), "style.css must exist"
    content = css_path.read_text(encoding="utf-8")

    # Verify theme selectors
    assert '[data-theme="cyber-gold"]' in content
    assert '[data-theme="electric-cyan"]' in content
    assert '[data-theme="matrix-emerald"]' in content
    assert '[data-theme="synthwave-purple"]' in content

    # Verify required CSS custom properties
    for token in ["--theme-primary", "--theme-accent", "--theme-glow", "--theme-border", "--theme-bg-gradient"]:
        assert token in content, f"Token {token} missing from style.css"

    # Verify key palette hex values
    assert "#f59e0b" in content  # Cyber Gold
    assert "#00f0ff" in content  # Electric Cyan
    assert "#10b981" in content  # Matrix Emerald
    assert "#d946ef" in content  # Synthwave Purple


def test_css_glow_modes():
    """AC-2: style.css defines rules for both clean and cyberpunk glow modes."""
    css_path = PROJECT_ROOT / "app" / "static" / "css" / "style.css"
    content = css_path.read_text(encoding="utf-8")

    assert '[data-glow="cyberpunk"]' in content
    assert '[data-glow="clean"]' in content

    # Verify clean mode resets box-shadow and removes background gradient
    assert "background-image: none !important" in content
    assert "box-shadow: none !important" in content or "box-shadow: 0 4px 16px" in content


def test_svg_logo_present():
    """AC-3: header.html contains responsive isometric SVG cube with brackets { }."""
    header_path = PROJECT_ROOT / "app" / "templates" / "components" / "header.html"
    assert header_path.exists(), "header.html must exist"
    content = header_path.read_text(encoding="utf-8")

    assert '<svg id="header-logo-cube"' in content
    assert 'viewBox="0 0 64 64"' in content
    assert "{ }" in content
    assert "var(--theme-accent)" in content or "var(--theme-primary)" in content

    # Verify isometric face paths exist
    assert "d=\"M32 6 L54 18 L32 30 L10 18 Z\"" in content  # Top face
    assert "d=\"M10 18 L32 30 L32 56 L10 44 Z\"" in content  # Left face
    assert "d=\"M32 30 L54 18 L54 44 L32 56 Z\"" in content  # Right face


def test_theme_settings_modal_markup():
    """AC-4: header.html contains settings button and modal with palette swatches."""
    header_path = PROJECT_ROOT / "app" / "templates" / "components" / "header.html"
    content = header_path.read_text(encoding="utf-8")

    # Trigger button and modal container
    assert 'id="theme-settings-btn"' in content
    assert 'id="theme-settings-modal"' in content
    assert 'id="close-theme-settings-btn"' in content

    # 4 Theme choices
    assert 'switchTheme(\'cyber-gold\')' in content
    assert 'switchTheme(\'electric-cyan\')' in content
    assert 'switchTheme(\'matrix-emerald\')' in content
    assert 'switchTheme(\'synthwave-purple\')' in content

    # Glow mode toggles
    assert 'id="glow-btn-clean"' in content
    assert 'id="glow-btn-cyberpunk"' in content
    assert "setGlowMode('clean')" in content
    assert "setGlowMode('cyberpunk')" in content


def test_zero_fouc_script_present():
    """AC-5: index.html and exam.html contain synchronous zero-FOUC script in <head>."""
    for filename in ["index.html", "exam.html"]:
        file_path = PROJECT_ROOT / "app" / "templates" / filename
        assert file_path.exists(), f"{filename} must exist"
        content = file_path.read_text(encoding="utf-8")

        head_idx = content.find("</head>")
        assert head_idx != -1, f"{filename} must contain </head>"

        head_content = content[:head_idx]
        assert "weboop_theme" in head_content, f"weboop_theme missing from {filename} <head>"
        assert "weboop_glow" in head_content, f"weboop_glow missing from {filename} <head>"
        assert "data-theme" in head_content, f"data-theme attribute missing from {filename} <head>"
        assert "data-glow" in head_content, f"data-glow attribute missing from {filename} <head>"


def test_theme_js_functions():
    """AC-6: app.js contains theme management and persistence functions."""
    js_path = PROJECT_ROOT / "app" / "static" / "js" / "app.js"
    assert js_path.exists(), "app.js must exist"
    content = js_path.read_text(encoding="utf-8")

    # Required functions
    assert "function initThemeSystem" in content
    assert "function switchTheme" in content
    assert "function setGlowMode" in content
    assert "function openThemeSettings" in content
    assert "function closeThemeSettings" in content

    # Storage keys
    assert "weboop_theme" in content
    assert "weboop_glow" in content


def test_http_endpoints_render_theme_elements():
    """AC-7: All primary endpoints render SVG logo, settings modal, and zero-FOUC script."""
    endpoints = ["/week1", "/week2", "/week3", "/exam"]

    for endpoint in endpoints:
        resp = CLIENT.get(endpoint)
        assert resp.status_code == 200, f"Endpoint {endpoint} failed with {resp.status_code}"
        html = resp.text

        # Verify logo
        assert 'id="header-logo-cube"' in html, f"SVG logo missing on {endpoint}"
        # Verify settings button and modal
        assert 'id="theme-settings-btn"' in html, f"Theme settings btn missing on {endpoint}"
        assert 'id="theme-settings-modal"' in html, f"Theme modal missing on {endpoint}"
        # Verify zero-FOUC script
        assert 'weboop_theme' in html, f"Zero-FOUC script missing on {endpoint}"
        assert 'weboop_glow' in html, f"Zero-FOUC script missing on {endpoint}"
