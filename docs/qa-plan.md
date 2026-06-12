# mcp-audit QA Plan

## Acceptance Criteria Under Test

- `mcp-audit scan --config mcp-audit/examples/high-risk-mcp.json --format markdown` produces a Markdown report with high-risk findings for secret exposure, unpinned remote package execution, broad filesystem access, and unsafe shell execution.
- `mcp-audit scan --config mcp-audit/examples/high-risk-mcp.json --format json` produces valid JSON with stable keys for scanned files, findings, severities, rule IDs, evidence, and remediation.
- `mcp-audit scan --config ...` supports JSON, YAML, and TOML object configs.
- `mcp-audit scan --config mcp-audit/examples/high-risk-mcp.json --format sarif` produces SARIF 2.1.0 that CI and code scanning tools can consume.
- `mcp-audit doctor` explains runtime and bounded discovery state without scanning or making network calls.
- `mcp-audit baseline --config ... --output ...` writes stable finding fingerprints for reviewed accepted findings.
- `mcp-audit scan --baseline ...` suppresses only matching accepted fingerprints and still fails on new high findings when `--fail-on high` is used.
- Reports show the count of findings suppressed by baseline.
- `mcp-audit baseline --prune` removes accepted findings that no longer appear in the current scan.
- `mcp-audit init` writes `.mcp-audit.toml` with safe default scan policy.
- `mcp-audit init --profile ...` writes profile-specific defaults without requiring an interactive prompt.
- `mcp-audit scan --profile ...` changes enabled rules without changing rule IDs.
- `mcp-audit scan` uses `.mcp-audit.toml` defaults when explicit CLI flags are absent.
- Sanitized real-world corpus fixtures scan successfully and cover known false-positive boundaries.
- Sanitized real-world corpus v2 tracks twelve public samples with source traceability and rule-gap notes.
- Client-format fixtures cover Claude, Cursor-style MCP, Windsurf, Gemini/Qwen-style settings, and Zed `context_servers`.
- Broad tool enablement, unpinned container images, and sensitive container env passthrough are covered by positive and negative tests.
- Human-readable reports redact literal secret values while preserving useful evidence.
- Every v0.1 rule has at least one positive fixture and one negative fixture.
- JSON report contract tests fail on required key removal or rename.
- Markdown report tests fail when scanned files, rule ID, severity, why-it-matters text, evidence, remediation, or limitations are missing.
- CLI exits non-zero on parse errors and reports the file path and parse reason.
- CLI and report output make the next action clear enough for a reviewer to act without reading source code.
- CLI does not make network calls during scan.
- `mcp-audit/README.md` remains concise and routes deeper context to `mcp-audit/ops/README.md`.
- OPT source files outside this repository remain unmodified.

## Test Matrix

