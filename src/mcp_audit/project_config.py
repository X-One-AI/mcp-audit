from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib

CONFIG_FILE = ".mcp-audit.toml"
PROFILE_DEFAULT_FAIL_ON = {
    "starter": "high",
    "balanced": "high",
    "team": "medium",
}

DEFAULT_CONFIG_TEMPLATE = """# mcp-audit project configuration

[scan]
# Rule profile. Allowed values: "starter", "balanced", "team"
profile = "{profile}"

# Fail the command when unsuppressed findings at this severity or higher exist.
# Allowed values: "high", "medium", "low", "never"
fail_on = "{fail_on}"

# Optional baseline file for reviewed accepted findings.
baseline = ".mcp-audit-baseline.json"
"""


@dataclass(frozen=True)
class ScanConfig:
    fail_on: str = "never"
    baseline: str | None = None
    profile: str = "balanced"


def render_default_config(profile: str = "balanced") -> str:
    if profile not in PROFILE_DEFAULT_FAIL_ON:
        profile = "balanced"
    return DEFAULT_CONFIG_TEMPLATE.format(profile=profile, fail_on=PROFILE_DEFAULT_FAIL_ON[profile])


def load_scan_config(root: str | Path = ".") -> ScanConfig:
    path = Path(root) / CONFIG_FILE
    if not path.exists():
        return ScanConfig()

    data = tomllib.loads(path.read_text(encoding="utf-8"))
    scan = data.get("scan", {})
    profile = scan.get("profile", "balanced")
    if profile not in PROFILE_DEFAULT_FAIL_ON:
        profile = "balanced"
    fail_on = scan.get("fail_on", "never")
    baseline = scan.get("baseline")
    if fail_on not in {"high", "medium", "low", "never"}:
        fail_on = "never"
    if baseline is not None:
        baseline = str(baseline)
    return ScanConfig(fail_on=fail_on, baseline=baseline, profile=profile)


def write_default_config(path: str | Path = CONFIG_FILE, profile: str = "balanced") -> Path:
    output = Path(path)
    if output.exists():
        return output
    output.write_text(render_default_config(profile=profile), encoding="utf-8")
    return output
