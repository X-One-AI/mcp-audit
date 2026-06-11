from pathlib import Path

from mcp_audit.rules.registry import get_rule_infos


def test_rules_document_mentions_every_registered_rule():
    rules_doc = Path("docs/rules.md").read_text(encoding="utf-8")

    for rule in get_rule_infos():
        assert rule.id in rules_doc
        assert rule.title in rules_doc
