from __future__ import annotations

from mcp_audit.model import ConfigDocument, Finding
from mcp_audit.rules.base import make_finding, walk_json


class BroadToolEnablementRule:
    id = "XONE008"
    title = "Broad tool enablement"
    category = "command"
    default_severity = "medium"
    description = "Configuration enables all tools instead of an explicit allowlist."
    remediation = "Replace all-tool enablement with the smallest reviewed tool allowlist."

    def evaluate(self, document: ConfigDocument) -> list[Finding]:
        findings: list[Finding] = []
        for path, value in walk_json(document.data):
            key = path.rsplit(".", 1)[-1].lower()
            if key in {"enablealltools", "allowalltools"} and value is True:
                findings.append(self._finding(document, path, f"{key} is true"))
            if key == "tools" and value == "*":
                findings.append(self._finding(document, path, 'tools is "*"'))
        return findings

    def _finding(self, document: ConfigDocument, config_path: str, evidence: str) -> Finding:
        return make_finding(
            document=document,
            rule_id=self.id,
            title=self.title,
            description=self.description,
            severity=self.default_severity,
            category=self.category,
            config_path=config_path,
            evidence=evidence,
            redacted_evidence=evidence,
            remediation=self.remediation,
            confidence="high",
        )
