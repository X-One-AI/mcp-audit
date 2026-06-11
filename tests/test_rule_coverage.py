from pathlib import Path

from mcp_audit.parsers.json_parser import parse_json_config
from mcp_audit.rules.registry import get_rules


FIXTURES = Path(__file__).parent / "fixtures"


def test_every_registered_rule_has_positive_and_negative_fixture_coverage():
    high_risk = parse_json_config(FIXTURES / "high-risk-mcp.json")
    safe = parse_json_config(FIXTURES / "safe-mcp.json")

    for rule in get_rules():
        assert rule.evaluate(high_risk), f"{rule.id} needs a positive fixture"
        assert rule.evaluate(safe) == [], f"{rule.id} needs a negative fixture"
