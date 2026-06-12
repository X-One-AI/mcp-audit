# Changelog

All notable changes to `mcp-audit` are recorded here.

## Unreleased

### Added

- Nothing yet.

## 0.4.1 - 2026-06-13

### Fixed

- Added MIT license metadata and README package metadata for cleaner PyPI/Homebrew distribution.

## 0.4.0 - 2026-06-13

### Added

- `mcp-audit discover` previews supported config paths without scanning files.
- `mcp-audit doctor` now recommends the next onboarding command.
- Rule explanations now include acceptance and policy exception guidance.
- Team adoption playbook for CI gates, baseline review, exceptions, and rollout stages.
- Homebrew tap packaging guidance for the official X-One tap.

### Changed

- README install guidance now treats PyPI as the default user install path.

## 0.3.1 - 2026-06-13

### Changed

- Renamed the Python distribution package to `xone-mcp-audit` because TestPyPI rejects `mcp-audit` as too similar to an existing project.
- Kept the CLI command as `mcp-audit` and the Python import package as `mcp_audit`.

## 0.3.0 - 2026-06-12

### Added

- Enforced team policy checks for profiles, required rules, blocked rules, global config paths, baseline review files, policy exceptions, and maximum unsuppressed severity.
- `mcp-audit policy check` for CI-friendly team policy validation.
- `mcp-audit scan --policy ...` enforcement mode.
- Reviewed baseline hash generation with `mcp-audit baseline --review-output ...`.
- Time-bounded policy exception files for approved finding fingerprints.
- Guided team setup with `mcp-audit init --wizard`.
- False-negative issue template and stable feedback triage workflow.

### Changed

- Version advanced to `0.3.0` for the stable production hardening release.
- Team policy documentation now describes active enforcement instead of a draft-only schema.

## 0.2.0 - 2026-06-12

### Added

- Sanitized real-world corpus fixtures with source manifest.
- Internal GitHub URL to sanitized fixture workflow.
- Twelve-sample real-world corpus v2 with source matrix and rule-tuning findings.
- Client-format fixtures for Claude-style config, Windsurf, Zed, Gemini/Qwen-style settings, and project-local MCP configs.
- Rules for broad tool enablement, unpinned container images, and sensitive container environment passthrough.
- Rule profiles: `starter`, `balanced`, and `team`.
- `mcp-audit init --profile ...` and `mcp-audit scan --profile ...`.
- Distribution and team policy roadmap for PyPI, Homebrew, configuration guidance, profiles, and team adoption.
- PyPI/TestPyPI Trusted Publishing workflow.
- Team policy schema draft and parser.
- Public sample review workflow as a substitute for unavailable real-user configuration reviews.

### Changed

- Unpinned remote package detection now scans nested `mcpServers` and Zed-style `context_servers`.
- Unpinned remote package detection now treats `bunx` like other remote package runners.
- Floating package versions such as `@latest` are treated as unpinned.
- Broad filesystem detection now treats `${HOME}` as broad access.
- Secret detection ignores CLI option names such as `--api-key`.
- Documentation placeholders such as `<your-api-key>` remain outside literal-secret findings.
- Cline global settings are documented as explicit `--config` scans rather than default discovery targets.

## 0.1.0 - 2026-06-12

### Added

- Local MCP / agent config scanning.
- Markdown, JSON, and SARIF reports.
- Rule explanations and rule listing.
- Diagnostic `doctor` command.
- Stable finding fingerprints.
- Baseline creation and suppression for reviewed accepted findings.
- Project configuration with `.mcp-audit.toml` and `mcp-audit init`.
- YAML and TOML config scanning.
- Additional high-signal rules for broad environment exposure and dangerous container options.
- Package build verification in CI.
- Package artifact upload from CI.
- False-positive feedback template and rule tuning workflow.
- English and Simplified Chinese README files.
- GitHub Actions CI for install, tests, and CLI smoke checks.

### Security

- Reports redact literal secret-like values.
- Scanning is local-first and does not execute scanned commands.
