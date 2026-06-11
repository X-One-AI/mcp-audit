from __future__ import annotations

import argparse
import platform
import sys
from pathlib import Path

from mcp_audit import __version__
from mcp_audit.app import scan_config, scan_default_configs
from mcp_audit.config_discovery import DEFAULT_CANDIDATES, discover_configs
from mcp_audit.errors import ConfigNotFoundError, McpAuditError, ParseConfigError
from mcp_audit.renderers.json_report import render_json_report
from mcp_audit.renderers.markdown_report import render_markdown_report
from mcp_audit.renderers.sarif_report import render_sarif_report
from mcp_audit.rules.registry import get_rule_info, get_rule_infos

_SEVERITY_RANK = {"low": 1, "medium": 2, "high": 3}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mcp-audit")
    parser.add_argument("--version", action="store_true", help="show version and exit")
    subparsers = parser.add_subparsers(dest="command")

    scan = subparsers.add_parser("scan", help="scan an MCP or agent config")
    scan.add_argument("--config", help="config file to scan; defaults to bounded config discovery")
    scan.add_argument("--format", choices=("markdown", "json", "sarif"), default="markdown")
    scan.add_argument("--output", help="write report to file instead of stdout")
    scan.add_argument("--fail-on", choices=("high", "medium", "low", "never"), default="never")

    explain = subparsers.add_parser("explain", help="explain a rule")
    explain.add_argument("rule_id")

    subparsers.add_parser("rules", help="list registered rules")
    subparsers.add_parser("doctor", help="show runtime and config discovery diagnostics")
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


def _run_doctor() -> int:
    found = {str(path) for path in discover_configs()}
    lines = [
        f"mcp-audit {__version__}",
        f"Python: {platform.python_version()}",
        f"Platform: {platform.platform()}",
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
            "Use `mcp-audit scan --config PATH` to scan a specific file.",
            "",
        ]
    )
    sys.stdout.write("\n".join(lines))
    return 0


def _list_rules() -> int:
    lines = ["Rule     Severity  Category      Title", "-------  --------  ------------  -----"]
    for rule in get_rule_infos():
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

        if args.command == "rules":
            return _list_rules()

        if args.command == "scan":
            report = scan_config(args.config) if args.config else scan_default_configs()
            _write_output(_render(report, args.format), args.output)
            return 1 if _should_fail(report, args.fail_on) else 0

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
                        f"Remediation: {info.remediation}",
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
