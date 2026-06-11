from pathlib import Path

import pytest

from mcp_audit.config_discovery import discover_configs, resolve_config
from mcp_audit.errors import ConfigNotFoundError


def test_discover_configs_uses_bounded_candidate_paths(tmp_path):
    expected = tmp_path / "mcp.json"
    expected.write_text("{}", encoding="utf-8")
    ignored = tmp_path / "nested" / "mcp.json"
    ignored.parent.mkdir()
    ignored.write_text("{}", encoding="utf-8")

    discovered = discover_configs(tmp_path)

    assert discovered == [expected]


def test_resolve_config_reports_missing_file():
    with pytest.raises(ConfigNotFoundError):
        resolve_config(Path("does-not-exist.json"))
