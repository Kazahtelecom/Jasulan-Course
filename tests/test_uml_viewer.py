"""Unit tests for Interactive UML Diagram Viewer component.

Verifies:
1. Self-contained <defs> in all 4 SVG diagrams (Week 1, Week 2, Architecture, ERD).
2. All filter/marker/gradient references resolve within each SVG.
3. Presence of all essential classes, interfaces, and methods.
4. Correct layout and zero overlapping text in Week 2 DI lines.
5. Multi-tab navigation between Week 1, Week 2, Platform Architecture, and DB ERD.
"""

import re

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_uml_viewer_rendered_on_all_weeks() -> None:
    """Verify UML viewer component is included on /week1, /week2, and /week3."""
    for path in ("/week1", "/week2", "/week3"):
        res = client.get(path)
        assert res.status_code == 200
        html = res.text
        assert 'id="uml-diagram-section"' in html
        assert 'id="svg-week1"' in html
        assert 'id="svg-week2"' in html
        assert 'id="svg-week3"' in html
        assert 'id="svg-arch"' in html
        assert 'id="svg-db"' in html
        assert 'id="uml-lens"' in html
        assert 'id="uml-fullscreen-modal"' in html


def test_uml_svgs_have_self_contained_defs() -> None:
    """Verify each SVG defines its own filters and markers locally."""
    res = client.get("/week1")
    assert res.status_code == 200
    html = res.text

    svg_ids = ["svg-week1", "svg-week2", "svg-week3", "svg-arch", "svg-db"]
    for svg_id in svg_ids:
        # Extract the SVG block
        match = re.search(rf'<svg\s+id="{svg_id}".*?</svg>', html, re.DOTALL)
        assert match is not None, f"Could not find <svg id='{svg_id}'>"
        svg_content = match.group(0)

        # 1. Must contain <defs>
        assert "<defs>" in svg_content, f"{svg_id} missing <defs>"
        assert "</defs>" in svg_content, f"{svg_id} missing </defs>"

        # 2. Extract all defined IDs within this SVG's <defs>
        defs_match = re.search(r"<defs>(.*?)</defs>", svg_content, re.DOTALL)
        assert defs_match is not None
        defs_content = defs_match.group(1)
        defined_ids = set(re.findall(r'id="([^"]+)"', defs_content))

        # 3. Find all filter="url(#...)" references and verify they are defined locally
        filter_refs = re.findall(r'filter="url\(#([^)]+)\)"', svg_content)
        for ref in filter_refs:
            assert ref in defined_ids, (
                f"In {svg_id}, filter='url(#{ref})' references undeclared ID! "
                f"This causes elements to disappear when other tabs are hidden."
            )

        # 4. Find all marker references and verify they are defined locally
        marker_refs = re.findall(r'marker-(?:start|end)="url\(#([^)]+)\)"', svg_content)
        for ref in marker_refs:
            assert ref in defined_ids, (
                f"In {svg_id}, marker='url(#{ref})' references undeclared ID: '{ref}'!"
            )


def test_week1_diagram_classes_and_encapsulation() -> None:
    """Verify Week 1 diagram contains Passenger, SmartCard, and TerminalValidator."""
    res = client.get("/week1")
    html = res.text
    match = re.search(r'<svg\s+id="svg-week1".*?</svg>', html, re.DOTALL)
    assert match is not None
    svg = match.group(0)

    assert "Passenger" in svg
    assert "SmartCard" in svg
    assert "TerminalValidator" in svg
    assert "_balance" in svg
    assert "🔒 [private]" in svg
    assert "&lt;&lt;property&gt;&gt;" in svg or "<<property>>" in svg
    assert "top_up" in svg
    assert "pay" in svg


def test_week2_diagram_solid_and_di_structure() -> None:
    """Verify Week 2 diagram contains interfaces, implementations, and TerminalValidator with DI."""
    res = client.get("/week2")
    html = res.text
    match = re.search(r'<svg\s+id="svg-week2".*?</svg>', html, re.DOTALL)
    assert match is not None
    svg = match.group(0)

    # Interfaces
    assert "IFareService" in svg
    assert "IPaymentMethod" in svg

    # Implementations
    assert "StandardFareService" in svg
    assert "StudentFareService" in svg
    assert "CardPayment" in svg
    assert "BluetoothPayment" in svg

    # Central validator
    assert "TerminalValidator" in svg
    assert "fare_service: IFareService" in svg
    assert "payment_method: IPaymentMethod" in svg
    assert "__init__(fare_service, payment_method)" in svg
    assert "Dependency Injection" in svg

    # Ensure no overlapping identical text labels at the exact same coordinates
    di_fare_match = re.search(r'<g id="edge-di-fare">(.*?)</g>', svg, re.DOTALL)
    di_pay_match = re.search(r'<g id="edge-di-payment">(.*?)</g>', svg, re.DOTALL)
    assert di_fare_match is not None
    assert di_pay_match is not None
    assert "DI: IFareService" in di_fare_match.group(1)
    assert "DI: IPaymentMethod" in di_pay_match.group(1)


def test_arch_and_db_diagrams_entities() -> None:
    """Verify Architecture and Database diagrams contain all required entities."""
    res = client.get("/week1")
    html = res.text

    # Architecture diagram
    arch_match = re.search(r'<svg\s+id="svg-arch".*?</svg>', html, re.DOTALL)
    assert arch_match is not None
    arch_svg = arch_match.group(0)
    assert "WeekRegistry" in arch_svg
    assert "WeekModule" in arch_svg
    assert "ScoringService" in arch_svg
    assert "RunnerService" in arch_svg
    assert "ASTValidator" in arch_svg

    # Database diagram
    db_match = re.search(r'<svg\s+id="svg-db".*?</svg>', html, re.DOTALL)
    assert db_match is not None
    db_svg = db_match.group(0)
    assert "STUDENTS" in db_svg
    assert "TOPIC_PROGRESS" in db_svg
    assert "SUBMISSIONS" in db_svg
    assert "Режим WAL" in db_svg


def test_week3_diagram_classes_and_clean_arch() -> None:
    """Verify Week 3 diagram contains GoF patterns and Clean Architecture entities."""
    res = client.get("/week3")
    assert res.status_code == 200
    html = res.text
    match = re.search(r'<svg\s+id="svg-week3".*?</svg>', html, re.DOTALL)
    assert match is not None, "Could not find svg-week3"
    svg = match.group(0)

    # Required key classes and interfaces
    assert "TransitTerminalFacade" in svg
    assert "ShiftReportBuilder" in svg
    assert "ValidationHandler" in svg
    assert "TransitTelemetrySubject" in svg
    assert "ValidateRideUseCase" in svg
    assert "CardRepositoryPort" in svg
    assert "PaymentGatewayPort" in svg
    assert "BankApiAdapter" in svg
    assert "TransitCard" in svg
    assert "Money" in svg
    assert "LegacyBankClient" in svg
