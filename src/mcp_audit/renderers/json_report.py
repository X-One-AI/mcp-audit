from __future__ import annotations

import json
from dataclasses import asdict

from mcp_audit import __version__
from mcp_audit.model import ScanReport


def render_json_report(report: ScanReport) -> str:
    payload = {
        "schema_version": report.schema_version,
        "tool": {"name": "mcp-audit", "version": __version__},
        "summary": asdict(report.summary),
        "files": [asdict(item) for item in report.files],
        "findings": [asdict(item) for item in report.findings],
        "errors": [asdict(item) for item in report.errors],
    }
    return json.dumps(payload, indent=2, sort_keys=False) + "\n"
