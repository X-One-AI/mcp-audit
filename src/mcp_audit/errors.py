from __future__ import annotations

from pathlib import Path


class McpAuditError(Exception):
    """Base error for expected mcp-audit failures."""


class ParseConfigError(McpAuditError):
    def __init__(
        self,
        file_path: Path,
        message: str,
        *,
        parser: str = "json",
        line: int | None = None,
        column: int | None = None,
    ) -> None:
        self.file_path = file_path
        self.parser = parser
        self.message = message
        self.line = line
        self.column = column
        location = ""
        if line is not None and column is not None:
            location = f" at line {line}, column {column}"
        super().__init__(f"{file_path}: {message}{location}")


class ConfigNotFoundError(McpAuditError):
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        super().__init__(f"Config file not found: {file_path}")
