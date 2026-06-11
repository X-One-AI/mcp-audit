from __future__ import annotations

import json

from mcp_audit import __version__
from mcp_audit.model import Finding, ScanReport

_LEVEL_BY_SEVERITY = {"high": "error", "medium": "warning", "low": "note"}


def _result_for_finding(finding: Finding) -> dict:
    return {
        "ruleId": finding.rule_id,
        "level": _LEVEL_BY_SEVERITY[finding.severity],
        "message": {"text": f"{finding.title}: {finding.remediation}"},
        "locations": [
            {
                "physicalLocation": {
                    "artifactLocation": {"uri": finding.file_path},
                    "region": {"startLine": 1},
                },
                "logicalLocations": [{"fullyQualifiedName": finding.config_path}],
            }
        ],
        "properties": {
            "category": finding.category,
            "confidence": finding.confidence,
            "evidence": finding.redacted_evidence,
            "fingerprint": finding.fingerprint,
        },
    }


def render_sarif_report(report: ScanReport) -> str:
    rules = {}
    for finding in report.findings:
        rules[finding.rule_id] = {
            "id": finding.rule_id,
            "name": finding.title,
            "shortDescription": {"text": finding.title},
            "fullDescription": {"text": finding.description},
            "help": {"text": finding.remediation},
            "properties": {"category": finding.category, "severity": finding.severity},
        }

    payload = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "mcp-audit",
                        "version": __version__,
                        "informationUri": "https://github.com/X-One-AI/mcp-audit",
                        "rules": list(rules.values()),
                    }
                },
                "results": [_result_for_finding(finding) for finding in report.findings],
            }
        ],
    }
    return json.dumps(payload, indent=2, sort_keys=False) + "\n"
