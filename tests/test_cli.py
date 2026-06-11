import json
from pathlib import Path

from mcp_audit.cli import main


FIXTURES = Path(__file__).parent / "fixtures"


def test_cli_scan_outputs_json_report(capsys):
    exit_code = main(["scan", "--config", str(FIXTURES / "high-risk-mcp.json"), "--format", "json"])

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert exit_code == 0
    assert data["summary"]["findings_total"] >= 5


def test_cli_scan_discovers_default_mcp_json(tmp_path, monkeypatch, capsys):
    config = tmp_path / "mcp.json"
    config.write_text((FIXTURES / "high-risk-mcp.json").read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    exit_code = main(["scan", "--format", "json"])

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert exit_code == 0
    assert data["files"][0]["path"] == "mcp.json"
    assert data["summary"]["findings_total"] >= 5


def test_cli_scan_without_config_reports_when_no_supported_config_exists(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    exit_code = main(["scan", "--format", "json"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "No supported MCP or agent config files found" in captured.err


def test_cli_scan_returns_parse_error_exit_code(capsys):
    exit_code = main(["scan", "--config", str(FIXTURES / "invalid-json.json"), "--format", "json"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "invalid-json.json" in captured.err


def test_cli_explain_outputs_rule_rationale(capsys):
    exit_code = main(["explain", "XONE001"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "XONE001" in captured.out
    assert "Remediation" in captured.out


def test_cli_fail_on_high_returns_one_when_high_findings_exist():
    exit_code = main(
        [
            "scan",
            "--config",
            str(FIXTURES / "high-risk-mcp.json"),
            "--format",
            "json",
            "--fail-on",
            "high",
        ]
    )

    assert exit_code == 1
