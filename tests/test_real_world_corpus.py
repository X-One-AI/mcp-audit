from pathlib import Path

from mcp_audit.app import scan_config


CORPUS = Path(__file__).parent / "fixtures" / "real-world-corpus"


def _rule_ids(name: str) -> set[str]:
    report = scan_config(CORPUS / name)
    return {finding.rule_id for finding in report.findings}


def test_real_world_corpus_manifest_records_public_sources():
    manifest = (CORPUS / "README.md").read_text(encoding="utf-8")

    for name in [
        "claude-llamacloud-sanitized.json",
        "cursor-chrome-devtools-sanitized.json",
        "claude-local-node-sanitized.json",
        "yaml-nested-agent-filesystem.yaml",
        "zed-context-server-sanitized.json",
    ]:
        assert name in manifest
    assert "https://github.com/" in manifest
    assert "sanitized" in manifest


def test_real_world_corpus_files_scan_without_parse_errors():
    for path in CORPUS.iterdir():
        if path.suffix not in {".json", ".yaml", ".yml", ".toml"}:
            continue
        report = scan_config(path)
        assert report.files[0].status == "scanned"
        assert report.errors == []


def test_at_latest_and_unpinned_scoped_packages_are_flagged():
    assert "XONE003" in _rule_ids("claude-llamacloud-sanitized.json")
    assert "XONE003" in _rule_ids("cursor-chrome-devtools-sanitized.json")


def test_placeholder_api_keys_are_not_reported_as_literal_secrets():
    assert "XONE001" not in _rule_ids("claude-llamacloud-sanitized.json")


def test_nested_agent_mcp_servers_are_scanned_for_unpinned_packages():
    assert "XONE003" in _rule_ids("yaml-nested-agent-filesystem.yaml")


def test_zed_context_servers_are_scanned_for_unpinned_packages():
    assert "XONE003" in _rule_ids("zed-context-server-sanitized.json")


def test_local_node_entrypoint_shape_does_not_trigger_remote_package_rule():
    assert "XONE003" not in _rule_ids("claude-local-node-sanitized.json")
