# Changelog

All notable changes to `mcp-audit` are recorded here.

## 0.1.0 - Unreleased

### Added

- Local MCP / agent config scanning.
- Markdown, JSON, and SARIF reports.
- Rule explanations and rule listing.
- Diagnostic `doctor` command.
- Stable finding fingerprints.
- Baseline creation and suppression for reviewed accepted findings.
- Project configuration with `.mcp-audit.toml` and `mcp-audit init`.
- English and Simplified Chinese README files.
- GitHub Actions CI for install, tests, and CLI smoke checks.

### Security

- Reports redact literal secret-like values.
- Scanning is local-first and does not execute scanned commands.
