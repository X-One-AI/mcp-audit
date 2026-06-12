# mcp-audit Next Phase OPT Plan

## 1. Product Manager

### Problem

`mcp-audit v0.1.0` is usable, but the next maturity gap is real-world fit: users will bring different client config shapes, documentation placeholders, nested agent configs, and noisy findings. The product needs broader fixture coverage and a tuning loop before broader package-channel distribution.

### Goals

- Build a sanitized real-world corpus with source traceability.
- Add client-format fixtures for more MCP and agent clients.
- Reduce known false positives without hiding high-risk behavior.
- Introduce rule profiles so first-time users and teams can adopt different strictness levels.
- Define PyPI, Homebrew, setup, and team policy sequencing.

### Non-Goals

- Do not publish to PyPI or Homebrew in this phase.
- Do not scan user home directories by default.
- Do not add a hosted service or dashboard.
- Do not weaken rule semantics merely to reduce noise.

### Requirements

| ID | Requirement | Acceptance |
| --- | --- | --- |
| PH2-001 | Sanitized real-world corpus | Corpus fixtures scan and manifest records public source URLs |
| PH2-002 | More client fixtures | Claude, Windsurf, Zed, Gemini/Qwen-style, and project-local MCP fixtures pass |
| PH2-003 | False-positive tuning | Placeholder API keys are not literal secrets; local node entrypoints are not remote package findings |
| PH2-004 | False-negative tuning | `@latest` and unversioned `npx`/`uvx` package launches are flagged |
| PH2-005 | Nested config scanning | Nested `mcpServers` and Zed `context_servers` are evaluated |
| PH2-006 | Rule profiles | `starter`, `balanced`, and `team` profiles are implemented and documented |
| PH2-007 | Configuration guidance | `init --profile` creates reviewable `.mcp-audit.toml` defaults |
| PH2-008 | Distribution roadmap | PyPI/Homebrew plan is documented with current official guidance links |

## 2. Architect

### Boundaries

- `rules/registry.py`: owns profile membership.
- `rules/commands.py`: owns package execution boundary detection.
- `project_config.py`: owns generated profile defaults.
- `config_discovery.py`: owns bounded project-local discovery.
- `tests/fixtures/real-world-corpus`: sanitized source-derived behavior corpus.
- `tests/fixtures/client-formats`: client shape compatibility fixtures.
- `docs/distribution-and-team-policy.md`: package and team policy roadmap.

### Data Flow

```text
CLI / project config profile
  -> registry filters enabled rules
  -> parser normalizes JSON/YAML/TOML object data
  -> rules scan direct and nested server maps
  -> reports keep stable rule IDs and fingerprints
```

### Risk Controls

| Risk | Mitigation |
| --- | --- |
| Public samples introduce copied secrets or license ambiguity | Keep sanitized minimal fixtures and source manifest only |
| Profiles hide important risks | Keep `balanced` as default; only exclude noisy medium rule from `starter` |
| Team defaults surprise users | Require explicit `init --profile team` |
| Package-channel work distracts from product fit | Document PyPI/Homebrew gates, do not publish yet |

## 3. QA Engineer

### Test Matrix

| Requirement | Evidence |
| --- | --- |
| PH2-001 | `tests/test_real_world_corpus.py` |
| PH2-002 | `tests/test_client_fixtures.py` |
| PH2-003 | `tests/test_real_world_corpus.py` |
| PH2-004 | `tests/test_real_world_corpus.py`, existing rule coverage |
| PH2-005 | `tests/test_real_world_corpus.py` |
| PH2-006 | `tests/test_rule_profiles.py` |
| PH2-007 | `tests/test_rule_profiles.py`, `tests/test_project_config.py` |
| PH2-008 | docs review and release docs |

## 4. Developer Plan

### Batch A: Corpus And Boundaries

- Add sanitized corpus with manifest.
- Add tests for placeholder secrets, `@latest`, nested `mcpServers`, Zed `context_servers`, and local node entrypoint boundaries.
- Update remote package rule traversal and version parsing.

### Batch B: Profiles And Config Guidance

- Add profile filtering to rule registry.
- Add `scan --profile`, `rules --profile`, and `init --profile`.
- Persist profile in `.mcp-audit.toml`.

### Batch C: Client Fixtures And Docs

- Add client-format fixtures.
- Expand bounded discovery paths.
- Update README, rules docs, QA plan, changelog, and distribution roadmap.

## 5. Completion Gate

- Local full test suite passes.
- Markdown fences and diff whitespace checks pass.
- No raw secrets are introduced in fixtures.
- Work is committed locally.
- Do not push to GitHub unless explicitly approved after this phase.
