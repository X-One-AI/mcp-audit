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


def test_cli_explicit_fail_on_overrides_project_config(tmp_path, monkeypatch):
    config = tmp_path / "mcp.json"
    config.write_text((FIXTURES / "high-risk-mcp.json").read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / ".mcp-audit.toml").write_text('[scan]\nfail_on = "never"\n', encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    exit_code = main(["scan", "--fail-on", "high"])

    assert exit_code == 1
