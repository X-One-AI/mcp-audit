from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from mcp_audit.model import Category, ConfigDocument, Finding, Severity


class Rule(Protocol):
    id: str
    title: str
    category: Category
    default_severity: Severity
    description: str
    remediation: str

    def evaluate(self, document: ConfigDocument) -> list[Finding]:
        ...


@dataclass(frozen=True)
class RuleInfo:
    id: str
    title: str
    category: Category
    severity: Severity
    description: str
    remediation: str


def walk_json(value: object, path: str = "$"):
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            yield child_path, child
            yield from walk_json(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_path = f"{path}[{index}]"
            yield child_path, child
            yield from walk_json(child, child_path)


def make_finding(
    *,
    document: ConfigDocument,
    rule_id: str,
    title: str,
    description: str,
    severity: Severity,
    category: Category,
    config_path: str,
    evidence: str,
    redacted_evidence: str,
    remediation: str,
    confidence: str = "medium",
) -> Finding:
    return Finding(
        rule_id=rule_id,
        title=title,
        description=description,
        severity=severity,
        category=category,
        file_path=str(document.path),
        config_path=config_path,
        evidence=evidence,
        redacted_evidence=redacted_evidence,
        remediation=remediation,
        confidence=confidence,  # type: ignore[arg-type]
    )
