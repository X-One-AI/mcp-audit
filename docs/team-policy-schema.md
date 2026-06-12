# Team Policy Schema

Team policy is separate from rule profiles. Profiles choose rule bundles for a scan; policy describes how an organization expects repositories to use those profiles and how exceptions should be controlled.

The current schema is a `v0.2.0` draft. It is parsed by `mcp_audit.team_policy.load_team_policy`, documented here, and demonstrated in `examples/team-policy.toml`. Enforcement is intentionally deferred until the next product slice so the schema can be reviewed before it blocks teams.

## Example

```toml
[policy]
schema_version = 1
mode = "advisory"
required_profile = "team"
allowed_profiles = ["balanced", "team"]
required_rules = ["XONE001", "XONE002", "XONE003"]
blocked_rules = []
allow_global_config_scan = false
require_baseline_review = true
max_allowed_severity = "medium"
```

## Fields

| Field | Type | Meaning |
| --- | --- | --- |
| `schema_version` | integer | Policy schema version. Current value is `1`. |
| `mode` | string | `advisory` records guidance; `enforced` is reserved for a future blocking mode. |
| `required_profile` | string | Default profile the team expects in CI. |
| `allowed_profiles` | list of strings | Profiles allowed for local or CI use. |
| `required_rules` | list of strings | Rule IDs that must stay enabled in team-controlled scans. |
| `blocked_rules` | list of strings | Rule IDs the team has explicitly disabled with review context. |
| `allow_global_config_scan` | boolean | Whether policy permits scanning user-level global config paths. |
| `require_baseline_review` | boolean | Whether baseline changes require human review. |
| `max_allowed_severity` | string | Highest accepted unsuppressed finding severity before the scan should fail. |

## Constraints

- Keep policy file-based and reviewable.
- Do not depend on a hosted policy service for the local scan path.
- Keep global config scanning explicit because reading home-directory configs can surprise users.
- Treat baselines as risk acceptance, not proof of safety.
