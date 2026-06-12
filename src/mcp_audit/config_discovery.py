from __future__ import annotations

from dataclasses import dataclass
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
    ".claude/claude_desktop_config.json",
    ".continue/config.json",
    ".continue/config.yaml",
    ".windsurf/mcp_config.json",
    ".gemini/settings.json",
    ".qwen/settings.json",
    ".factory/mcp.json",
    ".factory/settings.json",
    ".zed/settings.json",
)

_IGNORED_DIRS = {".git", ".hg", ".svn", ".venv", "node_modules", "__pycache__"}
_SUPPORTED_FILENAMES = {Path(name).name for name in DEFAULT_CANDIDATES}


@dataclass(frozen=True)
class ConfigDiscovery:
    supported: list[Path]
    ignored_supported_names: list[Path]


def resolve_config(path: str | Path) -> Path:
    resolved = Path(path)
    if not resolved.exists():
        raise ConfigNotFoundError(resolved)
    return resolved


def discover_configs(root: str | Path = ".") -> list[Path]:
    base = Path(root)
    return [candidate for name in DEFAULT_CANDIDATES if (candidate := base / name).exists()]


def discover_config_candidates(root: str | Path = ".") -> ConfigDiscovery:
    base = Path(root)
    supported = discover_configs(base)
    supported_resolved = {path.resolve() for path in supported}
    ignored: list[Path] = []

    for path in base.rglob("*"):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(base).parts
        if any(part in _IGNORED_DIRS for part in relative_parts):
            continue
        if path.name not in _SUPPORTED_FILENAMES:
            continue
        if path.resolve() not in supported_resolved:
            ignored.append(path)

    return ConfigDiscovery(supported=supported, ignored_supported_names=sorted(ignored))