| Requirement ID | Scenario | Level | Expected result | Evidence |
| --- | --- | --- | --- | --- |
| REQ-001 | Scan explicit JSON config file. | integration | CLI reads provided file and returns report. | `tests/test_cli.py` |
| REQ-002 | Discover supported config files from bounded paths. | integration | CLI checks only documented candidate paths. | `tests/test_config_discovery.py` |
| REQ-003 | Parse valid JSON config. | unit | Parser returns normalized config document. | `tests/test_json_parser.py` |
| REQ-003A | Parse valid YAML config. | integration | CLI scans YAML object config and emits findings. | `tests/test_parsers_multi_format.py` |
| REQ-003B | Parse valid TOML config. | integration | CLI scans TOML object config and emits findings. | `tests/test_parsers_multi_format.py` |
| REQ-003 | Parse invalid JSON config. | unit | Parser returns structured parse error with file path and reason. | `tests/test_json_parser.py` |
| REQ-005 | Detect literal GitHub-token-like value. | unit | Rule emits `XONE001` high severity finding. | `tests/test_rules_secrets.py` |
| REQ-005 | Ignore safe environment variable reference. | unit | Rule does not flag `${GITHUB_TOKEN}` or equivalent reference as literal secret. | `tests/test_rules_secrets.py` |
| REQ-006 | Detect bash or sh shell launch. | unit | Rule emits high severity command finding. | `tests/test_rules_commands.py` |
| REQ-007 | Detect unpinned `npx -y package` launch. | unit | Rule emits supply-chain finding. | `tests/test_rules_commands.py` |
| REQ-008 | Detect broad `/Users/example` filesystem path. | unit | Rule emits filesystem finding. | `tests/test_rules_filesystem.py` |
| REQ-008 | Allow narrow project-relative path. | unit | Rule does not emit broad filesystem finding. | `tests/test_rules_filesystem.py` |
| REQ-009 | Detect broad URL/network-enabled tool when config evidence exists. | unit | Rule emits medium network finding. | `tests/test_rules_network.py` |
| REQ-011 | Render Markdown report. | contract | Report includes title, summary, scanned files, rule ID, severity, why it matters, file path, evidence, remediation, and limitations. | `tests/test_markdown_report.py` |
| REQ-012 | Render JSON report. | contract | JSON contains stable top-level keys and finding fields. | `tests/test_json_report.py` |
| REQ-012A | Render SARIF report. | contract | SARIF contains tool metadata and one result per finding. | `tests/test_cli.py` |
| REQ-014 | Explain known rule. | integration | `mcp-audit explain XONE001` returns description and remediation. | `tests/test_cli.py` |
| REQ-014A | Baseline accepted findings. | integration | Baseline writes fingerprints and scan suppresses matching accepted findings. | `tests/test_baseline.py` |
| REQ-014B | Project configuration. | integration | Init writes config; scan reads baseline and fail-on defaults; explicit flags override config. | `tests/test_project_config.py` |
| REQ-014C | Rule profiles. | integration | Starter profile removes the medium network heuristic; team init writes stricter defaults. | `tests/test_rule_profiles.py` |
| REQ-014D | Real-world corpus. | integration | Sanitized public-sample-derived fixtures scan and preserve expected rule boundaries. | `tests/test_real_world_corpus.py` |
| REQ-014D2 | Twelve-sample corpus v2. | integration / docs | Public sample matrix, corpus v2 fixtures, and rule-tuning findings remain in sync. | `tests/test_real_world_corpus_v2.py` |
| REQ-014E | Client format fixtures. | integration | Client-shaped configs for Claude, Windsurf, Zed, Gemini/Qwen-style settings scan successfully. | `tests/test_client_fixtures.py` |
| REQ-014F | Broad tool enablement. | unit / integration | `enableAllTools`, `allowAllTools`, and wildcard tools emit `XONE008`. | `tests/test_rule_tool_enablement.py`, `tests/test_real_world_corpus_v2.py` |
| REQ-014G | Docker supply-chain. | unit / integration | Untagged and `latest` Docker images emit `XONE009`; tagged and digest-pinned images do not. | `tests/test_rule_docker.py`, `tests/test_real_world_corpus_v2.py` |
| REQ-014H | Docker env passthrough. | unit / integration | Sensitive env names passed through Docker emit `XONE010` without leaking values. | `tests/test_rule_docker.py`, `tests/test_real_world_corpus_v2.py` |
| REQ-015 | Redact secret in Markdown. | unit / contract | Raw literal token is absent from Markdown output. | `tests/test_redaction.py` |
| REQ-016 | Preserve useful redacted evidence. | unit / contract | Redacted output includes config path and masked token family. | `tests/test_redaction.py` |
| REQ-018 | Every rule has positive and negative fixtures. | meta-test | Test fails if any registered rule lacks fixture coverage. | `tests/test_rule_coverage.py` |
| REQ-019 | Report contracts are stable. | contract | Tests fail on required key or section removal. | `tests/test_json_report.py`, `tests/test_markdown_report.py` |
| REQ-020 | README stays concise. | docs | README links to operating model and avoids internal OPT details. | docs review |
| REQ-022 | OPT source remains unmodified. | manual / command | No changes under external OPT path. | `find` or VCS status outside repo |
| REQ-024 | No hidden network calls. | unit / code review | Scan path uses no networking libraries or subprocess network calls. | code review, dependency audit |
| REQ-025 | Security wording avoids overclaims. | docs / report | Docs and report output use risk-review language only. | docs review |
| UX-001 | Findings explain why they matter and what to do next. | contract / docs | Markdown and rule explanations include specific remediation. | `tests/test_markdown_report.py`, docs review |
| UX-002 | Errors are recoverable. | integration | Missing config and parse errors describe the action needed. | `tests/test_cli.py` |

## Test Data And Environment

- Data:
  - `mcp-audit/examples/high-risk-mcp.json`
  - `mcp-audit/tests/fixtures/real-world-corpus`
  - `mcp-audit/tests/fixtures/real-world-corpus-v2`
  - `mcp-audit/tests/fixtures/client-formats`
  - positive fixtures for secret, command, supply-chain, filesystem, and network rules
  - negative fixtures for safe env references, pinned commands, narrow paths, and benign configs
  - invalid JSON fixture for parse error handling
- Environment:
  - Python 3.11+
  - macOS and Linux for v0.1 validation
  - no network dependency during tests
