# mcp-audit Architecture Brief

## Context

`mcp-audit` is the first active X-One project. It scans MCP / AI agent configuration files for high-signal risk patterns and produces local Markdown and JSON reports.

The v0.1 product is a production-usable static auditor, not a demo, runtime sandbox, hosted service, or enforcement gateway. It references the One Person Team workflow but keeps project-specific constraints and knowledge inside `mcp-audit/ops/`.

The architecture must support:

```text
- deterministic local CLI scans
- stable rule IDs
- secret-safe human-readable reports
- machine-readable JSON output
- fixture-based rule tests
- future GitHub Action integration
```

## Module Boundaries

Recommended implementation root:

```text
mcp-audit/src/mcp_audit/
```

| Module | Responsibility |
|---|---|
| `cli.py` | Parse CLI arguments, call application services, map results to exit codes. |
| `app.py` | Orchestrate scan flow without CLI-specific formatting. |
| `config_discovery.py` | Resolve explicit config paths and discover supported files in bounded locations. |
| `parsers/json_parser.py` | Parse JSON files into normalized config documents. |
| `parsers/yaml_parser.py` | Optional future parser for YAML; not required for the JSON-first v0.1 path. |
| `model.py` | Define shared data models: scanned file, finding, evidence, severity, report. |
| `rules/base.py` | Define rule interface and rule result contract. |
| `rules/secrets.py` | Detect literal secret-like values. |
| `rules/commands.py` | Detect unsafe shells, exec/eval patterns, and unpinned remote command execution. |
| `rules/filesystem.py` | Detect broad filesystem access. |
| `rules/network.py` | Detect broad network/external access when config evidence is present. |
| `rules/registry.py` | Register enabled rules and expose rule metadata for `explain`. |
| `redaction.py` | Redact sensitive values for human-readable reports. |
| `renderers/json_report.py` | Render stable machine-readable JSON report. |
| `renderers/markdown_report.py` | Render concise human-readable Markdown report. |
| `errors.py` | Define parse, scan, validation, and CLI errors. |

Recommended test root:

```text
mcp-audit/tests/
```

| Test Area | Responsibility |
|---|---|
| `tests/fixtures/` | Positive and negative configs for every rule. |
| `tests/test_rules_*.py` | Rule-level expectations. |
| `tests/test_json_report.py` | JSON report contract. |
| `tests/test_markdown_report.py` | Markdown report contract. |
| `tests/test_cli.py` | CLI command behavior and exit codes. |
| `tests/test_redaction.py` | Secret redaction behavior. |

## Data Flow

1. User runs `mcp-audit scan --config <path> --format <markdown|json>` or `mcp-audit scan` for bounded default discovery.
2. `cli.py` validates arguments and calls `app.scan()`.
3. `config_discovery.py` resolves explicit files or bounded default search paths.
4. Parser modules load supported files into normalized `ConfigDocument` objects.
5. Rule registry returns enabled rules.
6. Each rule evaluates each document and emits zero or more `Finding` objects.
7. `redaction.py` redacts sensitive evidence for human-readable output.
8. Report renderer produces Markdown or JSON.
9. CLI writes output to stdout or an explicit output file.
10. CLI returns an exit code based on parse errors and optionally finding severity.

No step performs network access, telemetry, uploads, or runtime execution of scanned commands.

## Contracts

### CLI Contract

Interface:

```bash
mcp-audit scan [--config PATH] [--format markdown|json] [--output PATH] [--fail-on high|medium|low|never]
mcp-audit explain RULE_ID
```

Default discovery candidates:

```text
mcp.json
.mcp.json
.cursor/mcp.json
.vscode/mcp.json
```

Discovery is bounded to these paths and does not recursively scan repositories.

Initial defaults:

```text
--format markdown
--fail-on never
```

Exit codes:

| Code | Meaning |
|---|---|
| 0 | Scan completed and `--fail-on` threshold was not met. |
| 1 | Scan completed and `--fail-on` threshold was met. |
| 2 | User input error, unsupported format, missing file, or parse error. |
| 3 | Unexpected internal error. |

### Finding Model

Interface:

```text
Finding
- rule_id: string
- title: string
- description: string
- severity: high | medium | low
- category: secret | command | supply-chain | filesystem | network | ci | documentation
- file_path: string
- config_path: string
- evidence: string
- redacted_evidence: string
- remediation: string
- confidence: high | medium | low
```

Rules must not return raw secret values as `redacted_evidence`.

### JSON Report Contract

Response:

```json
{
  "schema_version": "0.1",
  "tool": {
    "name": "mcp-audit",
    "version": "0.1.0"
  },
  "summary": {
    "files_scanned": 1,
    "findings_total": 4,
    "findings_by_severity": {
      "high": 4,
      "medium": 0,
      "low": 0
    }
  },
  "files": [
    {
      "path": "mcp-audit/examples/high-risk-mcp.json",
      "parser": "json",
      "status": "scanned"
    }
  ],
  "findings": [
    {
      "rule_id": "XONE001",
      "title": "Literal secret appears in configuration",
      "description": "Configuration appears to contain a literal token, API key, or credential.",
      "severity": "high",
      "category": "secret",
      "file_path": "mcp-audit/examples/high-risk-mcp.json",
      "config_path": "$.mcpServers.shell.env.GITHUB_TOKEN",
      "evidence": "literal value matched GitHub token pattern",
      "redacted_evidence": "ghp_********",
      "remediation": "Move the token to a secret manager or environment variable reference.",
      "confidence": "high"
    }
  ],
  "errors": []
}
```

JSON output is the automation contract. Required keys must not be removed without a schema version change.

