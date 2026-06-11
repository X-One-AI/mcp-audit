import json
from pathlib import Path

from mcp_audit.cli import main


FIXTURES = Path(__file__).parent / "fixtures"


def test_cli_scan_outputs_findings_for_yaml_config(capsys):
    exit_code = main(["scan", "--config", str(FIXTURES / "high-risk-agent.yaml"), "--format", "json"])

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert exit_code == 0
    assert data["files"][0]["parser"] == "yaml"
    assert data["summary"]["findings_total"] >= 4


def test_cli_scan_outputs_findings_for_toml_config(capsys):
    exit_code = main(["scan", "--config", str(FIXTURES / "high-risk-agent.toml"), "--format", "json"])

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert exit_code == 0
    assert data["files"][0]["parser"] == "toml"
    assert data["summary"]["findings_total"] >= 4