- Fixtures or accounts:
  - no real credentials
  - fake token-like strings only
  - no external accounts required

## E2E Paths

- E2E-001: Run Markdown scan against high-risk config and verify expected high-risk findings and redaction.
- E2E-002: Run JSON scan against high-risk config and validate JSON contract.
- E2E-002A: Run SARIF scan against high-risk config and validate SARIF version, tool metadata, and rule IDs.
- E2E-002B: Run JSON scan against YAML and TOML high-risk configs.
- E2E-003: Run scan against safe config and verify no high-risk findings.
- E2E-004: Run scan against invalid JSON and verify exit code 2 with actionable parse error.
- E2E-005: Run `explain XONE001` and verify rule explanation and remediation.
- E2E-006: Run `mcp-audit --version` or `python -m mcp_audit.cli --version` and verify version output.
- E2E-007: Create a baseline from high-risk config, rescan with `--baseline`, and verify accepted findings are suppressed.
- E2E-007A: Verify JSON, Markdown, and SARIF report the suppressed finding count when a baseline suppresses findings.
- E2E-007B: Add a stale baseline fingerprint, run prune, and verify the stale entry is removed.
- E2E-008: Run `init`, inspect `.mcp-audit.toml`, then scan using project config defaults.
- E2E-009: Run `init --profile team`, inspect stricter generated defaults, and run `scan --profile starter` against a high-risk fixture.
- E2E-010: Run scans across sanitized real-world corpus fixtures and client-format fixtures.
- E2E-011: Run scans across the twelve-sample corpus v2 and review `docs/rule-tuning-findings.md` for expected gaps.
- E2E-012: Run scans against Docker and broad-tool corpus v2 fixtures and verify `XONE008`, `XONE009`, and `XONE010`.

## Contract Checks

- JSON report schema:
  - `schema_version`
  - `tool`
  - `summary`
  - `files`
  - `findings`
  - `errors`
- Finding schema:
  - `rule_id`
  - `title`
  - `description`
  - `severity`
  - `category`
  - `file_path`
  - `config_path`
  - `evidence`
  - `redacted_evidence`
  - `remediation`
  - `confidence`
- Markdown report sections:
  - title
  - summary
  - scanned files
  - findings
  - why it matters
  - redacted evidence
  - remediation
  - limitations
  - errors when present
- CLI exit codes:
  - `0` success without fail threshold
  - `0` version output
  - `1` findings meet `--fail-on`
  - `2` user input or parse error
  - `3` unexpected internal error
- User experience checks:
  - first useful command is visible in README
  - missing config error tells user to pass `--config`
  - findings include remediation
  - output avoids raw secret values
  - output avoids security guarantees
- SARIF report checks:
  - `version` is `2.1.0`
  - tool driver name and version are present
  - result rule IDs map to registered XONE rules
  - evidence remains redacted

## Regression Scope

- Stable rule IDs must not be renamed without migration notes.
- Profile membership must not change without changelog notes and fixture evidence.
- JSON report required keys must not be removed without schema version change.
- Markdown output must not expose raw secret-like values.
- Default scan behavior must remain local-first and non-networked.
- Default `--fail-on` must remain `never` for v0.1 unless Product and Security approve a change.
- README must stay focused on user onboarding and avoid internal process sprawl.

## CI And Blocking Checks

Before a release or completion claim:

```bash
python -m pytest mcp-audit/tests -q
python -m json.tool mcp-audit/examples/high-risk-mcp.json
```

Manual gates:

```text
- Security wording review for README, CLI messages, and reports
- Fixture coverage review for each registered rule
- No-network code review for scan path
- OPT source untouched check
```

## Not Tested

- Windows path behavior: not tested in v0.1 unless Windows fixture and environment are added.
- YAML configs: not tested until YAML support is included.
- Publishing to PyPI/Homebrew: planned but not executed in this phase.
- Runtime MCP server behavior: out of scope for static audit v0.1.
- Runtime sandboxing or enforcement: out of scope for v0.1.
- Hosted service behavior: out of scope.
- Full CI workflow safety: limited to future scope unless explicitly added after CLI MVP.

## Verification Report

- Command: run the commands listed in `mcp-audit/docs/implementation-plan.md#verification` before release or completion claims.
- Result: implementation exists; current verification evidence belongs in commit, PR, or release notes because command output changes over time.
- Evidence:
  - Screenshot or recording: not applicable.
  - Logs or test output: capture fresh output from the verification commands for each release candidate.
- Residual risk:
  - static auditing is incomplete by nature
  - secret detection remains heuristic
  - false positives require fixture-driven tuning
  - unsupported MCP/client config formats may limit early usefulness
