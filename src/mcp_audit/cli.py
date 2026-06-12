from __future__ import annotations

import argparse
import platform
import sys
from pathlib import Path

from mcp_audit import __version__
from mcp_audit.app import scan_config, scan_default_configs
from mcp_audit.baseline import (
    filter_accepted_findings,
    load_baseline_fingerprints,
    prune_baseline,
    render_baseline,
)
from mcp_audit.config_discovery import DEFAULT_CANDIDATES, discover_config_candidates, discover_configs
from mcp_audit.errors import ConfigNotFoundError, McpAuditError, ParseConfigError
from mcp_audit.project_config import CONFIG_FILE, load_scan_config, write_default_config
from mcp_audit.project_config import write_wizard_config
from mcp_audit.renderers.json_report import render_json_report
from mcp_audit.renderers.markdown_report import render_markdown_report
from mcp_audit.renderers.sarif_report import render_sarif_report
from mcp_audit.rules.registry import get_rule_info, get_rule_infos
from mcp_audit.team_policy import (
    check_team_policy,
    filter_policy_exceptions,
    load_policy_exceptions,
    load_team_policy,
    render_baseline_review,
)

_SEVERITY_RANK = {"low": 1, "medium": 2, "high": 3}
_PROFILES = ("starter", "balanced", "team")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mcp-audit")
    parser.add_argument("--version", action="store_true", help="show version and exit")
    subparsers = parser.add_subparsers(dest="command")

    scan = subparsers.add_parser("scan", help="scan an MCP or agent config")
    scan.add_argument("--config", help="config file to scan; defaults to bounded config discovery")
    scan.add_argument("--format", choices=("markdown", "json", "sarif"), default="markdown")
    scan.add_argument("--output", help="write report to file instead of stdout")
    scan.add_argument("--fail-on", choices=("high", "medium", "low", "never"))
    scan.add_argument("--profile", choices=_PROFILES, help="rule profile to use for this scan")
    scan.add_argument("--baseline", help="suppress findings accepted in a baseline file")
    scan.add_argument("--policy", help="team policy file to enforce for this scan")
    scan.add_argument("--baseline-review", help="baseline review TOML file required by enforced team policy")
    scan.add_argument("--exceptions", help="policy exception TOML file with approved finding fingerprints")

    baseline = subparsers.add_parser("baseline", help="write a baseline of currently accepted findings")
    baseline.add_argument("--config", required=True, help="config file to scan for baseline creation")
    baseline.add_argument("--output", required=True, help="baseline JSON file to write")
    baseline.add_argument("--baseline", help="existing baseline file to maintain")
    baseline.add_argument("--prune", action="store_true", help="remove accepted findings that no longer appear")
    baseline.add_argument("--review-output", help="write a baseline review file for the generated baseline")
    baseline.add_argument("--approved-by", help="reviewer name for --review-output")
    baseline.add_argument("--reason", help="review reason for --review-output")

    explain = subparsers.add_parser("explain", help="explain a rule")
    explain.add_argument("rule_id")

    rules = subparsers.add_parser("rules", help="list registered rules")
    rules.add_argument("--profile", choices=_PROFILES, default="balanced", help="show rules enabled by a profile")
    subparsers.add_parser("doctor", help="show runtime and config discovery diagnostics")
    subparsers.add_parser("discover", help="preview supported config paths without scanning")
    init = subparsers.add_parser("init", help="write a project mcp-audit configuration file")
    init.add_argument("--profile", choices=_PROFILES, default="balanced", help="configuration profile to write")
    init.add_argument("--wizard", action="store_true", help="write guided team-ready defaults")
    init.add_argument("--no-policy", action="store_true", help="with --wizard, skip writing the team policy file")

    policy = subparsers.add_parser("policy", help="team policy operations")
    policy_subparsers = policy.add_subparsers(dest="policy_command")
    policy_check = policy_subparsers.add_parser("check", help="check team policy without writing a report")
    policy_check.add_argument("--policy", required=True, help="team policy TOML file")
    policy_check.add_argument("--profile", choices=_PROFILES, help="profile to check")
    policy_check.add_argument("--config", action="append", default=[], help="config path to check; repeatable")
    policy_check.add_argument("--baseline", help="baseline file to validate")
    policy_check.add_argument("--baseline-review", help="baseline review TOML file")
    policy_check.add_argument("--exceptions", help="policy exception TOML file")
    return parser


