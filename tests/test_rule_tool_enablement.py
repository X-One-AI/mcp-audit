from mcp_audit.model import ConfigDocument
from mcp_audit.rules.tool_enablement import BroadToolEnablementRule


def _rule_ids(data):
    document = ConfigDocument(path="tool-enable.json", parser="json", data=data)
    return {finding.rule_id for finding in BroadToolEnablementRule().evaluate(document)}


def test_flags_enable_all_tools_true():
    assert _rule_ids({"mcpServers": {"kubernetes": {"enableAllTools": True}}}) == {"XONE008"}


def test_flags_allow_all_tools_true():
    assert _rule_ids({"agents": [{"allowAllTools": True}]}) == {"XONE008"}


def test_flags_tools_wildcard():
    assert _rule_ids({"mcpServers": {"agent": {"tools": "*"}}}) == {"XONE008"}


def test_ignores_explicit_tool_allowlist():
    assert _rule_ids({"mcpServers": {"agent": {"tools": ["read_file", "list_issues"]}}}) == set()
