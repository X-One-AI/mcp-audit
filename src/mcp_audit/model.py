from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

Severity = Literal["high", "medium", "low"]
Confidence = Literal["high", "medium", "low"]
Category = Literal[
    "secret",
    "command",
    "supply-chain",
    "filesystem",
    "network",
    "ci",
    "documentation",
]


@dataclass(frozen=True)
class ConfigDocument:
    path: Path
    parser: str
    data: dict[str, Any]


@dataclass(frozen=True)
class ScannedFile:
    path: str
    parser: str
    status: str


@dataclass(frozen=True)
class Finding:
    rule_id: str
    title: str
    description: str
    severity: Severity
    category: Category
    file_path: str
    config_path: str
    evidence: str
    redacted_evidence: str
    remediation: str
    confidence: Confidence = "medium"


@dataclass(frozen=True)
class ReportSummary:
    files_scanned: int
    findings_total: int
    findings_by_severity: dict[str, int]


@dataclass(frozen=True)
class ScanError:
    file_path: str
    parser: str
    message: str
    line: int | None = None
    column: int | None = None


@dataclass(frozen=True)
class ScanReport:
    files: list[ScannedFile]
    findings: list[Finding]
    errors: list[ScanError] = field(default_factory=list)
    schema_version: str = "0.1"

    @property
    def summary(self) -> ReportSummary:
        counts = {"high": 0, "medium": 0, "low": 0}
        for finding in self.findings:
            counts[finding.severity] += 1
        return ReportSummary(
            files_scanned=len(self.files),
            findings_total=len(self.findings),
            findings_by_severity=counts,
        )
