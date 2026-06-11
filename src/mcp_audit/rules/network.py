from __future__ import annotations

from mcp_audit.model import ConfigDocument, Finding
from mcp_audit.rules.base import make_finding, walk_json


class BroadNetworkAccessRule:
    id = "XONE005"
    title = "Broad network access"
    category = "network"
    default_severity = "medium"
    description = "Configuration appears to allow broad outbound network access."
    remediation = "Document the network purpose or restrict access with an allowlist."

    def evaluate(self, document: ConfigDocument) -> list[Finding]:
        findings: list[Finding] = []
        for path, value in walk_json(document.data):
            if not isinstance(value, str):
                continue
            lowered = value.lower()
            if "https://*" in lowered or "http://*" in lowered or "server-fetch" in lowered:
                findings.append(
                    make_finding(
                        document=document,
                        rule_id=self.id,
                        title=self.title,
                        description=self.description,
                        severity=self.default_severity,
                        category=self.category,
                        config_path=path,
                        evidence="configuration suggests broad outbound network access",
                        redacted_evidence="configuration suggests broad outbound network access",
                        remediation=self.remediation,
                        confidence="medium",
                    )
                )
        return findings
