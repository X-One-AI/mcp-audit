from pathlib import Path

from mcp_audit.app import scan_config


CLIENT_FIXTURES = Path(__file__).parent / "fixtures" / "client-formats"


def test_client_format_fixtures_scan_successfully():
    for path in CLIENT_FIXTURES.iterdir():
        report = scan_config(path)
        assert report.files[0].status == "scanned"


def test_client_format_fixtures_cover_expected_rule_boundaries():
    results = {
        path.name: {finding.rule_id for finding in scan_config(path).findings}
        for path in CLIENT_FIXTURES.iterdir()
    }

    assert "XONE003" in results["claude-desktop-config.json"]
    assert "XONE003" in results["windsurf-mcp-config.json"]
    assert "XONE003" not in results["zed-settings.json"]
    assert "XONE003" not in results["gemini-settings.json"]
    assert "XONE002" in results["qwen-settings.json"]
