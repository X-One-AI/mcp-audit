from __future__ import annotations

import json
from pathlib import Path

from mcp_audit.errors import ConfigNotFoundError, ParseConfigError
from mcp_audit.model import ConfigDocument


def parse_json_config(path: str | Path) -> ConfigDocument:
    file_path = Path(path)
    if not file_path.exists():
        raise ConfigNotFoundError(file_path)

    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ParseConfigError(
            file_path,
            exc.msg,
            line=exc.lineno,
            column=exc.colno,
        ) from exc

    if not isinstance(data, dict):
        raise ParseConfigError(file_path, "top-level JSON value must be an object")

    return ConfigDocument(path=file_path, parser="json", data=data)
