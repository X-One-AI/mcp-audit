from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
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

    @property
    def fingerprint(self) -> str:
        stable_parts = [
            self.rule_id,
            self.file_path,
            self.config_path,
            self.redacted_evidence,
        ]
        return sha256("\x1f".join(stable_parts).encode("utf-8")).hexdigest()[:16]


@dataclass(frozen=True)
class ReportSummary:
    files_scanned: int
    findings_total: int
    suppressed_findings_total: int
    findings_by_severity: dict[str, int]
    highest_severity: Severity | None
    recommended_action: str


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
    suppressed_findings: list[Finding] = field(default_factory=list)
    schema_version: str = "0.1"

    @property
    def summary(self) -> ReportSummary:
        counts = {"high": 0, "medium": 0, "low": 0}
        for finding in self.findings:
            counts[finding.severity] += 1
        highest_severity = None
        recommended_action = "No findings detected. Review limitations before treating this as approval."
        if counts["high"]:
            highest_severity = "high"
            recommended_action = "Review high severity findings before allowing this configuration in production."
        elif counts["medium"]:
            highest_severity = "medium"
            recommended_action = "Review medium severity findings and document accepted risk."
        elif counts["low"]:
            highest_severity = "low"
            recommended_action = "Review low severity findings during normal maintenance."
        return ReportSummary(
            files_scanned=len(self.files),
            findings_total=len(self.findings),
            suppressed_findings_total=len(self.suppressed_findings),
            findings_by_severity=counts,
            highest_severity=highest_severity,
            recommended_action=recommended_action,
        )
