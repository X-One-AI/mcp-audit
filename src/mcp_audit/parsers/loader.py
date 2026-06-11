from __future__ import annotations

from pathlib import Path

from mcp_audit.errors import ParseConfigError
from mcp_audit.model import ConfigDocument
from mcp_audit.parsers.json_parser import parse_json_config
from mcp_audit.parsers.toml_parser import parse_toml_config
from mcp_audit.parsers.yaml_parser import parse_yaml_config

_YAML_SUFFIXES = {".yaml", ".yml"}


def parse_config(path: str | Path) -> ConfigDocument:
    file_path = Path(path)
    suffix = file_path.suffix.lower()
    if suffix == ".json":
        return parse_json_config(file_path)
    if suffix in _YAML_SUFFIXES:
        return parse_yaml_config(file_path)
    if suffix == ".toml":
        return parse_toml_config(file_path)
    raise ParseConfigError(file_path, f"unsupported config extension: {suffix or '<none>'}")
