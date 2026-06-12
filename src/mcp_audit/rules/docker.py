from __future__ import annotations

import re

from mcp_audit.model import ConfigDocument, Finding
from mcp_audit.rules.base import make_finding, walk_json

_DOCKER_OPTIONS_WITH_VALUES = {"-e", "--env", "-v", "--volume", "--name", "--network", "--pid"}
_DOCKER_SUBCOMMANDS = {"run", "exec", "pull"}
_SENSITIVE_ENV_PATTERN = re.compile(r"(TOKEN|SECRET|PASSWORD|API_KEY|ACCESS_KEY|PRIVATE_KEY)", re.IGNORECASE)
_SHA256_DIGEST_PATTERN = re.compile(r"@sha256:[a-fA-F0-9]{64}$")


def _iter_docker_commands(document: ConfigDocument):
    for path, value in walk_json(document.data):
        if not isinstance(value, dict):
            continue
        if str(value.get("command", "")).lower() != "docker":
            continue
        args = value.get("args", [])
        if isinstance(args, list):
            yield path, args


def _subcommand(args: list) -> str | None:
    for arg in args:
        if isinstance(arg, str) and not arg.startswith("-"):
            return arg
    return None


def _is_digest_pinned(image: str) -> bool:
    return bool(_SHA256_DIGEST_PATTERN.search(image))


def _is_tag_pinned(image: str) -> bool:
    last_segment = image.rsplit("/", 1)[-1]
    if ":" not in last_segment:
        return False
    tag = last_segment.rsplit(":", 1)[1].lower()
    return bool(tag) and tag != "latest"


def _iter_images(args: list) -> list[str]:
    subcommand = _subcommand(args)
    if subcommand not in {"run", "pull"}:
        return []
    after_subcommand = False
    skip_next = False
    for arg in args:
        if skip_next:
            skip_next = False
            continue
        if not isinstance(arg, str):
            continue
        if not after_subcommand:
            after_subcommand = arg == subcommand
            continue
        if arg in _DOCKER_OPTIONS_WITH_VALUES:
            skip_next = True
            continue
        if arg.startswith("-"):
            continue
        if arg.startswith("${") or arg.startswith("<"):
            return []
        return [arg]
    return []


def _iter_env_names(args: list) -> list[str]:
    if _subcommand(args) != "run":
        return []
    env_names = []
    index = 0
    while index < len(args):
        arg = args[index]
        if not isinstance(arg, str):
            index += 1
            continue
        if arg in {"-e", "--env"} and index + 1 < len(args):
            next_arg = args[index + 1]
            if isinstance(next_arg, str):
                env_names.append(next_arg.split("=", 1)[0])
            index += 2
            continue
        if arg.startswith("--env="):
            env_names.append(arg.split("=", 1)[1].split("=", 1)[0])
        index += 1
    return env_names


class UnpinnedContainerImageRule:
    id = "XONE009"
    title = "Unpinned container image"
    category = "supply-chain"
    default_severity = "high"
    description = "Docker MCP server uses a container image without a stable tag or digest."
    remediation = "Pin container images to a reviewed version tag or sha256 digest."

    def evaluate(self, document: ConfigDocument) -> list[Finding]:
        findings: list[Finding] = []
        for path, args in _iter_docker_commands(document):
            for image in _iter_images(args):
                if _is_digest_pinned(image) or _is_tag_pinned(image):
                    continue
                findings.append(
                    make_finding(
                        document=document,
                        rule_id=self.id,
                        title=self.title,
                        description=self.description,
                        severity=self.default_severity,
                        category=self.category,
                        config_path=f"{path}.args",
                        evidence=f"docker image {image} is unpinned",
                        redacted_evidence=f"docker image {image} is unpinned",
                        remediation=self.remediation,
                        confidence="high",
                    )
                )
        return findings


class SensitiveContainerEnvPassthroughRule:
    id = "XONE010"
    title = "Sensitive container environment passthrough"
    category = "secret"
    default_severity = "medium"
    description = "Docker MCP server passes sensitive-looking host environment variables into a container."
    remediation = "Pass only required variables and prefer scoped tokens or secret-manager injection."

    def evaluate(self, document: ConfigDocument) -> list[Finding]:
        findings: list[Finding] = []
        for path, args in _iter_docker_commands(document):
            for env_name in _iter_env_names(args):
                if not _SENSITIVE_ENV_PATTERN.search(env_name):
                    continue
                evidence = f"container receives sensitive env {env_name}"
                findings.append(
                    make_finding(
                        document=document,
                        rule_id=self.id,
                        title=self.title,
                        description=self.description,
                        severity=self.default_severity,
                        category=self.category,
                        config_path=f"{path}.args",
                        evidence=evidence,
                        redacted_evidence=evidence,
                        remediation=self.remediation,
                        confidence="high",
                    )
                )
        return findings
