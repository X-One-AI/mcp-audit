from __future__ import annotations

from mcp_audit.model import ConfigDocument, Finding
from mcp_audit.rules.base import make_finding, walk_json


def _is_broad_path(value: str) -> bool:
    normalized = value.rstrip("/")
    return normalized in {"/", "~", "$HOME", "${HOME}"} or normalized.startswith("/Users/") or normalized.startswith("/home/")


class BroadFilesystemAccessRule:
    id = "XONE004"
    title = "Broad filesystem access"
    category = "filesystem"
    default_severity = "high"
    description = "Configuration exposes a broad filesystem path to an MCP tool."
    remediation = "Restrict filesystem access to the smallest project-specific directory."

    def evaluate(self, document: ConfigDocument) -> list[Finding]:
        findings: list[Finding] = []
        for path, value in walk_json(document.data):
            if isinstance(value, str) and _is_broad_path(value):
                findings.append(
                    make_finding(
                        document=document,
                        rule_id=self.id,
                        title=self.title,
                        description=self.description,
                        severity=self.default_severity,
                        category=self.category,
                        config_path=path,
                        evidence=f"filesystem path {value} is broad",
                        redacted_evidence=f"filesystem path {value} is broad",
                        remediation=self.remediation,
                        confidence="high",
                    )
                )
        return findings
