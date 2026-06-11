from __future__ import annotations

from mcp_audit.model import ConfigDocument, Finding
from mcp_audit.rules.base import make_finding, walk_json

_DANGEROUS_CONTAINER_ARGS = {
    "--privileged": "container runs privileged",
    "--network=host": "container uses host network",
    "--pid=host": "container uses host PID namespace",
}


class DangerousContainerOptionRule:
    id = "XONE007"
    title = "Dangerous container option"
    category = "command"
    default_severity = "high"
    description = "Configuration launches a container with host-level or privileged access."
    remediation = "Remove privileged or host namespace options unless there is a reviewed, narrow operational need."

    def evaluate(self, document: ConfigDocument) -> list[Finding]:
        findings: list[Finding] = []
        for path, value in walk_json(document.data):
            if not isinstance(value, str):
                continue
            for option, evidence in _DANGEROUS_CONTAINER_ARGS.items():
                if value == option:
                    findings.append(self._finding(document, path, evidence))
            if value in {"/:/host", "/:/workspace"}:
                findings.append(self._finding(document, path, f"container mounts host root as {value}"))
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
