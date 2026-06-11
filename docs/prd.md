# mcp-audit PRD

## Problem Statement

AI agents and MCP tools are moving into developer workflows where they can access repositories, terminals, filesystems, credentials, external services, and CI jobs. Teams want the productivity benefits, but they lack a simple, reviewable way to inspect MCP / agent configuration risk before trusting these tools in real projects.

`mcp-audit` solves the first layer of this problem: it scans MCP and AI agent configurations, detects high-signal risk patterns, and generates local reports that engineers and security reviewers can act on.

This is not a demo project. The product must be small enough to ship early, but every shipped behavior must be production-usable in a real repository.

## Target Users

- Developers using MCP servers with local AI assistants or coding agents.
- Small engineering teams adopting AI coding agents in repositories.
- DevTools and platform engineers responsible for internal developer workflows.
- DevSecOps and security platform engineers reviewing agent/tool access risk.
- Founders or CTOs deciding whether AI agents can safely touch source code, credentials, CI, or local systems.

## Goals

- Provide a local-first CLI that scans MCP / agent configuration files for high-signal risks.
- Generate human-readable Markdown reports and machine-readable JSON reports.
- Use stable rule IDs, clear severity, and concrete remediation guidance.
- Support production-ready behavior from the first release: deterministic scans, no hidden network calls, no telemetry, clear failure modes, and testable rule fixtures.
- Use the One Person Team workflow as a reference, while keeping project-specific knowledge, constraints, and role overlays inside `mcp-audit/ops/`.
- Keep public entrypoints concise and route deep operating context to `ops/` and `docs/`.
- Allow constraints, local skill overlays, and rule knowledge to evolve through explicit review and recorded decisions.

## Non-Goals

- No runtime sandboxing in v0.1.
- No runtime policy enforcement in v0.1.
- No hosted service in v0.1.
- No dashboard in v0.1.
- No claim that `mcp-audit` prevents attacks or makes agents safe.
- No broad AI production-readiness checklist in v0.1.
- No scanning of every possible agent framework in v0.1.
- No modification of global OPT files.
- No telemetry, remote upload, or background network access.

## Scenarios

- A developer adds a new MCP filesystem server and wants to know whether it exposes too much local file access.
- A team reviews an agent configuration before allowing it in a repository.
- A security reviewer wants a Markdown report that explains risky commands, literal secrets, and broad permissions.
- A platform engineer wants JSON output that can later feed CI checks or dashboards.
- A maintainer wants rule findings to include severity, evidence, and remediation without exaggerated security claims.
- A future agent worker needs project-specific constraints and knowledge without reading chat history or modifying OPT.

## Requirements

| ID | Requirement | Priority | Source |
| --- | --- | --- | --- |
| REQ-001 | Provide a CLI command to scan an explicitly provided MCP / agent config file. | must | Product |
| REQ-002 | Provide a CLI command that can discover supported config files in the current repository or working directory. | should | Product |
| REQ-003 | Support JSON config parsing for the first release. | must | Product |
| REQ-004 | Support YAML config parsing if a supported MCP / agent config format requires it during v0.1 validation. | should | Product |
| REQ-005 | Detect literal secret-like values in supported config files. | must | Security |
| REQ-006 | Detect unsafe command execution patterns such as shell, exec, eval, bash, sh, and equivalent launchers. | must | Security |
| REQ-007 | Detect unpinned remote package execution through tools such as `npx`, `uvx`, `curl | sh`, or similar patterns. | must | Security |
| REQ-008 | Detect broad filesystem access such as home, root, or overly broad workspace paths. | must | Security |
| REQ-009 | Detect broad network or external service access when the config gives enough evidence to identify it. | should | Security |
| REQ-010 | Detect basic CI / PR safety gaps only when scanning supported workflow files is explicitly enabled. | could | Product |
| REQ-011 | Generate Markdown reports with summary, findings, evidence, severity, and remediation. | must | Product |
| REQ-012 | Generate JSON reports with stable keys suitable for automated processing. | must | Product |
| REQ-013 | Use stable rule IDs for all findings. | must | Architecture |
| REQ-014 | Provide an `explain` command or equivalent documentation path for each rule. | must | Product |
| REQ-015 | Redact sensitive values in human-readable reports by default. | must | Security |
| REQ-016 | Preserve enough evidence in reports for reviewers to understand why a finding appeared. | must | Product |
| REQ-017 | Separate parser, rule engine, findings model, report rendering, CLI, and fixtures into clear modules. | must | Architecture |
| REQ-018 | Add at least one positive and one negative fixture for every rule. | must | QA |
| REQ-019 | Add contract tests for Markdown and JSON report output. | must | QA |
| REQ-020 | Keep `mcp-audit/README.md` concise and route operating details to `ops/`. | must | User constraint |
| REQ-021 | Store project-specific knowledge, constraints, role overlays, and decisions in `mcp-audit/ops/`. | must | User constraint |
| REQ-022 | Reference OPT workflow, but do not edit global OPT source files. | must | User constraint |
| REQ-023 | Record changes to project constraints or local overlays through explicit review and decision notes when they affect future work. | should | User constraint |
| REQ-024 | Avoid hidden network calls, telemetry, uploads, or external service access during scan. | must | Security |
| REQ-025 | Avoid security overclaims in CLI output, reports, README, and docs. | must | Security |

