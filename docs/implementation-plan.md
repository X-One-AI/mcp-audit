# mcp-audit v0.1 Implementation Plan

## Goal

Build the first production-usable `mcp-audit` CLI that scans explicit JSON MCP / agent configuration files, detects high-signal risk findings, and renders local Markdown and JSON reports with secret-safe human-readable output.

## Files And Ownership

- Create:
  - `mcp-audit/pyproject.toml`: package metadata, Python version, pytest config, console script.
  - `mcp-audit/src/mcp_audit/__init__.py`: package version export.
  - `mcp-audit/src/mcp_audit/model.py`: shared dataclasses and enums.
  - `mcp-audit/src/mcp_audit/errors.py`: parse and scan errors.
  - `mcp-audit/src/mcp_audit/parsers/__init__.py`: parser package.
  - `mcp-audit/src/mcp_audit/parsers/json_parser.py`: JSON config parser.
  - `mcp-audit/src/mcp_audit/rules/__init__.py`: rules package.
  - `mcp-audit/src/mcp_audit/rules/base.py`: rule interface.
  - `mcp-audit/src/mcp_audit/rules/secrets.py`: literal secret detection.
  - `mcp-audit/src/mcp_audit/rules/commands.py`: shell, exec, eval, unpinned command detection.
  - `mcp-audit/src/mcp_audit/rules/filesystem.py`: broad filesystem access detection.
  - `mcp-audit/src/mcp_audit/rules/network.py`: broad network access detection.
  - `mcp-audit/src/mcp_audit/rules/registry.py`: rule registry and explain data.
  - `mcp-audit/src/mcp_audit/redaction.py`: sensitive value masking.
  - `mcp-audit/src/mcp_audit/renderers/__init__.py`: renderer package.
  - `mcp-audit/src/mcp_audit/renderers/json_report.py`: JSON report renderer.
  - `mcp-audit/src/mcp_audit/renderers/markdown_report.py`: Markdown report renderer.
  - `mcp-audit/src/mcp_audit/config_discovery.py`: explicit config and bounded discovery.
  - `mcp-audit/src/mcp_audit/app.py`: scan orchestration.
  - `mcp-audit/src/mcp_audit/cli.py`: CLI entrypoint.
  - `mcp-audit/tests/fixtures/`: positive and negative fixture files.
  - `mcp-audit/tests/test_*.py`: unit, contract, integration, and CLI tests.
- Modify:
  - `mcp-audit/README.md`: add install/run snippet only after CLI exists.
  - `mcp-audit/docs/rules.md`: keep in sync with implemented rules and severities.
  - `mcp-audit/ops/decisions/`: add ADRs if dependencies, schema, or rule severity semantics change.
- Test:
  - `mcp-audit/tests/test_json_parser.py`
  - `mcp-audit/tests/test_rules_secrets.py`
  - `mcp-audit/tests/test_rules_commands.py`
  - `mcp-audit/tests/test_rules_filesystem.py`
  - `mcp-audit/tests/test_rules_network.py`
  - `mcp-audit/tests/test_redaction.py`
  - `mcp-audit/tests/test_json_report.py`
  - `mcp-audit/tests/test_markdown_report.py`
  - `mcp-audit/tests/test_cli.py`
  - `mcp-audit/tests/test_rule_coverage.py`

## Steps

1. Create Python package skeleton with `pyproject.toml`, package directory, console script, and pytest configuration.
2. Add shared models for severity, confidence, category, scanned file, finding, report summary, report, and parse errors.
3. Add JSON parser that returns normalized config documents and structured parse errors.
4. Add initial fixtures:
   - high-risk config
   - safe config
   - invalid JSON config
   - narrow filesystem config
   - safe environment variable reference config
5. Implement redaction helpers for GitHub-token-like values, generic API keys, bearer tokens, and long secret-like strings.
6. Implement rule interface and rule registry.
7. Implement `XONE001` literal secret rule with positive and negative tests.
8. Implement command and supply-chain rules for shell launch, `curl | sh`, and unpinned `npx` / `uvx` usage.
9. Implement filesystem rule for broad home/root/workspace exposure and narrow-path negative cases.
10. Implement network rule only for explicit broad network evidence in config; keep severity medium by default.
11. Implement JSON renderer and contract tests for required top-level keys and finding keys.
12. Implement Markdown renderer and contract tests for summary, finding sections, remediation, redacted evidence, and limitations.
13. Implement scan orchestration in `app.py`.
14. Implement CLI scan command with optional `--config`, bounded default discovery, `--format`, `--output`, and `--fail-on`.
15. Implement `explain RULE_ID`.
16. Add CLI integration tests for success, parse error, unknown rule, version output, JSON output, Markdown output, and fail threshold.
17. Add rule coverage meta-test requiring positive and negative fixtures for every registered rule.
18. Update `docs/rules.md` to match implemented rule IDs, severity, and remediation.
19. Update `README.md` with a minimal install/run section after CLI behavior is verified.
20. Run full verification and record any residual risks in release notes or docs.

## Reuse Strategy

- Reuse existing project docs:
  - `mcp-audit/docs/prd.md`
  - `mcp-audit/docs/architecture.md`
  - `mcp-audit/docs/expert-review-security.md`
  - `mcp-audit/docs/qa-plan.md`
  - `mcp-audit/ops/constraints/production.md`
  - `mcp-audit/ops/constraints/main-entry.md`