def _render(report, output_format: str) -> str:
    if output_format == "sarif":
        return render_sarif_report(report)
    if output_format == "json":
        return render_json_report(report)
    return render_markdown_report(report)


def _should_fail(report, threshold: str) -> bool:
    if threshold == "never":
        return False
    required = _SEVERITY_RANK[threshold]
    return any(_SEVERITY_RANK[finding.severity] >= required for finding in report.findings)


def _write_output(text: str, output: str | None) -> None:
    if output:
        Path(output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


def _load_scan_baseline(path: str | None, *, explicit: bool) -> set[str]:
    if path is None:
        return set()
    if Path(path).exists():
        return load_baseline_fingerprints(path)
    if explicit:
        raise McpAuditError(f"Baseline file not found: {path}")
    return set()


def _emit_policy_violations(violations) -> None:
    for violation in violations:
        print(f"{violation.code}: {violation.message}", file=sys.stderr)


def _policy_exit_code(policy, violations) -> int:
    if not violations:
        return 0
    return 1 if policy.mode == "enforced" else 0


def _run_doctor() -> int:
    found = {str(path) for path in discover_configs()}
    project_config = load_scan_config()
    config_status = f"found ({CONFIG_FILE})" if Path(CONFIG_FILE).exists() else "missing"
    next_command = "mcp-audit scan" if found else "mcp-audit discover"
    lines = [
        f"mcp-audit {__version__}",
        f"Python: {platform.python_version()}",
        f"Platform: {platform.platform()}",
        f"Project config: {config_status}",
        f"Effective profile: {project_config.profile}",
        f"Effective fail-on: {project_config.fail_on}",
        f"Effective baseline: {project_config.baseline or 'none'}",
        "",
        "Default config discovery:",
    ]
    for candidate in DEFAULT_CANDIDATES:
        status = "found" if candidate in found else "missing"
        lines.append(f"- {candidate}: {status}")
    lines.extend(
        [
            "",
            "No network calls are required for scanning.",
            f"Next recommended command: `{next_command}`",
            "Use `mcp-audit scan --config PATH` to scan a specific file.",
            "",
        ]
    )
    sys.stdout.write("\n".join(lines))
    return 0


def _relative_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path)


def _run_discover() -> int:
    candidates = discover_config_candidates()
    lines = [
        "Config discovery preview",
        "",
        "Supported default paths:",
    ]
    if candidates.supported:
        for path in candidates.supported:
            lines.append(f"- {_relative_path(path)}")
    else:
        lines.append("- none")

    lines.extend(["", "Ignored supported filenames outside bounded defaults:"])
    if candidates.ignored_supported_names:
        for path in candidates.ignored_supported_names:
            lines.append(f"- {_relative_path(path)}")
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "No files were scanned.",
            "Run `mcp-audit scan` to scan supported default paths.",
            "Run `mcp-audit scan --config PATH` to scan a specific file.",
            "",
        ]
    )
    sys.stdout.write("\n".join(lines))
    return 0


