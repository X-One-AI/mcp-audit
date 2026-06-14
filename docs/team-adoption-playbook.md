# Team Adoption Playbook

This playbook turns `mcp-audit` from a local scanner into a reviewable team workflow. It assumes real-user feedback is collected separately and focuses on the repeatable operating model a team can adopt today.

## 10-minute team adoption path

Use this path when a team wants to try `mcp-audit` without designing a full security program first.

1. **Owner:** assign one reviewer who owns the first scan result and decides whether a finding becomes a fix, a baseline review PR, or a time-bounded exception.
2. Run an advisory scan with explicit config input:

   ```bash
   mcp-audit init --profile starter
   mcp-audit discover
   mcp-audit scan --config ./mcp.json --profile starter --format markdown --output mcp-audit-report.md
   ```

3. Review the report in a pull request. Treat the first report as an advisory scan, not a merge blocker.
4. Fix high-confidence findings before creating any baseline.
5. If existing risk must be accepted, open a baseline review PR with the baseline file, review file, owner, reason, and expiry or revisit trigger.
6. Move to the Production gate only after the team has one clean scan or one reviewed baseline PR.

Production gate:

- `mcp-audit policy check --policy .mcp-audit-policy.toml --profile team` passes.
- `mcp-audit scan --policy --baseline-review` runs in CI.
- Baseline or exception changes require code review.
- False-positive or false-negative feedback has a fixture, documented limitation, or rule-tuning finding before it changes rule behavior.

## Rollout Stages

1. Start in advisory mode with `mcp-audit init --profile starter`.
2. Run `mcp-audit discover` to preview supported config files without scanning.
3. Scan explicit project configs with `mcp-audit scan --config PATH --profile starter`.
4. Fix high-confidence findings before creating a baseline.
5. Create a reviewed baseline only for accepted risks.
6. Move CI to `balanced` after the team has reviewed medium-noise rules.
7. Move CI to `team` when medium findings should block merges.

## CI Gate

Use this gate for repositories that are ready for enforcement:

```bash
mcp-audit init --wizard --profile team
mcp-audit policy check --policy .mcp-audit-policy.toml --profile team
mcp-audit scan --config ./mcp.json \
  --profile team \
  --policy .mcp-audit-policy.toml \
  --baseline .mcp-audit-baseline.json \
  --baseline-review .mcp-audit-baseline.review.toml \
  --fail-on medium
```

## Baseline Review Gate

A baseline is a risk acceptance record, not proof that a finding is safe. Treat the baseline review gate as a required code-review checkpoint.

Required review evidence:

- Reviewer name in `.mcp-audit-baseline.review.toml`
- Reason for accepting the risk
- Matching SHA256 for the current baseline file
- PR discussion explaining why remediation is not practical yet

Do not approve a baseline when the finding contains a real secret, gives broad filesystem access without a bounded path, or enables network/tool access that the workflow does not need.

## Exception Policy

Use policy exceptions for temporary risk acceptance that should expire. Prefer reviewed baselines for known long-lived findings.

An acceptable exception must include:

- Exact finding fingerprint
- Expiration date
- Owner
- Reason
- Link to the issue or PR that will remove the risk

## Pull Request Review

Reviewers should check:

- New findings are remediated or explicitly accepted.
- Baseline changes have matching review hash updates.
- Exceptions are time-bounded and owned.
- `starter` profile is not used in CI after the team has moved to enforcement.
- Reports do not include raw secret values.

## Operational Boundaries

`mcp-audit` is a static local auditor. It does not execute scanned commands, upload configs, run a hosted policy service, or sandbox agent tools.
