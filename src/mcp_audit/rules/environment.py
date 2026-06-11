from __future__ import annotations

from mcp_audit.model import ConfigDocument, Finding
from mcp_audit.rules.base import make_finding, walk_json


class BroadEnvironmentExposureRule:
    id = "XONE006"
    title = "Broad environment exposure"
    category = "secret"
    default_severity = "high"
    description = "Configuration appears to pass the full process environment to an MCP or agent tool."
    remediation = "Pass only the environment variables the tool requires, preferably by explicit name."

    def evaluate(self, document: ConfigDocument) -> list[Finding]:
        findings: list[Finding] = []
        for path, value in walk_json(document.data):
            lowered_path = path.lower()
            if lowered_path.endswith(".env") and value == "*":
                findings.append(self._finding(document, path, "env is '*'"))
            if lowered_path.endswith(".passenvironment") and value is True:
                findings.append(self._finding(document, path, "passEnvironment is true"))
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