def _list_rules(profile: str = "balanced") -> int:
    lines = ["Rule     Severity  Category      Title", "-------  --------  ------------  -----"]
    for rule in get_rule_infos(profile=profile):
        lines.append(f"{rule.id:<7}  {rule.severity:<8}  {rule.category:<12}  {rule.title}")
    lines.append("")
    sys.stdout.write("\n".join(lines))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code or 0)

    if args.version:
        print(f"mcp-audit {__version__}")
        return 0

    if args.command is None:
        parser.print_help(sys.stderr)
        return 2

    try:
        if args.command == "doctor":
            return _run_doctor()

        if args.command == "discover":
            return _run_discover()

        if args.command == "rules":
            return _list_rules(profile=args.profile)

        if args.command == "init":
            if args.wizard:
                paths = write_wizard_config(profile=args.profile, write_policy=not args.no_policy)
                for path in paths:
                    print(f"Wrote {path}")
                print("Next: run `mcp-audit policy check --policy .mcp-audit-policy.toml --profile team`")
                return 0
            path = write_default_config(profile=args.profile)
            print(f"Wrote {path}")
            return 0

        if args.command == "policy":
            if args.policy_command != "check":
                print("Unknown policy command", file=sys.stderr)
                return 2
            project_config = load_scan_config()
            profile = args.profile or project_config.profile
            policy = load_team_policy(args.policy)
            violations = check_team_policy(
                policy,
                profile=profile,
                config_paths=args.config,
                baseline_path=args.baseline,
                baseline_review_path=args.baseline_review,
                exceptions_path=args.exceptions,
            )
            if violations:
                _emit_policy_violations(violations)
                return _policy_exit_code(policy, violations)
            print("Policy check passed")
            return 0

        if args.command == "scan":
            project_config = load_scan_config()
            profile = args.profile or project_config.profile
            baseline = args.baseline or project_config.baseline
            baseline_for_policy = baseline if baseline and Path(baseline).exists() else None
            fail_on = args.fail_on or project_config.fail_on
            report = scan_config(args.config, profile=profile) if args.config else scan_default_configs(profile=profile)
            report = filter_accepted_findings(report, _load_scan_baseline(baseline, explicit=args.baseline is not None))
            if args.exceptions:
                exceptions, exception_violations = load_policy_exceptions(args.exceptions)
                if exception_violations:
                    _emit_policy_violations(exception_violations)
                    return 1
                report = filter_policy_exceptions(report, exceptions)
            policy_failed = False
            if args.policy:
                policy = load_team_policy(args.policy)
                violations = check_team_policy(
                    policy,
                    profile=profile,
                    config_paths=[args.config] if args.config else [],
                    baseline_path=baseline_for_policy,
                    baseline_review_path=args.baseline_review,
                    exceptions_path=args.exceptions,
                    report=report,
                )
                if violations:
                    _emit_policy_violations(violations)
                    if policy.mode == "enforced":
                        policy_failed = True
            _write_output(_render(report, args.format), args.output)
            if policy_failed:
                return 1
            return 1 if _should_fail(report, fail_on) else 0

        if args.command == "baseline":
            report = scan_config(args.config)
            if args.prune:
                if not args.baseline:
                    print("--baseline is required when using --prune", file=sys.stderr)
                    return 2
                _write_output(prune_baseline(report, args.baseline), args.output)
                return 0
            _write_output(render_baseline(report), args.output)
            if args.review_output:
                if not args.approved_by or not args.reason:
                    print("--approved-by and --reason are required with --review-output", file=sys.stderr)
                    return 2
                Path(args.review_output).write_text(
                    render_baseline_review(args.output, approved_by=args.approved_by, reason=args.reason),
                    encoding="utf-8",
                )
            return 0

        if args.command == "explain":
            info = get_rule_info(args.rule_id)
            if info is None:
                print(f"Unknown rule: {args.rule_id}", file=sys.stderr)
                return 2
            sys.stdout.write(
                "\n".join(
                    [
                        f"# {info.id}: {info.title}",
                        "",
                        f"Severity: {info.severity}",
                        f"Category: {info.category}",
                        "",
                        info.description,
                        "",
                        "When this is acceptable: only after a reviewer documents why the access is required and why a narrower configuration is not practical.",
                        "",
                        f"Remediation: {info.remediation}",
                        "",
                        "Policy exception guidance: prefer a reviewed baseline for known findings; use a time-bounded policy exception only when the risk owner accepts this exact finding fingerprint.",
                        "",
                    ]
                )
            )
            return 0
    except (ConfigNotFoundError, ParseConfigError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except McpAuditError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"Unexpected internal error: {exc}", file=sys.stderr)
        return 3

    print(f"Unknown command: {args.command}", file=sys.stderr)
    return 2


def entrypoint() -> None:
    raise SystemExit(main())


if __name__ == "__main__":
    entrypoint()
