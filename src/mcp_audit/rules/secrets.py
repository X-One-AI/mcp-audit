from __future__ import annotations

from mcp_audit.model import ConfigDocument, Finding
from mcp_audit.redaction import looks_like_literal_secret, redact_text
from mcp_audit.rules.base import make_finding, walk_json


class LiteralSecretRule:
    id = "XONE001"
    title = "Literal secret appears in configuration"
    category = "secret"
    default_severity = "high"
    description = "Configuration appears to contain a literal token, API key, or credential."
    remediation = "Move the value to a secret manager or environment variable reference."

    def evaluate(self, document: ConfigDocument) -> list[Finding]:
        findings: list[Finding] = []
        for path, value in walk_json(document.data):
            if looks_like_literal_secret(value):
                findings.append(
                    make_finding(
                        document=document,
                        rule_id=self.id,
                        title=self.title,
                        severity=self.default_severity,
                        category=self.category,
                        config_path=path,
                        evidence="literal value matched a secret-like pattern",
                        redacted_evidence=redact_text(value),
                        remediation=self.remediation,
                        confidence="high",
                    )
                )
        return findings
