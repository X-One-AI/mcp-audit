from datetime import date
from pathlib import Path

from mcp_audit.app import scan_config
from mcp_audit.baseline import render_baseline
from mcp_audit.team_policy import (
    check_team_policy,
    filter_policy_exceptions,
    load_policy_exceptions,
    load_team_policy,
    render_baseline_review,
)


def test_team_policy_example_loads_expected_defaults():
    policy = load_team_policy(Path("examples/team-policy.toml"))

    assert policy.schema_version == 1
    assert policy.mode == "advisory"
    assert policy.required_profile == "team"
    assert policy.allowed_profiles == ("balanced", "team")
    assert policy.allow_global_config_scan is False
    assert policy.require_baseline_review is True
    assert policy.baseline_review_file == ".mcp-audit-baseline.review.toml"
    assert policy.max_allowed_severity == "medium"
    assert "XONE001" in policy.required_rules


def test_team_policy_invalid_values_fall_back_to_safe_defaults(tmp_path):
    path = tmp_path / "policy.toml"
    path.write_text(
        """
[policy]
schema_version = 1
mode = "unsafe"
required_profile = "unknown"
allowed_profiles = ["unknown"]
allow_global_config_scan = true
require_baseline_review = false
max_allowed_severity = "critical"
""",
        encoding="utf-8",
    )

    policy = load_team_policy(path)

    assert policy.mode == "advisory"
    assert policy.required_profile == "balanced"
    assert policy.allowed_profiles == ("balanced", "team")
    assert policy.allow_global_config_scan is True
    assert policy.require_baseline_review is False
    assert policy.max_allowed_severity == "high"


def test_policy_check_blocks_disallowed_profile():
    policy = load_team_policy(Path("examples/team-policy.toml"))

    violations = check_team_policy(policy, profile="starter")

    codes = {violation.code for violation in violations}
    assert "XONEP001" in codes
    assert "XONEP002" in codes


def test_policy_check_blocks_missing_required_rules(tmp_path):
    policy_path = tmp_path / "policy.toml"
    policy_path.write_text(
        """
[policy]
schema_version = 1
mode = "enforced"
required_profile = "starter"
allowed_profiles = ["starter"]
required_rules = ["XONE005", "XONE008", "XONE010"]
require_baseline_review = false
max_allowed_severity = "never"
""",
        encoding="utf-8",
    )
    policy = load_team_policy(policy_path)

    violations = check_team_policy(policy, profile="starter")

    assert any(violation.code == "XONEP003" for violation in violations)


def test_policy_check_requires_baseline_review_hash(tmp_path):
    baseline = tmp_path / ".mcp-audit-baseline.json"
    review = tmp_path / ".mcp-audit-baseline.review.toml"
    baseline.write_text('{"accepted_findings": []}\n', encoding="utf-8")
    review.write_text(
        '[baseline_review]\nsha256 = "wrong"\napproved_by = "security"\nreason = "known risk"\n',
        encoding="utf-8",
    )
    policy = load_team_policy(Path("examples/team-policy.toml"))

    violations = check_team_policy(
        policy,
        profile="team",
        baseline_path=baseline,
        baseline_review_path=review,
    )

    assert any(violation.code == "XONEP009" for violation in violations)


def test_render_baseline_review_satisfies_policy(tmp_path):
    report = scan_config(Path("tests/fixtures/high-risk-mcp.json"))
    baseline = tmp_path / ".mcp-audit-baseline.json"
    review = tmp_path / ".mcp-audit-baseline.review.toml"
    baseline.write_text(render_baseline(report), encoding="utf-8")
    review.write_text(
        render_baseline_review(baseline, approved_by="security", reason="accepted for fixture"),
        encoding="utf-8",
    )
    policy = load_team_policy(Path("examples/team-policy.toml"))

    violations = check_team_policy(
        policy,
        profile="team",
        baseline_path=baseline,
        baseline_review_path=review,
    )

    assert not violations


def test_policy_exceptions_suppress_matching_findings(tmp_path):
    report = scan_config(Path("tests/fixtures/high-risk-mcp.json"))
    finding = report.findings[0]
    exceptions_file = tmp_path / "exceptions.toml"
    exceptions_file.write_text(
        f"""
[[exceptions]]
fingerprint = "{finding.fingerprint}"
rule_id = "{finding.rule_id}"
reason = "fixture risk accepted"
approved_by = "security"
expires_on = "2099-01-01"
""",
        encoding="utf-8",
    )

    exceptions, violations = load_policy_exceptions(exceptions_file, today=date(2026, 6, 12))
    filtered = filter_policy_exceptions(report, exceptions)

    assert not violations
    assert len(filtered.findings) == len(report.findings) - 1
    assert len(filtered.suppressed_findings) == 1


def test_expired_policy_exception_is_a_violation(tmp_path):
    exceptions_file = tmp_path / "exceptions.toml"
    exceptions_file.write_text(
        """
[[exceptions]]
fingerprint = "abc"
rule_id = "XONE001"
reason = "old exception"
approved_by = "security"
expires_on = "2020-01-01"
""",
        encoding="utf-8",
    )

    _, violations = load_policy_exceptions(exceptions_file, today=date(2026, 6, 12))

    assert any(violation.code == "XONEP014" for violation in violations)
