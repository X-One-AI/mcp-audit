from pathlib import Path

from mcp_audit.team_policy import load_team_policy


def test_team_policy_example_loads_expected_defaults():
    policy = load_team_policy(Path("examples/team-policy.toml"))

    assert policy.schema_version == 1
    assert policy.mode == "advisory"
    assert policy.required_profile == "team"
    assert policy.allowed_profiles == ("balanced", "team")
    assert policy.allow_global_config_scan is False
    assert policy.require_baseline_review is True
    assert policy.max_allowed_severity == "medium"
    assert "XONE001" in policy.required_rules


def test_team_policy_invalid_values_fall_back_to_safe_defaults(tmp_path):
    path = tmp_path / "policy.toml"
    path.write_text(
        """
[policy]
schema_version = 1
mode = "unsafe"
required_profile = "unknown"
allowed_profiles = ["unknown"]
allow_global_config_scan = true
require_baseline_review = false
max_allowed_severity = "critical"
""",
        encoding="utf-8",
    )

    policy = load_team_policy(path)

    assert policy.mode == "advisory"
    assert policy.required_profile == "balanced"
    assert policy.allowed_profiles == ("balanced", "team")
    assert policy.allow_global_config_scan is True
    assert policy.require_baseline_review is False
    assert policy.max_allowed_severity == "high"
