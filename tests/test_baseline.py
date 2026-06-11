import json
from pathlib import Path

from mcp_audit.cli import main


FIXTURES = Path(__file__).parent / "fixtures"


def test_cli_baseline_writes_finding_fingerprints(tmp_path):
    output = tmp_path / "mcp-audit-baseline.json"

    exit_code = main(["baseline", "--config", str(FIXTURES / "high-risk-mcp.json"), "--output", str(output)])

    data = json.loads(output.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert data["schema_version"] == "0.1"
    assert data["tool"] == "mcp-audit"
    assert data["accepted_findings"]
    assert data["accepted_findings"][0]["fingerprint"]
    assert data["accepted_findings"][0]["rule_id"].startswith("XONE")


def test_cli_scan_with_baseline_suppresses_accepted_findings(tmp_path, capsys):
    baseline = tmp_path / "mcp-audit-baseline.json"
    assert main(["baseline", "--config", str(FIXTURES / "high-risk-mcp.json"), "--output", str(baseline)]) == 0

    exit_code = main(
        [
            "scan",
            "--config",
            str(FIXTURES / "high-risk-mcp.json"),
            "--baseline",
            str(baseline),
            "--format",
            "json",
            "--fail-on",
            "high",
        ]
    )

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert exit_code == 0
    assert data["summary"]["findings_total"] == 0
    assert data["summary"]["suppressed_findings_total"] >= 5


def test_cli_scan_with_baseline_reports_suppressed_count_in_markdown(tmp_path, capsys):
    baseline = tmp_path / "mcp-audit-baseline.json"
    assert main(["baseline", "--config", str(FIXTURES / "high-risk-mcp.json"), "--output", str(baseline)]) == 0

    exit_code = main(
        [
            "scan",
            "--config",
            str(FIXTURES / "high-risk-mcp.json"),
            "--baseline",
            str(baseline),
            "--format",
            "markdown",
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Suppressed findings:" in captured.out


def test_cli_scan_with_baseline_reports_suppressed_count_in_sarif(tmp_path, capsys):
    baseline = tmp_path / "mcp-audit-baseline.json"
    assert main(["baseline", "--config", str(FIXTURES / "high-risk-mcp.json"), "--output", str(baseline)]) == 0

    exit_code = main(
        [
            "scan",
            "--config",
            str(FIXTURES / "high-risk-mcp.json"),
            "--baseline",
            str(baseline),
            "--format",
            "sarif",
        ]
    )

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert exit_code == 0
    assert data["runs"][0]["properties"]["suppressedFindingsTotal"] >= 5


def test_cli_baseline_prune_removes_stale_fingerprints(tmp_path):
    baseline = tmp_path / "mcp-audit-baseline.json"
    pruned = tmp_path / "mcp-audit-baseline-pruned.json"
    assert main(["baseline", "--config", str(FIXTURES / "high-risk-mcp.json"), "--output", str(baseline)]) == 0
    data = json.loads(baseline.read_text(encoding="utf-8"))
    data["accepted_findings"].append(
        {
            "fingerprint": "stale-fingerprint",
            "rule_id": "XONE999",
            "severity": "low",
            "file_path": "missing.json",
            "config_path": "$.missing",
            "title": "Stale accepted finding",
        }
    )
    baseline.write_text(json.dumps(data), encoding="utf-8")

    exit_code = main(
        [
            "baseline",
            "--config",
            str(FIXTURES / "high-risk-mcp.json"),
            "--baseline",
            str(baseline),
            "--prune",
            "--output",
            str(pruned),
        ]
    )

    pruned_data = json.loads(pruned.read_text(encoding="utf-8"))
    fingerprints = {item["fingerprint"] for item in pruned_data["accepted_findings"]}
    assert exit_code == 0
    assert "stale-fingerprint" not in fingerprints
    assert fingerprints
