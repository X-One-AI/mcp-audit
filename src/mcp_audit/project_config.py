from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib

CONFIG_FILE = ".mcp-audit.toml"

DEFAULT_CONFIG = """# mcp-audit project configuration

[scan]
# Fail the command when unsuppressed findings at this severity or higher exist.
# Allowed values: "high", "medium", "low", "never"
fail_on = "high"

# Optional baseline file for reviewed accepted findings.
baseline = ".mcp-audit-baseline.json"
"""


@dataclass(frozen=True)
class ScanConfig:
    fail_on: str = "never"
    baseline: str | None = None


def load_scan_config(root: str | Path = ".") -> ScanConfig:
    path = Path(root) / CONFIG_FILE
    if not path.exists():
        return ScanConfig()

    data = tomllib.loads(path.read_text(encoding="utf-8"))
    scan = data.get("scan", {})
    fail_on = scan.get("fail_on", "never")
    baseline = scan.get("baseline")
    if fail_on not in {"high", "medium", "low", "never"}:
        fail_on = "never"
    if baseline is not None:
        baseline = str(baseline)
    return ScanConfig(fail_on=fail_on, baseline=baseline)


def write_default_config(path: str | Path = CONFIG_FILE) -> Path:
    output = Path(path)
    if output.exists():
        return output
    output.write_text(DEFAULT_CONFIG, encoding="utf-8")
    return output
