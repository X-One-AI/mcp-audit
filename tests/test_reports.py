import json
from pathlib import Path

from mcp_audit.app import scan_config
from mcp_audit.renderers.json_report import render_json_report
from mcp_audit.renderers.markdown_report import render_markdown_report


FIXTURES = Path(__file__).parent / "fixtures"


def test_json_report_contains_stable_contract_keys():
    report = scan_config(FIXTURES / "high-risk-mcp.json")

    data = json.loads(render_json_report(report))

    assert set(data) == {"schema_version", "tool", "summary", "files", "findings", "errors"}
    assert data["schema_version"] == "0.1"
    assert data["summary"]["findings_total"] >= 5
    finding = data["findings"][0]
    assert {
        "rule_id",
        "title",
        "severity",
        "category",
        "file_path",
        "config_path",
        "evidence",
        "redacted_evidence",
        "remediation",
        "confidence",
    } <= set(finding)


def test_markdown_report_contains_review_sections_and_redacts_secrets():
    report = scan_config(FIXTURES / "high-risk-mcp.json")

    markdown = render_markdown_report(report)

    assert "# mcp-audit Report" in markdown
    assert "## Summary" in markdown
    assert "## Findings" in markdown
    assert "## Limitations" in markdown
    assert "XONE001" in markdown
    assert "Remediation:" in markdown
    assert "ghp_example_literal_token" not in markdown
