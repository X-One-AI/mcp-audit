# Team Governance Gate

This guide turns `mcp-audit` from a local scanner into a reviewable team gate. It is intentionally file-based so policy, baseline changes, and exceptions can go through normal code review.

## Target State

A production team repository should contain:

- `.mcp-audit.toml` for local and CI scan defaults.
- `.mcp-audit-policy.toml` for required profile, required rules, global-config boundaries, baseline review, and severity gates.
- `.mcp-audit-baseline.json` only when existing findings are accepted.
- `.mcp-audit-baseline.review.toml` when a baseline exists and policy requires human review.
- `.mcp-audit-exceptions.toml` only for time-bounded exceptions.
- A CI workflow that runs `mcp-audit scan --policy` and uploads SARIF.

## Bootstrap

```bash
mcp-audit init --wizard --profile team
mcp-audit policy check --policy .mcp-audit-policy.toml --profile team
```

For a stricter starting point, copy `examples/team-policy.enforced.toml` to `.mcp-audit-policy.toml`.

## Baseline Review

Use a baseline only to accept known findings that cannot be fixed immediately:

```bash
mcp-audit baseline --config ./mcp.json --output .mcp-audit-baseline.json \
  --review-output .mcp-audit-baseline.review.toml \
  --approved-by security-team \
  --reason "accepted known MCP risks"
```

Policy enforcement checks the baseline review hash. If the baseline changes without a matching review file, `scan --policy` fails.

## Exceptions

Use exceptions for exact finding fingerprints with an owner and expiry date:

```bash
cp examples/policy-exceptions.toml .mcp-audit-exceptions.toml
mcp-audit scan --config ./mcp.json --policy .mcp-audit-policy.toml --exceptions .mcp-audit-exceptions.toml
```

Expired exceptions fail policy checks. Do not use exceptions as a permanent allowlist.

## CI Gate

Copy `examples/github-actions-team-policy.yml` into `.github/workflows/mcp-audit.yml` and adjust the config path. The gate should run on pull requests and protected branches.

Recommended branch protection:

- Require the MCP Audit workflow before merge.
- Require at least one reviewer for baseline or policy changes.
- Treat `.mcp-audit-baseline.json`, `.mcp-audit-baseline.review.toml`, `.mcp-audit-policy.toml`, and `.mcp-audit-exceptions.toml` as security-owned files.

## Review Rules

- Policy changes must explain why profile, severity, or rule requirements changed.
- Baseline changes must include a regenerated review file.
- Exception changes must include a clear reason, approver, and expiry.
- Global config scans must stay explicit because they can read user-level agent configuration.
- SARIF upload is for visibility; the CLI exit code remains the merge gate.
