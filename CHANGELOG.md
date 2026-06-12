# Changelog

All notable changes to `mcp-audit` are recorded here.

## Unreleased

### Added

- Sanitized real-world corpus fixtures with source manifest.
- Twelve-sample real-world corpus v2 with source matrix and rule-tuning findings.
- Client-format fixtures for Claude-style config, Windsurf, Zed, Gemini/Qwen-style settings, and project-local MCP configs.
- Rule profiles: `starter`, `balanced`, and `team`.
- `mcp-audit init --profile ...` and `mcp-audit scan --profile ...`.
- Distribution and team policy roadmap for PyPI, Homebrew, configuration guidance, profiles, and team adoption.

### Changed

- Unpinned remote package detection now scans nested `mcpServers` and Zed-style `context_servers`.
- Unpinned remote package detection now treats `bunx` like other remote package runners.
- Floating package versions such as `@latest` are treated as unpinned.
- Broad filesystem detection now treats `${HOME}` as broad access.
- Secret detection ignores CLI option names such as `--api-key`.
- Documentation placeholders such as `<your-api-key>` remain outside literal-secret findings.

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
