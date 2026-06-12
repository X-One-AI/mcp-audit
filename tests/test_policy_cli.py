import json
from pathlib import Path

from mcp_audit.app import scan_config
from mcp_audit.baseline import render_baseline
from mcp_audit.cli import main
from mcp_audit.team_policy import render_baseline_review


FIXTURES = Path(__file__).parent / "fixtures"


def test_policy_check_enforced_mode_returns_one_for_profile_violation(tmp_path, capsys):
    policy = tmp_path / "policy.toml"
    policy.write_text(
        """
[policy]
schema_version = 1
mode = "enforced"
required_profile = "team"
allowed_profiles = ["team"]
require_baseline_review = false
max_allowed_severity = "never"
""",
        encoding="utf-8",
    )

    exit_code = main(["policy", "check", "--policy", str(policy), "--profile", "starter"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "XONEP001" in captured.err


def test_policy_check_advisory_mode_reports_but_returns_zero(tmp_path, capsys):
    policy = tmp_path / "policy.toml"
    policy.write_text(
        """
[policy]
schema_version = 1
mode = "advisory"
required_profile = "team"
allowed_profiles = ["team"]
require_baseline_review = false
max_allowed_severity = "never"
""",
        encoding="utf-8",
    )

    exit_code = main(["policy", "check", "--policy", str(policy), "--profile", "starter"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "XONEP001" in captured.err


def test_scan_policy_enforced_blocks_unsuppressed_findings(tmp_path, capsys):
    policy = tmp_path / "policy.toml"
    policy.write_text(
        """
[policy]
schema_version = 1
mode = "enforced"
required_profile = "team"
allowed_profiles = ["team"]
require_baseline_review = false
max_allowed_severity = "medium"
""",
        encoding="utf-8",
    )

    exit_code = main(
        [
            "scan",
            "--config",
            str(FIXTURES / "high-risk-mcp.json"),
            "--profile",
            "team",
            "--policy",
            str(policy),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert exit_code == 1
    assert "XONEP006" in captured.err
    assert data["summary"]["findings_total"] > 0


def test_scan_policy_does_not_require_review_for_missing_project_default_baseline(tmp_path, monkeypatch, capsys):
    config = tmp_path / "mcp.json"
    config.write_text((FIXTURES / "high-risk-mcp.json").read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / ".mcp-audit.toml").write_text(
        '[scan]\nprofile = "team"\nfail_on = "never"\nbaseline = ".mcp-audit-baseline.json"\n',
        encoding="utf-8",
    )
    policy = tmp_path / ".mcp-audit-policy.toml"
    policy.write_text(
        """
[policy]
schema_version = 1
mode = "enforced"
required_profile = "team"
allowed_profiles = ["team"]
require_baseline_review = true
max_allowed_severity = "medium"
""",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    exit_code = main(["scan", "--config", str(config), "--policy", str(policy), "--format", "json"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "XONEP006" in captured.err
    assert "XONEP007" not in captured.err


def test_scan_policy_passes_with_reviewed_baseline(tmp_path, capsys):
    config = FIXTURES / "high-risk-mcp.json"
    report = scan_config(config, profile="team")
    baseline = tmp_path / ".mcp-audit-baseline.json"
    review = tmp_path / ".mcp-audit-baseline.review.toml"
    baseline.write_text(render_baseline(report), encoding="utf-8")
    review.write_text(
        render_baseline_review(baseline, approved_by="security", reason="fixture acceptance"),
        encoding="utf-8",
    )
    policy = tmp_path / "policy.toml"
    policy.write_text(
        """
[policy]
schema_version = 1
mode = "enforced"
required_profile = "team"
allowed_profiles = ["team"]
require_baseline_review = true
max_allowed_severity = "medium"
""",
        encoding="utf-8",
    )

    exit_code = main(
        [
            "scan",
            "--config",
            str(config),
            "--profile",
            "team",
            "--baseline",
            str(baseline),
            "--baseline-review",
            str(review),
            "--policy",
            str(policy),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert exit_code == 0
    assert data["summary"]["findings_total"] == 0
    assert data["summary"]["suppressed_findings_total"] > 0
