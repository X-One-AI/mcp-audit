from __future__ import annotations

from mcp_audit.model import ScanReport


def render_markdown_report(report: ScanReport) -> str:
    lines: list[str] = [
        "# mcp-audit Report",
        "",
        "## Summary",
        "",
        f"- Files scanned: {report.summary.files_scanned}",
        f"- Findings total: {report.summary.findings_total}",
        f"- High: {report.summary.findings_by_severity['high']}",
        f"- Medium: {report.summary.findings_by_severity['medium']}",
        f"- Low: {report.summary.findings_by_severity['low']}",
        f"- Highest severity: {report.summary.highest_severity or 'none'}",
        f"- Recommended action: {report.summary.recommended_action}",
        "",
        "## Scanned Files",
        "",
    ]

    for scanned_file in report.files:
        lines.append(f"- `{scanned_file.path}` ({scanned_file.parser}, {scanned_file.status})")

    lines.extend(
        [
            "",
            "## Findings",
            "",
        ]
    )

    if not report.findings:
        lines.extend(["No findings.", ""])
    else:
        for finding in report.findings:
            lines.extend(
                [
                    f"### {finding.rule_id}: {finding.title}",
                    "",
                    f"- Severity: {finding.severity}",
                    f"- Category: {finding.category}",
                    f"- Why it matters: {finding.description}",
                    f"- File: `{finding.file_path}`",
                    f"- Config path: `{finding.config_path}`",
                    f"- Fingerprint: `{finding.fingerprint}`",
                    f"- Evidence: {finding.redacted_evidence}",
                    f"- Confidence: {finding.confidence}",
                    f"- Remediation: {finding.remediation}",
                    "",
                ]
            )

    if report.errors:
        lines.extend(["## Errors", ""])
        for error in report.errors:
            location = ""
            if error.line is not None and error.column is not None:
                location = f" at line {error.line}, column {error.column}"
            lines.extend([f"- `{error.file_path}`: {error.message}{location}", ""])

    lines.extend(
        [
            "## Limitations",
            "",
            "mcp-audit reports static risk signals. It does not guarantee security, prevent attacks, or validate runtime behavior.",
            "",
        ]
    )
    return "\n".join(lines)
