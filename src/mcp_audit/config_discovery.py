from __future__ import annotations

from pathlib import Path

from mcp_audit.errors import ConfigNotFoundError

DEFAULT_CANDIDATES = (
    "mcp.json",
    ".mcp.json",
    "mcp.yaml",
    "mcp.yml",
    "agent.yaml",
    "agent.yml",
    "agent.toml",
    ".cursor/mcp.json",
    ".vscode/mcp.json",
    ".claude/mcp.json",
    ".continue/config.json",
    ".continue/config.yaml",
)


def resolve_config(path: str | Path) -> Path:
    resolved = Path(path)
    if not resolved.exists():
        raise ConfigNotFoundError(resolved)
    return resolved


def discover_configs(root: str | Path = ".") -> list[Path]:
    base = Path(root)
    return [candidate for name in DEFAULT_CANDIDATES if (candidate := base / name).exists()]
