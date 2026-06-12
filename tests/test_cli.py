import json
import os
import subprocess
import sys
from pathlib import Path

from mcp_audit.cli import main


FIXTURES = Path(__file__).parent / "fixtures"


def test_cli_scan_outputs_json_report(capsys):
    exit_code = main(["scan", "--config", str(FIXTURES / "high-risk-mcp.json"), "--format", "json"])

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert exit_code == 0
    assert data["summary"]["findings_total"] >= 5


def test_cli_scan_outputs_sarif_report(capsys):
    exit_code = main(["scan", "--config", str(FIXTURES / "high-risk-mcp.json"), "--format", "sarif"])

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert exit_code == 0
    assert data["version"] == "2.1.0"
    assert data["runs"][0]["tool"]["driver"]["name"] == "mcp-audit"
    assert data["runs"][0]["results"][0]["ruleId"].startswith("XONE")


def test_cli_version_outputs_package_version(capsys):
    exit_code = main(["--version"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "mcp-audit 0.3.1"


def test_cli_version_outputs_package_version_from_console_args(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["mcp-audit", "--version"])

    exit_code = main()

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "mcp-audit 0.3.1"


def test_package_module_entrypoint_outputs_version():
    env = os.environ | {"PYTHONPATH": "src"}
    result = subprocess.run(
        [sys.executable, "-m", "mcp_audit", "--version"],
        check=True,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
    )

    assert result.stdout.strip() == "mcp-audit 0.3.1"


def test_cli_without_command_returns_usage(capsys):
    exit_code = main([])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "usage: mcp-audit" in captured.err


def test_cli_invalid_arguments_return_two(capsys):
    exit_code = main(["scan", "--format", "xml"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "invalid choice" in captured.err


def test_cli_doctor_reports_runtime_and_discovery(tmp_path, monkeypatch, capsys):
    config = tmp_path / ".mcp.json"
    config.write_text((FIXTURES / "safe-mcp.json").read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    exit_code = main(["doctor"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "mcp-audit 0.3.1" in captured.out
    assert "Python:" in captured.out
    assert ".mcp.json: found" in captured.out
    assert "No network calls are required for scanning." in captured.out


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


def test_cli_rules_lists_registered_rules(capsys):
    exit_code = main(["rules"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "XONE001" in captured.out
    assert "Literal secret appears in configuration" in captured.out
    assert "XONE005" in captured.out


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
