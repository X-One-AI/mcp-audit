from __future__ import annotations

from mcp_audit.model import ConfigDocument, Finding
from mcp_audit.rules.base import make_finding, walk_json

_SHELL_COMMANDS = {"bash", "sh", "zsh", "fish", "powershell", "cmd", "exec", "eval"}
_REMOTE_RUNNERS = {"npx", "uvx"}


def _is_pinned_package(value: str) -> bool:
    if "@" not in value:
        return False
    if value.startswith("@"):
        # Scoped package needs a second @ for the version.
        return value.count("@") >= 2
    return True


class UnsafeCommandRule:
    id = "XONE002"
    title = "Unsafe command execution path"
    category = "command"
    default_severity = "high"
    description = "Configuration launches a shell or command execution surface."
    remediation = "Avoid unrestricted shell execution or wrap it with a narrow, documented tool."

    def evaluate(self, document: ConfigDocument) -> list[Finding]:
        findings: list[Finding] = []
        for path, value in walk_json(document.data):
            if isinstance(value, str) and path.endswith(".command") and value.lower() in _SHELL_COMMANDS:
                findings.append(
                    make_finding(
                        document=document,
                        rule_id=self.id,
                        title=self.title,
                        description=self.description,
                        severity=self.default_severity,
                        category=self.category,
                        config_path=path,
                        evidence=f"command uses {value}",
                        redacted_evidence=f"command uses {value}",
                        remediation=self.remediation,
                        confidence="high",
                    )
                )
            if isinstance(value, str) and "curl " in value and "| sh" in value:
                findings.append(
                    make_finding(
                        document=document,
                        rule_id=self.id,
                        title=self.title,
                        description=self.description,
                        severity=self.default_severity,
                        category=self.category,
                        config_path=path,
                        evidence="command pipes remote script into shell",
                        redacted_evidence="command pipes remote script into shell",
                        remediation=self.remediation,
                        confidence="high",
                    )
                )
        return findings


class UnpinnedRemotePackageRule:
    id = "XONE003"
    title = "Unpinned remote package execution"
    category = "supply-chain"
    default_severity = "high"
    description = "Configuration launches a remote package without an explicit version pin."
    remediation = "Pin remote packages to a reviewed version."

    def evaluate(self, document: ConfigDocument) -> list[Finding]:
        findings: list[Finding] = []
        servers = document.data.get("mcpServers", {})
        if not isinstance(servers, dict):
            return findings

        for server_name, server in servers.items():
            if not isinstance(server, dict):
                continue
            command = str(server.get("command", "")).lower()
            args = server.get("args", [])
            if command not in _REMOTE_RUNNERS or not isinstance(args, list):
                continue
            package_args = [
                str(arg)
                for arg in args
                if isinstance(arg, str) and not arg.startswith("-") and not arg.startswith(".") and "/" not in arg
            ]
            for arg in args:
                if isinstance(arg, str) and arg.startswith("@"):
                    package_args.append(arg)
            package_args = list(dict.fromkeys(package_args))
            if any(arg.startswith("@") and not _is_pinned_package(arg) for arg in package_args):
                findings.append(
                    make_finding(
                        document=document,
                        rule_id=self.id,
                        title=self.title,
                        description=self.description,
                        severity=self.default_severity,
                        category=self.category,
                        config_path=f"$.mcpServers.{server_name}.args",
                        evidence=f"{command} launches an unpinned package",
                        redacted_evidence=f"{command} launches an unpinned package",
                        remediation=self.remediation,
                        confidence="high",
                    )
                )
        return findings