## Non-Functional Requirements

- Performance: v0.1 scans should complete in under 2 seconds for a repository with typical MCP / agent configs and small CI workflow files. Large repository traversal must be bounded by explicit supported paths or options.
- Reliability: scans must be deterministic for the same input files and version. Parse failures must produce actionable errors without crashing the process.
- Security and privacy: scans are local-first. The tool must not upload files, send telemetry, or expose raw secret values in human-readable output.
- Accessibility: CLI output and Markdown reports must be readable without color. Color may be added later only as optional enhancement.
- Compatibility: v0.1 should run on current macOS and Linux development environments. Windows support can be documented as unverified until tested.
- Observability: v0.1 does not need telemetry. It should provide verbose local logs only when requested by CLI flags.
- Maintainability: rule definitions must be easy to test, document, and review independently.
- Extensibility: report contracts and rule IDs must allow future GitHub Action integration without breaking early adopters.

## Acceptance Criteria

- Running `mcp-audit scan --config mcp-audit/examples/high-risk-mcp.json --format markdown` produces a Markdown report with high-risk findings for literal secret exposure, unpinned remote package execution, broad filesystem access, and unsafe shell execution.
- Running `mcp-audit scan --config mcp-audit/examples/high-risk-mcp.json --format json` produces valid JSON with stable top-level keys for scanned files, findings, severities, rule IDs, evidence, and remediation.
- Human-readable reports redact literal secret values while preserving enough context to identify the affected config path or key.
- Every v0.1 rule has at least one positive fixture and one negative fixture.
- JSON report contract tests fail if required report keys are removed or renamed.
- Markdown report tests fail if rule ID, severity, evidence, or remediation sections are missing.
- The CLI exits non-zero on parse errors and reports the file path and parse reason.
- The CLI does not make network calls during scan.
- `mcp-audit/README.md` remains concise and links deeper operating context to `mcp-audit/ops/README.md`.
- OPT source files outside this repository remain unmodified.
- Any new project-specific constraint or role overlay is added under `mcp-audit/ops/` and, when future-impacting, gets a decision record.

## Prototype Need

- Required: no visual prototype for v0.1.
- Reason: v0.1 is a CLI and report-generation product. It still requires example CLI output and report examples for product validation.
- Expected fidelity: existing pattern reference through sample Markdown and JSON reports.

## Constraints

- The first release must be production-usable, not demo-only.
- The first release must stay local-first.
- The first release must keep scope to static audit and report generation.
- The project may reference OPT but must not modify OPT.
- Project-specific knowledge must live in `mcp-audit/ops/knowledge/`.
- Project-specific role overlays must live in `mcp-audit/ops/skills/`.
- Public README content must remain small and user-facing.
- Security wording must describe risk signals and review support, not guaranteed protection.

## Risks And Open Questions

| Risk or question | Impact | Owner | Status |
| --- | --- | --- | --- |
| Supported MCP config formats may vary across clients and tools. | high | Product / Architect | partially mitigated by bounded default discovery |
| Literal secret detection can produce false positives or miss uncommon secret formats. | high | Security / QA | open |
| Unsafe command rules may be noisy if legitimate MCP servers use shell wrappers. | medium | Security / Product | open |
| Broad filesystem path rules need platform-aware path handling. | medium | Architect | open |
| CI / PR safety checks may expand scope too early. | medium | Product | open |
| Windows compatibility is not yet validated. | low | QA | open |
| Users may expect runtime enforcement from a security-themed tool. | medium | Product / Security | mitigated by non-goals and wording constraints |

## Change Control

- Scope changes after handoff require a change request and affected artifact rechecks.
- Any requirement that adds runtime enforcement, network behavior, telemetry, hosted services, or destructive actions requires Product, Architecture, Security, and QA re-review.
- Any change to rule severity semantics requires Expert Review and QA fixture updates.
- Any change to project-local role overlays must be recorded under `mcp-audit/ops/skills/` and may require a decision record.

## Handoff Package

- `from_role`: Product Manager
- `to_role`: Architect
- `handoff_reason`: Define architecture for the first production-usable `mcp-audit` CLI and report pipeline.
- `input_context`: X-One focuses on Safe Agent Operations. `mcp-audit` is the first active project and must scan MCP / agent configs for risk signals while staying local-first and production-usable.
- `decisions_already_made`: v0.1 is static audit only; no runtime enforcement, hosted service, dashboard, telemetry, or hidden network calls. OPT is referenced, not modified. Project-specific constraints and knowledge live under `mcp-audit/ops/`.
- `open_questions`: exact v0.1 config formats beyond JSON; CI workflow scanning scope; Windows compatibility; secret detection patterns.
- `expected_output`: architecture brief covering module boundaries, data flow, CLI/report contracts, rule engine shape, parser strategy, fixture strategy, security boundaries, and implementation handoff.
- `acceptance_criteria`: architecture enables all PRD acceptance criteria and gives developers enough detail to create an implementation plan without guessing contracts.
- `risk_notes`: security overclaiming, false positives, secret handling, and hidden network behavior are high-risk review areas.
