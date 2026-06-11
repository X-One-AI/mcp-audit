# mcp-audit Operating Model

This directory defines how `mcp-audit` is built and maintained.

It references the local One Person Team workflow without modifying it:

```text
/Users/moquqicha/Documents/AHCode/opt/packages/one-person-team-skills
```

Project-specific knowledge, role overlays, constraints, and skill evolution live here.

## Rules

```text
1. Production-usable, not demo-only.
2. Build on OPT, but do not modify OPT source files.
3. Keep project-specific knowledge inside this repo.
4. Keep role adjustments as local overlays, not global skill edits.
5. Let constraints and local skills evolve through explicit review.
6. Keep the public README small and route deeper context here.
```

## Structure

| Path | Purpose |
|---|---|
| [../docs/prd.md](../docs/prd.md) | Product requirements for the first production-usable release. |
| [../docs/architecture.md](../docs/architecture.md) | Architecture brief for the v0.1 CLI and report pipeline. |
| [../docs/expert-review-security.md](../docs/expert-review-security.md) | Security expert gate for the product and architecture. |
| [../docs/qa-plan.md](../docs/qa-plan.md) | QA plan and requirement-to-test coverage for v0.1. |
| [../docs/implementation-plan.md](../docs/implementation-plan.md) | Developer implementation plan for the v0.1 CLI. |
| [opt-overlay.md](./opt-overlay.md) | How this project uses OPT roles without modifying OPT. |
| [constraints/production.md](./constraints/production.md) | Production-readiness constraints for every feature. |
| [constraints/main-entry.md](./constraints/main-entry.md) | Rules for keeping the main entry concise. |
| [knowledge/README.md](./knowledge/README.md) | Project knowledge base entry. |
| [knowledge/domain.md](./knowledge/domain.md) | MCP / agent safety domain assumptions. |
| [skills/evolution.md](./skills/evolution.md) | How local constraints and skills evolve. |
| [skills/local-overlays.md](./skills/local-overlays.md) | Project-specific role overlays. |
| [decisions/README.md](./decisions/README.md) | Lightweight ADR index. |

## Default Workflow

Use OPT stages for non-trivial work:

```text
Intake -> Product -> Architecture -> Expert Gate -> QA -> Development Plan -> TDD Execution -> Review -> Completion Gate
```

Security, production-impacting behavior, rule severity, report contracts, CI behavior, and dependency choices must pass Expert Gate before implementation.

## Active Project

`mcp-audit` is the only active implementation project in X-One right now.

Other X-One projects are reserved directions and should not receive code until `mcp-audit` has real user feedback.