- Reuse the existing high-risk example:
  - `mcp-audit/examples/high-risk-mcp.json`
- Use Python standard library for v0.1 CLI and JSON parsing to keep dependency surface small.
- Use `pytest` for tests.
- Do not introduce YAML, network, telemetry, or hosted-service dependencies in v0.1.

## Traceability

| Requirement | Implementation area | Test coverage |
|---|---|---|
| REQ-001 | `cli.py`, `app.py`, `config_discovery.py` | `tests/test_cli.py` |
| REQ-002 | `config_discovery.py` | `tests/test_config_discovery.py` |
| REQ-003 | `parsers/json_parser.py` | `tests/test_json_parser.py` |
| REQ-005 | `rules/secrets.py`, `redaction.py` | `tests/test_rules_secrets.py`, `tests/test_redaction.py` |
| REQ-006 | `rules/commands.py` | `tests/test_rules_commands.py` |
| REQ-007 | `rules/commands.py` | `tests/test_rules_commands.py` |
| REQ-008 | `rules/filesystem.py` | `tests/test_rules_filesystem.py` |
| REQ-009 | `rules/network.py` | `tests/test_rules_network.py` |
| REQ-011 | `renderers/markdown_report.py` | `tests/test_markdown_report.py` |
| REQ-012 | `renderers/json_report.py` | `tests/test_json_report.py` |
| REQ-013 | `rules/registry.py`, `model.py` | `tests/test_rule_coverage.py` |
| REQ-014 | `cli.py`, `rules/registry.py` | `tests/test_cli.py` |
| REQ-015 | `redaction.py`, `renderers/markdown_report.py` | `tests/test_redaction.py`, `tests/test_markdown_report.py` |
| REQ-016 | `model.py`, renderers | report contract tests |
| REQ-017 | package module boundaries | code review |
| REQ-018 | `tests/fixtures/`, meta-test | `tests/test_rule_coverage.py` |
| REQ-019 | renderers | `tests/test_json_report.py`, `tests/test_markdown_report.py` |
| REQ-020 | `README.md`, `ops/README.md` | docs review |
| REQ-021 | `ops/` docs | docs review |
| REQ-022 | external OPT untouched | manual/VCS check |
| REQ-024 | scan path code | code review and dependency audit |
| REQ-025 | CLI/report/docs wording | expert review and docs review |

## Test Strategy

- Unit:
  - parser behavior
  - rule behavior
  - redaction
  - config path helpers
- Integration:
  - scan explicit config file through `app.py`
  - CLI scan command
  - CLI explain command
- Contract:
  - JSON report required keys and finding fields, including finding descriptions
  - Markdown report required sections, including scanned files and why-it-matters text
  - CLI exit codes
- E2E:
  - high-risk config to Markdown report
  - high-risk config to JSON report
  - safe config to no high-risk findings
  - invalid JSON to parse error exit code
- Manual:
  - README remains concise
  - security wording avoids overclaims
  - no OPT source edits
  - no network/telemetry dependencies
- Test data:
  - fake token-like values only
  - no real secrets
  - fixture names clearly indicate expected behavior

## Verification

Commands:

```bash
cd mcp-audit
python -m pytest tests -q
python -m json.tool examples/high-risk-mcp.json
PYTHONPATH=src python -m mcp_audit.cli --version
PYTHONPATH=src python -m mcp_audit.cli scan --config examples/high-risk-mcp.json --format json
PYTHONPATH=src python -m mcp_audit.cli scan --config examples/high-risk-mcp.json --format markdown
PYTHONPATH=src python -m mcp_audit.cli explain XONE001
```

Expected result:

```text
- tests pass
- example JSON validates
- JSON scan emits valid report with findings
- Markdown scan emits readable report with redacted secrets
- explain command returns rule rationale and remediation
```

## Release Plan

- Deployment: local CLI package only.
- Migration: not applicable for v0.1.
- Feature flag or rollout: not applicable; default `--fail-on never`.
- Observability: no telemetry; optional local verbose flag can be future work.
- CI or blocking checks:
  - run pytest
  - validate JSON fixture
  - review docs wording
  - verify no hidden network dependencies

## Rollback Or Compatibility Notes

- Report `schema_version` starts at `0.1`.
- Required JSON keys cannot be removed without schema version change.
- Rule IDs must remain stable once released.
- Early users can pin or downgrade package versions when packaging exists.
- YAML, GitHub Action, and runtime enforcement remain future decisions.

## Handoff Package

- `from_role`: Developer Planner
- `to_role`: Implementer
- `handoff_reason`: Execute v0.1 CLI implementation using TDD and the documented module boundaries.
- `input_context`: PRD, architecture, security expert review, and QA plan are complete under `mcp-audit/docs/`.
- `decisions_already_made`: Python CLI, JSON-first parsing, local-first audit-only behavior, Markdown/JSON report contracts, no telemetry/network, no runtime enforcement.
- `open_questions`: package distribution method after local CLI works; YAML support after user validation; CI workflow scanning after report contracts stabilize.
- `expected_output`: working CLI with tests, fixtures, docs updates, and verification evidence.
- `acceptance_criteria`: all PRD acceptance criteria and QA plan checks pass.
- `risk_notes`: secret redaction, false positives, overclaiming, schema stability, and scope creep require close review.
