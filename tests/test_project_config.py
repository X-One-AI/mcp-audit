import json
from pathlib import Path

from mcp_audit.cli import main


FIXTURES = Path(__file__).parent / "fixtures"


def test_cli_init_writes_project_config(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    exit_code = main(["init"])

    config = tmp_path / ".mcp-audit.toml"
    assert exit_code == 0
    assert config.exists()
    text = config.read_text(encoding="utf-8")
    assert 'fail_on = "high"' in text
    assert 'baseline = ".mcp-audit-baseline.json"' in text


def test_cli_init_wizard_writes_team_policy(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    exit_code = main(["init", "--wizard", "--profile", "team"])

    captured = capsys.readouterr()
    config = tmp_path / ".mcp-audit.toml"
    policy = tmp_path / ".mcp-audit-policy.toml"
    assert exit_code == 0
    assert config.exists()
    assert policy.exists()
    assert 'profile = "team"' in config.read_text(encoding="utf-8")
    assert 'mode = "enforced"' in policy.read_text(encoding="utf-8")
    assert "policy check" in captured.out


def test_cli_scan_uses_project_config_for_baseline_and_fail_on(tmp_path, monkeypatch, capsys):
    config = tmp_path / "mcp.json"
    config.write_text((FIXTURES / "high-risk-mcp.json").read_text(encoding="utf-8"), encoding="utf-8")
    baseline = tmp_path / ".mcp-audit-baseline.json"
    assert main(["baseline", "--config", str(config), "--output", str(baseline)]) == 0
    (tmp_path / ".mcp-audit.toml").write_text(
        '[scan]\nfail_on = "high"\nbaseline = ".mcp-audit-baseline.json"\n',
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    exit_code = main(["scan", "--format", "json"])

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert exit_code == 0
    assert data["summary"]["findings_total"] == 0


def test_cli_scan_ignores_missing_project_baseline(tmp_path, monkeypatch, capsys):
    config = tmp_path / "mcp.json"
    config.write_text((FIXTURES / "high-risk-mcp.json").read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / ".mcp-audit.toml").write_text(
        '[scan]\nfail_on = "never"\nbaseline = ".mcp-audit-baseline.json"\n',
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    exit_code = main(["scan", "--format", "json"])

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert exit_code == 0
    assert data["summary"]["findings_total"] > 0


def test_cli_scan_reports_missing_explicit_baseline(tmp_path, monkeypatch, capsys):
    config = tmp_path / "mcp.json"
    config.write_text((FIXTURES / "high-risk-mcp.json").read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    exit_code = main(["scan", "--config", str(config), "--baseline", "missing.json"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "Baseline file not found: missing.json" in captured.err


def test_cli_explicit_fail_on_overrides_project_config(tmp_path, monkeypatch):
    config = tmp_path / "mcp.json"
    config.write_text((FIXTURES / "high-risk-mcp.json").read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / ".mcp-audit.toml").write_text('[scan]\nfail_on = "never"\n', encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    exit_code = main(["scan", "--fail-on", "high"])

    assert exit_code == 1


def test_cli_doctor_reports_project_config(tmp_path, monkeypatch, capsys):
    (tmp_path / ".mcp-audit.toml").write_text(
        '[scan]\nfail_on = "medium"\nbaseline = ".mcp-audit-baseline.json"\n',
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    exit_code = main(["doctor"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Project config: found (.mcp-audit.toml)" in captured.out
    assert "Effective fail-on: medium" in captured.out
    assert "Effective baseline: .mcp-audit-baseline.json" in captured.out
