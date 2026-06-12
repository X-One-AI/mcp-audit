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

WIZARD_TEAM_POLICY_TEMPLATE = """[policy]
schema_version = 1
mode = "enforced"
required_profile = "{profile}"
allowed_profiles = ["balanced", "team"]
required_rules = ["XONE001", "XONE002", "XONE003", "XONE004", "XONE005", "XONE006", "XONE007", "XONE008", "XONE009", "XONE010"]
blocked_rules = []
allow_global_config_scan = false
require_baseline_review = true
baseline_review_file = ".mcp-audit-baseline.review.toml"
max_allowed_severity = "{max_allowed_severity}"
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


def write_wizard_config(
    *,
    profile: str = "team",
    write_policy: bool = True,
    policy_path: str | Path = ".mcp-audit-policy.toml",
) -> list[Path]:
    config_path = write_default_config(profile=profile)
    written = [config_path]
    if write_policy:
        output = Path(policy_path)
        if not output.exists():
            max_allowed = "medium" if profile == "team" else "high"
            output.write_text(
                WIZARD_TEAM_POLICY_TEMPLATE.format(profile=profile, max_allowed_severity=max_allowed),
                encoding="utf-8",
            )
        written.append(output)
    return written
