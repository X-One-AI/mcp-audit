from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from mcp_audit import __version__
from mcp_audit.model import Finding, ScanReport


def render_baseline(report: ScanReport) -> str:
    payload = {
        "schema_version": report.schema_version,
        "tool": "mcp-audit",
        "tool_version": __version__,
        "accepted_findings": [
            {
                "fingerprint": finding.fingerprint,
                "rule_id": finding.rule_id,
                "severity": finding.severity,
                "file_path": finding.file_path,
                "config_path": finding.config_path,
                "title": finding.title,
            }
            for finding in report.findings
        ],
    }
    return json.dumps(payload, indent=2, sort_keys=False) + "\n"


def prune_baseline(report: ScanReport, baseline_path: str | Path) -> str:
    data = json.loads(Path(baseline_path).read_text(encoding="utf-8"))
    current_fingerprints = {finding.fingerprint for finding in report.findings}
    accepted = data.get("accepted_findings", [])
    data["accepted_findings"] = [
        item
        for item in accepted
        if isinstance(item, dict) and item.get("fingerprint") in current_fingerprints
    ]
    return json.dumps(data, indent=2, sort_keys=False) + "\n"


def load_baseline_fingerprints(path: str | Path | None) -> set[str]:
    if path is None:
        return set()

    data = json.loads(Path(path).read_text(encoding="utf-8"))
    accepted = data.get("accepted_findings", [])
    return {
        str(item["fingerprint"])
        for item in accepted
        if isinstance(item, dict) and item.get("fingerprint")
    }


def filter_accepted_findings(report: ScanReport, accepted_fingerprints: set[str]) -> ScanReport:
    if not accepted_fingerprints:
        return report

    return ScanReport(
        files=report.files,
        findings=[finding for finding in report.findings if finding.fingerprint not in accepted_fingerprints],
        suppressed_findings=[
            finding for finding in report.findings if finding.fingerprint in accepted_fingerprints
        ],
        errors=report.errors,
        schema_version=report.schema_version,
    )


def finding_to_dict(finding: Finding) -> dict:
    data = asdict(finding)
    data["fingerprint"] = finding.fingerprint
    return data
