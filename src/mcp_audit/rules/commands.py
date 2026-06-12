from __future__ import annotations

from mcp_audit.model import ConfigDocument, Finding
from mcp_audit.rules.base import make_finding, walk_json

_SHELL_COMMANDS = {"bash", "sh", "zsh", "fish", "powershell", "cmd", "exec", "eval"}
_REMOTE_RUNNERS = {"bunx", "npx", "uvx"}
_FLOATING_VERSIONS = {"latest", "next", "canary", "beta", "alpha", "dev", "nightly"}


def _is_pinned_package(value: str) -> bool:
    version = _extract_package_version(value)
    if version is None:
        return False
    return version.lower() not in _FLOATING_VERSIONS


def _extract_package_version(value: str) -> str | None:
    if value.startswith("@"):
        # Scoped package needs a second @ for the version.
        if value.count("@") < 2:
            return None
        return value.rsplit("@", 1)[1]
    if "@" not in value:
        return None
    return value.rsplit("@", 1)[1]


def _iter_server_maps(value: object, path: str = "$"):
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in {"mcpServers", "context_servers"} and isinstance(child, dict):
                yield child_path, child
            yield from _iter_server_maps(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _iter_server_maps(child, f"{path}[{index}]")


def _server_command_and_args(server: dict) -> tuple[str, list, str] | None:
    command = server.get("command")
    if isinstance(command, str):
        args = server.get("args", [])
        return command.lower(), args if isinstance(args, list) else [], "args"
    if isinstance(command, dict):
        path = command.get("path") or command.get("command")
        args = command.get("args", [])
        if isinstance(path, str):
            return path.lower(), args if isinstance(args, list) else [], "command.args"
    return None


def _candidate_package_args(args: list) -> list[str]:
    candidates = []
    for arg in args:
        if not isinstance(arg, str):
            continue
        if arg.startswith("-") or arg.startswith(".") or arg.startswith("/") or arg.startswith("<"):
            continue
        if "/" in arg and not arg.startswith("@"):
            continue
        candidates.append(arg)
    return list(dict.fromkeys(candidates))


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
        for servers_path, servers in _iter_server_maps(document.data):
            for server_name, server in servers.items():
                if not isinstance(server, dict):
                    continue
                command_and_args = _server_command_and_args(server)
                if command_and_args is None:
                    continue
                command, args, args_path = command_and_args
                if command not in _REMOTE_RUNNERS:
                    continue
                package_args = _candidate_package_args(args)
                if package_args and any(not _is_pinned_package(arg) for arg in package_args):
                    findings.append(
                        make_finding(
                            document=document,
                            rule_id=self.id,
                            title=self.title,
                            description=self.description,
                            severity=self.default_severity,
                            category=self.category,
                            config_path=f"{servers_path}.{server_name}.{args_path}",
                            evidence=f"{command} launches an unpinned package",
                            redacted_evidence=f"{command} launches an unpinned package",
                            remediation=self.remediation,
                            confidence="high",
                        )
                    )
        return findings
