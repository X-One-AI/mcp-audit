from __future__ import annotations

from mcp_audit.rules.base import Rule, RuleInfo
from mcp_audit.rules.commands import UnpinnedRemotePackageRule, UnsafeCommandRule
from mcp_audit.rules.filesystem import BroadFilesystemAccessRule
from mcp_audit.rules.network import BroadNetworkAccessRule
from mcp_audit.rules.secrets import LiteralSecretRule


def get_rules() -> list[Rule]:
    return [
        LiteralSecretRule(),
        UnsafeCommandRule(),
        UnpinnedRemotePackageRule(),
        BroadFilesystemAccessRule(),
        BroadNetworkAccessRule(),
    ]


def get_rule_info(rule_id: str) -> RuleInfo | None:
    for info in get_rule_infos():
        if info.id == rule_id:
            return info
    return None


def get_rule_infos() -> list[RuleInfo]:
    return [
        RuleInfo(
            id=rule.id,
            title=rule.title,
            category=rule.category,
            severity=rule.default_severity,
            description=rule.description,
            remediation=rule.remediation,
        )
        for rule in get_rules()
    ]
