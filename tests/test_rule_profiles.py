import json
from pathlib import Path

from mcp_audit.cli import main
from mcp_audit.rules.registry import get_rule_infos, get_rules


FIXTURES = Path(__file__).parent / "fixtures"


def test_starter_profile_excludes_noisy_medium_network_rule():
    rule_ids = {rule.id for rule in get_rules(profile="starter")}

    assert "XONE005" not in rule_ids
    assert {"XONE001", "XONE002", "XONE003", "XONE004", "XONE006", "XONE007"} <= rule_ids


def test_balanced_profile_keeps_all_current_rules():
    rule_ids = {rule.id for rule in get_rules(profile="balanced")}
    info_ids = {info.id for info in get_rule_infos(profile="balanced")}

    assert rule_ids == info_ids
    assert "XONE005" in rule_ids


def test_cli_scan_profile_filters_findings(capsys):
    exit_code = main(
        [
            "scan",
            "--config",
            str(FIXTURES / "high-risk-mcp.json"),
            "--format",
            "json",
            "--profile",
            "starter",
        ]
    )

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert exit_code == 0
    assert all(finding["rule_id"] != "XONE005" for finding in data["findings"])


def test_init_can_write_team_profile_config(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    exit_code = main(["init", "--profile", "team"])

    config = (tmp_path / ".mcp-audit.toml").read_text(encoding="utf-8")
    assert exit_code == 0
    assert 'profile = "team"' in config
    assert 'fail_on = "medium"' in config
