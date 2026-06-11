from pathlib import Path

from mcp_audit.parsers.json_parser import parse_json_config
from mcp_audit.rules.registry import get_rules


FIXTURES = Path(__file__).parent / "fixtures"


def _findings_for(name: str):
    document = parse_json_config(FIXTURES / name)
    findings = []
    for rule in get_rules():
        findings.extend(rule.evaluate(document))
    return findings


def test_high_risk_config_emits_expected_rule_ids():
    findings = _findings_for("high-risk-mcp.json")
    rule_ids = {finding.rule_id for finding in findings}

    assert {"XONE001", "XONE002", "XONE003", "XONE004", "XONE005"} <= rule_ids


def test_real_world_config_emits_environment_and_container_rule_ids():
    findings = _findings_for("high-risk-real-world.json")
    rule_ids = {finding.rule_id for finding in findings}

    assert {"XONE006", "XONE007"} <= rule_ids


def test_safe_config_does_not_emit_high_severity_findings():
    findings = _findings_for("safe-mcp.json")

    assert [finding for finding in findings if finding.severity == "high"] == []


def test_rule_findings_include_reviewable_evidence_and_remediation():
    findings = _findings_for("high-risk-mcp.json")

    for finding in findings:
        assert finding.rule_id.startswith("XONE")
        assert finding.file_path.endswith("high-risk-mcp.json")
        assert finding.config_path.startswith("$")
        assert finding.evidence
        assert finding.redacted_evidence
        assert finding.remediation
