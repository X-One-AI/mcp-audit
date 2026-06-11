# OPT Overlay For mcp-audit

## Source Of Truth

This project references One Person Team skills from:

```text
/Users/moquqicha/Documents/AHCode/opt/packages/one-person-team-skills
```

Do not edit those files for `mcp-audit`.

## Overlay Rule

Project-specific behavior must be added here, not upstream:

```text
mcp-audit/ops/
```

This keeps global OPT reusable while allowing `mcp-audit` to have its own product judgment, domain knowledge, and role constraints.

## Role Mapping

| OPT Role | How mcp-audit uses it |
|---|---|
| Product Manager | Defines user pain, target persona, non-goals, acceptance criteria, and validation metrics. |
| Architect | Owns CLI boundaries, parser/report contracts, rule engine shape, and extension points. |
| Expert Reviewer | Reviews MCP, secret, supply-chain, CI, and false-positive risk before release. |
| QA Engineer | Defines fixture matrix, CLI contract checks, report snapshot tests, and regression scope. |
| Developer | Implements only after PRD, architecture, expert gate, QA plan, and implementation plan exist. |
| Completion Gate | Verifies tests, docs, release notes, residual risks, and production-readiness constraints. |

## Project-Specific Role Adjustments

These are local overlays, not global OPT changes:

```text
- Product must reject demo-only features.
- Architect must preserve a small public entrypoint and route detail to ops/docs.
- Expert Reviewer must check security wording so the tool does not overclaim protection.
- QA must include false-positive and false-negative fixtures for each rule.
- Developer must avoid hidden network access and avoid sending config data anywhere.
```

## Handoff Requirement

Every non-trivial feature must include:

```text
- intended user
- production value
- non-goals
- contracts changed
- rule severity impact
- test fixtures
- documentation impact
- known residual risk
```
