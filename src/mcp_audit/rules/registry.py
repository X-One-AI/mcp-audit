from __future__ import annotations

from mcp_audit.rules.base import Rule, RuleInfo
from mcp_audit.rules.commands import UnpinnedRemotePackageRule, UnsafeCommandRule
from mcp_audit.rules.containers import DangerousContainerOptionRule
from mcp_audit.rules.docker import SensitiveContainerEnvPassthroughRule, UnpinnedContainerImageRule
from mcp_audit.rules.environment import BroadEnvironmentExposureRule
from mcp_audit.rules.filesystem import BroadFilesystemAccessRule
from mcp_audit.rules.network import BroadNetworkAccessRule
from mcp_audit.rules.secrets import LiteralSecretRule
from mcp_audit.rules.tool_enablement import BroadToolEnablementRule

PROFILE_RULE_IDS = {
    "starter": {"XONE001", "XONE002", "XONE003", "XONE004", "XONE006", "XONE007", "XONE009"},
    "balanced": {
        "XONE001",
        "XONE002",
        "XONE003",
        "XONE004",
        "XONE005",
        "XONE006",
        "XONE007",
        "XONE008",
        "XONE009",
        "XONE010",
    },
    "team": {
        "XONE001",
        "XONE002",
        "XONE003",
        "XONE004",
        "XONE005",
        "XONE006",
        "XONE007",
        "XONE008",
        "XONE009",
        "XONE010",
    },
}


def get_rules(profile: str = "balanced") -> list[Rule]:
    enabled = PROFILE_RULE_IDS.get(profile, PROFILE_RULE_IDS["balanced"])
    return [
        rule
        for rule in _all_rules()
        if rule.id in enabled
    ]


def _all_rules() -> list[Rule]:
    return [
        LiteralSecretRule(),
        UnsafeCommandRule(),
        UnpinnedRemotePackageRule(),
        BroadFilesystemAccessRule(),
        BroadNetworkAccessRule(),
        BroadEnvironmentExposureRule(),
        DangerousContainerOptionRule(),
        BroadToolEnablementRule(),
        UnpinnedContainerImageRule(),
        SensitiveContainerEnvPassthroughRule(),
    ]


def get_rule_info(rule_id: str) -> RuleInfo | None:
    for info in get_rule_infos():
        if info.id == rule_id:
            return info
    return None


def get_rule_infos(profile: str = "balanced") -> list[RuleInfo]:
    return [
        RuleInfo(
            id=rule.id,
            title=rule.title,
            category=rule.category,
            severity=rule.default_severity,
            description=rule.description,
            remediation=rule.remediation,
        )
        for rule in get_rules(profile=profile)
    ]
