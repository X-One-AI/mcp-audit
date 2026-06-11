from __future__ import annotations

from pathlib import Path

from mcp_audit.config_discovery import discover_configs, resolve_config
from mcp_audit.errors import NoConfigDiscoveredError
from mcp_audit.model import ScannedFile, ScanReport
from mcp_audit.parsers.json_parser import parse_json_config
from mcp_audit.rules.registry import get_rules


def _scan_one(path: str | Path):
    file_path = resolve_config(path)
    document = parse_json_config(file_path)
    findings = []
    for rule in get_rules():
        findings.extend(rule.evaluate(document))
    findings.sort(key=lambda item: (item.rule_id, item.config_path, item.evidence))
    return ScannedFile(path=str(file_path), parser=document.parser, status="scanned"), findings


def scan_config(path: str | Path) -> ScanReport:
    scanned_file, findings = _scan_one(path)
    return ScanReport(files=[scanned_file], findings=findings)


def scan_default_configs(root: str | Path = ".") -> ScanReport:
    configs = discover_configs(root)
    if not configs:
        raise NoConfigDiscoveredError()

    files: list[ScannedFile] = []
    findings = []
    for config in configs:
        scanned_file, config_findings = _scan_one(config)
        files.append(scanned_file)
        findings.extend(config_findings)
    findings.sort(key=lambda item: (item.rule_id, item.config_path, item.evidence))
    return ScanReport(files=files, findings=findings)
