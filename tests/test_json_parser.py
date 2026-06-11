from pathlib import Path

import pytest

from mcp_audit.errors import ParseConfigError
from mcp_audit.parsers.json_parser import parse_json_config


FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_json_config_returns_normalized_document():
    document = parse_json_config(FIXTURES / "high-risk-mcp.json")

    assert document.parser == "json"
    assert document.path.name == "high-risk-mcp.json"
    assert "mcpServers" in document.data


def test_parse_json_config_reports_file_path_for_invalid_json():
    with pytest.raises(ParseConfigError) as exc:
        parse_json_config(FIXTURES / "invalid-json.json")

    assert "invalid-json.json" in str(exc.value)
    assert exc.value.file_path.name == "invalid-json.json"