### Markdown Report Contract

Markdown reports must include:

```text
- title
- scan summary
- scanned files
- findings grouped or listed with severity
- rule ID
- why it matters
- affected file
- config path
- redacted evidence
- remediation
- errors if present
```

Markdown output is the human review contract. It should be readable without ANSI color.

### Rule Contract

Interface:

```text
Rule
- id: stable rule ID
- title: short finding title
- category: rule category
- default_severity: severity
- description: why this matters
- remediation: default remediation
- evaluate(document) -> list[Finding]
```

Rules must be deterministic and side-effect free.

### Parser Error Contract

Errors:

```text
ParseError
- file_path
- parser
- message
- line
- column
```

Parse errors should be rendered in both Markdown and JSON when scan can continue. If the explicit target config cannot be parsed, CLI returns exit code 2.

## Dependencies

Recommended v0.1 dependencies:

```text
- Python 3.11+
- Standard library `argparse` for CLI
- Standard library `json` for JSON parsing
- Standard library `pathlib` for path handling
- Standard library `dataclasses` or typed classes for models
- pytest for tests
```

Do not add YAML parsing dependency until a supported v0.1 config path requires it. If needed, prefer a widely used parser and record the dependency decision.

Do not add network, telemetry, analytics, or remote scanning dependencies.

## Non-Functional Requirements

- Performance: explicit config scans should complete under 2 seconds for normal config sizes. Discovery must use bounded candidate paths rather than broad repository crawling.
- Reliability: same inputs and version produce the same report ordering and findings.
- Security and privacy: no hidden network calls, uploads, telemetry, or raw secret disclosure in human-readable output.
- Compatibility: v0.1 targets macOS and Linux. Windows is unverified until fixture and path tests exist.
- Observability: no telemetry. Optional verbose local logs may be added later through a CLI flag.
- Maintainability: each rule must be independently testable and documented.

## Operability And Release

- Migration or backfill: not applicable for v0.1; no persistent state.
- Feature flag or rollout: not applicable for local CLI. Experimental rules can be disabled by default if needed.
- Logs, metrics, traces, or alerts: not applicable for v0.1. CLI errors and optional verbose output are enough.
- Rollback: users can pin or downgrade the package version once packaging exists. JSON schema changes require `schema_version` updates.
- Release notes: every release must list new rules, severity changes, schema changes, and known limitations.

## Risks

| Risk | Severity | Likelihood | Mitigation | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| Secret detection exposes sensitive values in output. | high | medium | Redaction module is mandatory for Markdown; tests cover common token patterns. | Security / Developer | open |
| Rules produce noisy false positives. | high | medium | Add negative fixtures and confidence levels; avoid blocking defaults in v0.1. | Product / QA | open |
| Config discovery scans too broadly. | medium | low | Use bounded candidate paths and explicit `--config` support. | Architect | mitigated |
| Users expect runtime enforcement. | medium | medium | Keep README and reports clear that this is audit-only in v0.1. | Product | mitigated |
| YAML support becomes necessary. | medium | medium | Keep parser boundary ready; add dependency only after validated need. | Architect | open |
| JSON schema changes break early automation. | medium | low | Version schema and add contract tests. | Architect / QA | open |
| CI checks expand scope before CLI is mature. | medium | medium | Treat CI scanning as `could` requirement after CLI report contract is stable. | Product | open |

## Alternatives Considered

- TypeScript CLI: rejected for v0.1 because Python with stdlib parsing is sufficient for local audit and keeps implementation smaller. Revisit if Node package distribution becomes the dominant adoption path.
- Full runtime gateway: rejected because v0.1 must remain static audit and production-usable without overclaiming enforcement.
- Hosted dashboard: rejected because local-first privacy and small scope are core constraints.
- OpenTelemetry-first architecture: rejected for v0.1 because report contracts and static findings matter more than telemetry integration.
- YAML-first support: rejected until a validated v0.1 config source requires YAML.

## Architecture Decisions

- ADR needed: yes
- Decision: v0.1 uses a Python CLI with explicit module boundaries for discovery, parsing, rule evaluation, redaction, reporting, and CLI presentation.
- Decision: v0.1 supports JSON parsing first and keeps YAML as an extension point.
- Decision: v0.1 report contracts are Markdown for humans and JSON for automation.
- Decision: v0.1 is audit-only and local-first.
- Consequences: implementation can be small and testable; package distribution may need revisiting if early users strongly prefer Node-based installation; runtime enforcement remains out of scope.

## Handoff Package

- `from_role`: Architect
- `to_role`: Expert Reviewer / QA Engineer
- `handoff_reason`: Review security boundaries, rule-risk semantics, report contracts, and test strategy before implementation planning.
- `input_context`: PRD requires a production-usable local CLI for MCP / agent config risk auditing. The project must reference OPT without modifying it and keep project-specific operating context under `mcp-audit/ops/`.
- `decisions_already_made`: Python CLI, JSON-first parsing, local-first audit-only v0.1, Markdown and JSON report contracts, modular rule engine, no network calls or telemetry.
- `open_questions`: whether YAML is required for v0.1; whether CI workflow scanning stays out of v0.1; packaging and installation strategy.
- `expected_output`: expert review findings and QA plan covering security claims, secret redaction, false positives, report contracts, parser errors, and fixture matrix.
- `acceptance_criteria`: reviewers can confirm the architecture satisfies PRD acceptance criteria and developers can create an implementation plan without guessing module boundaries or contracts.
- `risk_notes`: secret redaction, false-positive noise, security overclaiming, schema stability, and accidental scope expansion require close review.
