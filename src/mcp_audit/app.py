from __future__ import annotations

from pathlib import Path

from mcp_audit.config_discovery import resolve_config
from mcp_audit.model import ScannedFile, ScanReport
from mcp_audit.parsers.json_parser import parse_json_config
from mcp_audit.rules.registry import get_rules


def scan_config(path: str | Path) -> ScanReport:
    file_path = resolve_config(path)
    document = parse_json_config(file_path)
    findings = []
    for rule in get_rules():
        findings.extend(rule.evaluate(document))
    findings.sort(key=lambda item: (item.rule_id, item.config_path, item.evidence))
    return ScanReport(
        files=[ScannedFile(path=str(file_path), parser=document.parser, status="scanned")],
        findings=findings,
    )
