from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from hashlib import sha256
from pathlib import Path
import tomllib

from mcp_audit.model import ScanReport
from mcp_audit.rules.registry import PROFILE_RULE_IDS

POLICY_SCHEMA_VERSION = 1
KNOWN_POLICY_MODES = {"advisory", "enforced"}
KNOWN_PROFILES = {"starter", "balanced", "team"}
SEVERITY_RANK = {"low": 1, "medium": 2, "high": 3}


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
    baseline_review_file: str = ".mcp-audit-baseline.review.toml"
    max_allowed_severity: str = "high"


@dataclass(frozen=True)
class PolicyViolation:
    code: str
    message: str


@dataclass(frozen=True)
class PolicyException:
    fingerprint: str
    rule_id: str
    reason: str
    approved_by: str
    expires_on: date


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
        baseline_review_file=str(raw_policy.get("baseline_review_file", ".mcp-audit-baseline.review.toml")),
        max_allowed_severity=_choice(raw_policy.get("max_allowed_severity", "high"), {"high", "medium", "low", "never"}, "high"),
    )


def check_team_policy(
    policy: TeamPolicy,
    *,
    profile: str,
    config_paths: list[str | Path] | None = None,
    baseline_path: str | Path | None = None,
    baseline_review_path: str | Path | None = None,
    exceptions_path: str | Path | None = None,
    report: ScanReport | None = None,
) -> list[PolicyViolation]:
    violations: list[PolicyViolation] = []
    enabled_rules = PROFILE_RULE_IDS.get(profile, PROFILE_RULE_IDS["balanced"])

    if profile not in policy.allowed_profiles:
        violations.append(PolicyViolation("XONEP001", f'profile "{profile}" is not allowed by team policy'))
    if profile != policy.required_profile:
        violations.append(PolicyViolation("XONEP002", f'profile "{profile}" does not match required profile "{policy.required_profile}"'))

    missing_rules = sorted(set(policy.required_rules) - enabled_rules)
    if missing_rules:
        violations.append(PolicyViolation("XONEP003", f"required rules are not enabled by profile {profile}: {', '.join(missing_rules)}"))

    blocked_enabled_rules = sorted(set(policy.blocked_rules) & enabled_rules)
    if blocked_enabled_rules:
        violations.append(PolicyViolation("XONEP004", f"blocked rules are enabled by profile {profile}: {', '.join(blocked_enabled_rules)}"))

    if not policy.allow_global_config_scan:
        for config_path in config_paths or []:
            if _is_outside_cwd(Path(config_path)):
                violations.append(PolicyViolation("XONEP005", f"global config path is not allowed by team policy: {config_path}"))

    if baseline_path and policy.require_baseline_review:
        review_path = Path(baseline_review_path or policy.baseline_review_file)
        violations.extend(_check_baseline_review(Path(baseline_path), review_path))

    if exceptions_path:
        _, exception_violations = load_policy_exceptions(exceptions_path)
        violations.extend(exception_violations)

    if report is not None and policy.max_allowed_severity != "never":
        threshold = SEVERITY_RANK[policy.max_allowed_severity]
        blocking = [finding for finding in report.findings if SEVERITY_RANK[finding.severity] >= threshold]
        if blocking:
            violations.append(
                PolicyViolation(
                    "XONEP006",
                    f"{len(blocking)} unsuppressed findings meet or exceed max_allowed_severity={policy.max_allowed_severity}",
                )
            )

    return violations


def load_policy_exceptions(path: str | Path, today: date | None = None) -> tuple[list[PolicyException], list[PolicyViolation]]:
    today = today or date.today()
    data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    raw_items = data.get("exceptions", [])
    exceptions: list[PolicyException] = []
    violations: list[PolicyViolation] = []

    if not isinstance(raw_items, list):
        return [], [PolicyViolation("XONEP010", "exceptions file must use [[exceptions]] entries")]

    for index, item in enumerate(raw_items, start=1):
        if not isinstance(item, dict):
            violations.append(PolicyViolation("XONEP011", f"exception #{index} must be a table"))
            continue
        fingerprint = str(item.get("fingerprint", ""))
        rule_id = str(item.get("rule_id", ""))
        reason = str(item.get("reason", ""))
        approved_by = str(item.get("approved_by", ""))
        expires_raw = item.get("expires_on")
        if not fingerprint or not rule_id or not reason or not approved_by or not expires_raw:
            violations.append(PolicyViolation("XONEP012", f"exception #{index} must include fingerprint, rule_id, reason, approved_by, and expires_on"))
            continue
        try:
            expires_on = expires_raw if isinstance(expires_raw, date) else date.fromisoformat(str(expires_raw))
        except ValueError:
            violations.append(PolicyViolation("XONEP013", f"exception #{index} has invalid expires_on date"))
            continue
        if expires_on < today:
            violations.append(PolicyViolation("XONEP014", f"exception #{index} expired on {expires_on.isoformat()}"))
            continue
        exceptions.append(
            PolicyException(
                fingerprint=fingerprint,
                rule_id=rule_id,
                reason=reason,
                approved_by=approved_by,
                expires_on=expires_on,
            )
        )
    return exceptions, violations


def filter_policy_exceptions(report: ScanReport, exceptions: list[PolicyException]) -> ScanReport:
    accepted = {(exception.fingerprint, exception.rule_id) for exception in exceptions}
    if not accepted:
        return report
    suppressed = [
        finding
        for finding in report.findings
        if (finding.fingerprint, finding.rule_id) in accepted
    ]
    return ScanReport(
        files=report.files,
        findings=[
            finding
            for finding in report.findings
            if (finding.fingerprint, finding.rule_id) not in accepted
        ],
        suppressed_findings=[*report.suppressed_findings, *suppressed],
        errors=report.errors,
        schema_version=report.schema_version,
    )


def render_baseline_review(baseline_path: str | Path, *, approved_by: str, reason: str) -> str:
    digest = _file_sha256(Path(baseline_path))
    return "\n".join(
        [
            "[baseline_review]",
            f'baseline_path = "{Path(baseline_path)}"',
            f'sha256 = "{digest}"',
            f'approved_by = "{approved_by}"',
            f'reason = "{reason}"',
            "",
        ]
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


def _check_baseline_review(baseline_path: Path, review_path: Path) -> list[PolicyViolation]:
    if not baseline_path.exists():
        return [PolicyViolation("XONEP007", f"baseline file does not exist: {baseline_path}")]
    if not review_path.exists():
        return [PolicyViolation("XONEP008", f"baseline review file is required: {review_path}")]

    data = tomllib.loads(review_path.read_text(encoding="utf-8"))
    review = data.get("baseline_review", data)
    expected = str(review.get("sha256", ""))
    approved_by = str(review.get("approved_by", ""))
    reason = str(review.get("reason", ""))
    actual = _file_sha256(baseline_path)
    violations = []
    if expected != actual:
        violations.append(PolicyViolation("XONEP009", f"baseline review hash does not match {baseline_path}"))
    if not approved_by or not reason:
        violations.append(PolicyViolation("XONEP015", "baseline review must include approved_by and reason"))
    return violations


def _file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _is_outside_cwd(path: Path) -> bool:
    try:
        path.resolve().relative_to(Path.cwd().resolve())
    except ValueError:
        return True
    return False
