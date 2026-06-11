from __future__ import annotations

from pathlib import Path

import yaml

from mcp_audit.errors import ConfigNotFoundError, ParseConfigError
from mcp_audit.model import ConfigDocument


def parse_yaml_config(path: str | Path) -> ConfigDocument:
    file_path = Path(path)
    if not file_path.exists():
        raise ConfigNotFoundError(file_path)

    try:
        data = yaml.safe_load(file_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ParseConfigError(file_path, str(exc)) from exc

    if not isinstance(data, dict):
        raise ParseConfigError(file_path, "top-level YAML value must be an object")

    return ConfigDocument(path=file_path, parser="yaml", data=data)
