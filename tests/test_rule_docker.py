from mcp_audit.model import ConfigDocument
from mcp_audit.rules.docker import SensitiveContainerEnvPassthroughRule, UnpinnedContainerImageRule


def _findings_for(rule, data):
    document = ConfigDocument(path="docker.json", parser="json", data=data)
    return rule.evaluate(document)


def test_flags_untagged_container_image():
    findings = _findings_for(
        UnpinnedContainerImageRule(),
        {"mcpServers": {"github": {"command": "docker", "args": ["run", "ghcr.io/github/github-mcp-server"]}}},
    )

    assert {finding.rule_id for finding in findings} == {"XONE009"}


def test_flags_latest_container_image():
    findings = _findings_for(
        UnpinnedContainerImageRule(),
        {"mcpServers": {"tool": {"command": "docker", "args": ["run", "mcp/brave-search:latest"]}}},
    )

    assert {finding.rule_id for finding in findings} == {"XONE009"}


def test_flags_latest_official_container_image():
    findings = _findings_for(
        UnpinnedContainerImageRule(),
        {"mcpServers": {"tool": {"command": "docker", "args": ["run", "--rm", "python:latest"]}}},
    )

    assert {finding.rule_id for finding in findings} == {"XONE009"}


def test_allows_version_tagged_container_image():
    findings = _findings_for(
        UnpinnedContainerImageRule(),
        {"mcpServers": {"tool": {"command": "docker", "args": ["run", "mcp/brave-search:1.2.3"]}}},
    )

    assert findings == []


def test_allows_digest_pinned_container_image():
    findings = _findings_for(
        UnpinnedContainerImageRule(),
        {
            "mcpServers": {
                "tool": {
                    "command": "docker",
                    "args": ["run", "mcp/brave-search@sha256:" + "a" * 64],
                }
            }
        },
    )

    assert findings == []


def test_ignores_docker_exec_paths_for_image_pinning():
    findings = _findings_for(
        UnpinnedContainerImageRule(),
        {
            "mcpServers": {
                "tool": {
                    "command": "docker",
                    "args": ["exec", "-i", "kali-mcp-server", "python3", "/app/kali_server.py"],
                }
            }
        },
    )

    assert findings == []


def test_flags_sensitive_env_passthrough():
    findings = _findings_for(
        SensitiveContainerEnvPassthroughRule(),
        {"mcpServers": {"github": {"command": "docker", "args": ["run", "-e", "GITHUB_TOKEN", "safe/image:1.0.0"]}}},
    )

    assert {finding.rule_id for finding in findings} == {"XONE010"}
    assert findings[0].redacted_evidence == "container receives sensitive env GITHUB_TOKEN"


def test_flags_sensitive_env_passthrough_with_equals_value_without_leaking_value():
    findings = _findings_for(
        SensitiveContainerEnvPassthroughRule(),
        {
            "mcpServers": {
                "github": {
                    "command": "docker",
                    "args": ["run", "-e", "GITHUB_TOKEN=ghp_example_literal_token", "safe/image:1.0.0"],
                }
            }
        },
    )

    assert {finding.rule_id for finding in findings} == {"XONE010"}
    assert "ghp_example_literal_token" not in findings[0].redacted_evidence


def test_ignores_non_sensitive_env_passthrough():
    findings = _findings_for(
        SensitiveContainerEnvPassthroughRule(),
        {"mcpServers": {"tool": {"command": "docker", "args": ["run", "-e", "LOG_LEVEL", "safe/image:1.0.0"]}}},
    )

    assert findings == []
