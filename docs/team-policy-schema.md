# Team Policy Schema

Team policy is separate from rule profiles. Profiles choose rule bundles for a scan; policy describes how an organization expects repositories to use those profiles and how exceptions should be controlled.

The current schema is enforced by `mcp-audit policy check` and `mcp-audit scan --policy`. It is parsed by `mcp_audit.team_policy.load_team_policy`, documented here, and demonstrated in `examples/team-policy.toml`.

## Example

```toml
[policy]
schema_version = 1
mode = "enforced"
required_profile = "team"
allowed_profiles = ["balanced", "team"]
required_rules = ["XONE001", "XONE002", "XONE003"]
blocked_rules = []
allow_global_config_scan = false
require_baseline_review = true
baseline_review_file = ".mcp-audit-baseline.review.toml"
max_allowed_severity = "medium"
```

## Commands

```bash
mcp-audit init --wizard --profile team
mcp-audit policy check --policy .mcp-audit-policy.toml --profile team
mcp-audit scan --config ./mcp.json --profile team --policy .mcp-audit-policy.toml
```

## Fields

| Field | Type | Meaning |
| --- | --- | --- |
| `schema_version` | integer | Policy schema version. Current value is `1`. |
| `mode` | string | `advisory` reports guidance without failing; `enforced` returns non-zero for policy violations. |
| `required_profile` | string | Default profile the team expects in CI. |
| `allowed_profiles` | list of strings | Profiles allowed for local or CI use. |
| `required_rules` | list of strings | Rule IDs that must stay enabled in team-controlled scans. |
| `blocked_rules` | list of strings | Rule IDs the team has explicitly disabled with review context. |
| `allow_global_config_scan` | boolean | Whether policy permits scanning user-level global config paths. |
| `require_baseline_review` | boolean | Whether baseline changes require human review. |
| `baseline_review_file` | string | Default TOML review file containing the reviewed baseline SHA256. |
| `max_allowed_severity` | string | Highest accepted unsuppressed finding severity before the scan should fail. |

## Baseline Review Gate

Generate a reviewed baseline and matching review file:

```bash
mcp-audit baseline --config ./mcp.json --output .mcp-audit-baseline.json \
  --review-output .mcp-audit-baseline.review.toml \
  --approved-by security-team \
  --reason "accepted known MCP risks"
```

When policy requires baseline review, `scan --policy` checks that the review file SHA256 matches the baseline file.

## Exceptions

Use exceptions for time-bounded risk acceptance outside the baseline file:

```toml
[[exceptions]]
fingerprint = "abc123"
rule_id = "XONE004"
reason = "temporary migration path"
approved_by = "security-team"
expires_on = "2026-12-31"
```

Pass exceptions with:

```bash
mcp-audit scan --config ./mcp.json --policy .mcp-audit-policy.toml --exceptions .mcp-audit-exceptions.toml
```

## Constraints

- Keep policy file-based and reviewable.
- Do not depend on a hosted policy service for the local scan path.
- Keep global config scanning explicit because reading home-directory configs can surprise users.
- Treat baselines as risk acceptance, not proof of safety.
