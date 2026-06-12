from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib

POLICY_SCHEMA_VERSION = 1
KNOWN_POLICY_MODES = {"advisory", "enforced"}
KNOWN_PROFILES = {"starter", "balanced", "team"}


@dataclass(frozen=True)
class TeamPolicy:
    schema_version: int = POLICY_SCHEMA_VERSION
    mode: str = "advisory"
    required_profile: str = "balanced"
    allowed_profiles: tuple[str, ...] = ("balanced", "team")
    required_rules: tuple[str, ...] = ()
    blocked_rules: tuple[str, ...] = ()
    allow_global_config_scan: bool = False
    require_baseline_review: bool = True
    max_allowed_severity: str = "high"


def load_team_policy(path: str | Path) -> TeamPolicy:
    data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    raw_policy = data.get("policy", data)

    schema_version = int(raw_policy.get("schema_version", POLICY_SCHEMA_VERSION))
    mode = _choice(raw_policy.get("mode", "advisory"), KNOWN_POLICY_MODES, "advisory")
    required_profile = _choice(raw_policy.get("required_profile", "balanced"), KNOWN_PROFILES, "balanced")
    allowed_profiles = _string_tuple(raw_policy.get("allowed_profiles", ("balanced", "team")))
    allowed_profiles = tuple(profile for profile in allowed_profiles if profile in KNOWN_PROFILES) or ("balanced", "team")

    return TeamPolicy(
        schema_version=schema_version,
        mode=mode,
        required_profile=required_profile,
        allowed_profiles=allowed_profiles,
        required_rules=_string_tuple(raw_policy.get("required_rules", ())),
        blocked_rules=_string_tuple(raw_policy.get("blocked_rules", ())),
        allow_global_config_scan=bool(raw_policy.get("allow_global_config_scan", False)),
        require_baseline_review=bool(raw_policy.get("require_baseline_review", True)),
        max_allowed_severity=_choice(raw_policy.get("max_allowed_severity", "high"), {"high", "medium", "low", "never"}, "high"),
    )


def _choice(value: object, allowed: set[str], fallback: str) -> str:
    if isinstance(value, str) and value in allowed:
        return value
    return fallback


def _string_tuple(value: object) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,)
    if isinstance(value, list | tuple):
        return tuple(item for item in value if isinstance(item, str))
    return ()
