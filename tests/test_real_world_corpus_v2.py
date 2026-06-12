from pathlib import Path

from mcp_audit.app import scan_config


CORPUS = Path(__file__).parent / "fixtures" / "real-world-corpus-v2"
FIXTURES = {
    "agentdesk-browser-tools-floating-package.json": {
        "source": "AgentDeskAI/browser-tools-mcp",
        "expected": {"XONE003"},
    },
    "cline-official-settings-path.json": {"source": "cline/cline", "expected": set()},
    "confluent-local-node-config.json": {"source": "confluentinc/mcp-confluent", "expected": set()},
    "danlee-mcp-setup-aggregate.json": {"source": "danlee-dev/mcp-setup", "expected": {"XONE003", "XONE004"}},
    "task-master-cursor-roo-npx.json": {"source": "eyaltoledano/claude-task-master", "expected": {"XONE003"}},
    "github-mcp-docker-env.json": {"source": "github/github-mcp-server", "expected": set()},
    "grab-cursor-figma-bunx-latest.json": {
        "source": "grab/cursor-talk-to-figma-mcp",
        "expected": {"XONE003"},
    },
    "hassanaftab-pentest-docker.json": {"source": "hassanaftab93/pentesting-mcp-setup", "expected": set()},
    "ingenimax-devops-agent.yaml": {"source": "Ingenimax/agent-sdk-go", "expected": {"XONE003"}},
    "kubernetes-http-enable-all-tools.yaml": {
        "source": "containers/kubernetes-mcp-server",
        "expected": set(),
    },
    "nyldn-zed-context-servers.json": {"source": "nyldn/claude-octopus", "expected": {"XONE003"}},
    "run-llama-claude-llamacloud.json": {"source": "run-llama/llamacloud-mcp", "expected": {"XONE003"}},
}


def _rule_ids(name: str) -> set[str]:
    return {finding.rule_id for finding in scan_config(CORPUS / name).findings}


def test_corpus_v2_manifest_lists_all_sources():
    manifest = (CORPUS / "README.md").read_text(encoding="utf-8")

    for name, meta in FIXTURES.items():
        assert name in manifest
        assert meta["source"] in manifest
    assert "Sanitization policy" in manifest


def test_corpus_v2_sample_matrix_lists_all_sources():
    matrix = Path("docs/real-world-sample-matrix.md").read_text(encoding="utf-8")

    for name, meta in FIXTURES.items():
        assert name in matrix
        assert meta["source"] in matrix
    assert "2026-06-12" in matrix


def test_corpus_v2_files_scan_without_parse_errors():
    for name in FIXTURES:
        report = scan_config(CORPUS / name)
        assert report.files[0].status == "scanned"
        assert report.errors == []


def test_corpus_v2_expected_rule_boundaries():
    for name, meta in FIXTURES.items():
        rule_ids = _rule_ids(name)
        assert meta["expected"] <= rule_ids, f"{name} expected {meta['expected']} in {rule_ids}"


def test_corpus_v2_local_node_entrypoints_do_not_trigger_remote_package_rule():
    assert "XONE003" not in _rule_ids("cline-official-settings-path.json")
    assert "XONE003" not in _rule_ids("confluent-local-node-config.json")


def test_corpus_v2_cli_secret_flags_do_not_trigger_literal_secret_rule():
    assert "XONE001" not in _rule_ids("danlee-mcp-setup-aggregate.json")


def test_corpus_v2_no_real_secret_literals_are_checked_in():
    forbidden = [
        "ctx7sk-9cfe4d92",
        "YOUR_ANTHROPIC_API_KEY_HERE",
        "your_personal_access_token",
        "<YOUR_TOKEN>",
    ]
    for path in CORPUS.iterdir():
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for value in forbidden:
                assert value not in text


def test_rule_tuning_findings_tracks_current_gaps():
    findings = Path("docs/rule-tuning-findings.md").read_text(encoding="utf-8")

    assert "XONE008 candidate" in findings
    assert "Docker image pinning" in findings
    assert "enableAllTools" in findings
    assert "cline_mcp_settings.json" in findings
