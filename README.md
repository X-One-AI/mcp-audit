# mcp-audit

[![CI](https://github.com/X-One-AI/mcp-audit/actions/workflows/ci.yml/badge.svg)](https://github.com/X-One-AI/mcp-audit/actions/workflows/ci.yml)

Languages: English | [中文](./README.zh-CN.md)

Scan MCP and AI agent configurations for risky permissions, secrets, unsafe commands, and CI safety gaps.

## Purpose

`mcp-audit` is the first active X-One project.

It helps teams review the safety of MCP tools and AI agent workflows before those agents touch repositories, terminals, credentials, CI jobs, or internal systems.

## Positioning

```text
Agentic DevSecOps / Safe Agent Operations
```

`mcp-audit` is not a runtime sandbox and does not claim to block every attack. The first version is a local-first auditor that produces actionable, easy-to-review risk reports.

## Target Users

```text
- Developers using MCP tools
- Teams adopting AI coding agents
- DevTools and platform engineers
- DevSecOps and security platform teams
- Founders who want AI agents in their engineering workflow without blind trust
```

## MVP Scope

The first version should do four things well:

```text
1. Read MCP / agent configuration files
2. Detect high-signal risks
3. Generate Markdown and JSON reports
4. Explain each rule with concrete remediation
```

## First Rule Areas

```text
- Secret exposure
- Unsafe shell / exec / eval usage
- Unpinned remote package execution
- Excessive filesystem access
- Unrestricted network access
- Broad environment exposure
- Dangerous container options
- Broad tool enablement
- Unpinned container images
- Sensitive container environment passthrough
- CI and PR safety gaps
```

## Example CLI

```bash
mcp-audit doctor
mcp-audit discover
mcp-audit init
mcp-audit init --profile team
mcp-audit init --wizard --profile team
mcp-audit scan
mcp-audit scan --config ./mcp.json
mcp-audit scan --config ./agent.yaml
mcp-audit scan --config ./agent.toml
mcp-audit scan --profile starter
mcp-audit scan --format markdown
mcp-audit scan --format json
mcp-audit scan --format sarif --output mcp-audit.sarif
mcp-audit scan --fail-on high
mcp-audit baseline --config ./mcp.json --output .mcp-audit-baseline.json
mcp-audit scan --config ./mcp.json --baseline .mcp-audit-baseline.json --fail-on high
mcp-audit baseline --config ./mcp.json --baseline .mcp-audit-baseline.json --prune --output .mcp-audit-baseline.json
mcp-audit policy check --policy .mcp-audit-policy.toml --profile team
mcp-audit scan --config ./mcp.json --profile team --policy .mcp-audit-policy.toml
mcp-audit rules
mcp-audit explain XONE001
```

## Install

From PyPI:

```bash
python3 -m pip install xone-mcp-audit
mcp-audit --version
```

The Python distribution package is `xone-mcp-audit`; the installed CLI remains `mcp-audit`.

From this repository for local development:

```bash
python3 -m pip install -e .
mcp-audit --version
```

From a GitHub release artifact:

```bash
python3 -m pip install https://github.com/X-One-AI/mcp-audit/releases/download/v0.3.1/xone_mcp_audit-0.3.1-py3-none-any.whl
mcp-audit --version
```

PyPI and TestPyPI publishing use Trusted Publishing through GitHub Actions.

If your Python environment cannot fetch build dependencies because of network or certificate restrictions, use the local development commands below until packaging dependencies are available.

Without `--config`, `scan` checks only bounded default locations:

```text
mcp.json
.mcp.json
mcp.yaml
mcp.yml
agent.yaml
agent.yml
agent.toml
.cursor/mcp.json
.vscode/mcp.json
.claude/mcp.json
.claude/claude_desktop_config.json
.continue/config.json
.continue/config.yaml
.windsurf/mcp_config.json
.gemini/settings.json
.qwen/settings.json
.factory/mcp.json
.factory/settings.json
.zed/settings.json
```

It does not recursively scan the repository. Explicit `--config` supports JSON, YAML, and TOML object configs.

## Project Configuration

Create a project configuration:

```bash
mcp-audit init
```

This writes `.mcp-audit.toml`:

```toml
[scan]
profile = "balanced"
fail_on = "high"
baseline = ".mcp-audit-baseline.json"
```

Use `mcp-audit init --profile starter` for a quieter first run, or `mcp-audit init --profile team` when CI should fail on medium or higher findings.
Explicit CLI flags override project configuration.
Use `mcp-audit doctor` to inspect whether the config file is detected and which scan defaults are effective.

For a guided team setup:

```bash
mcp-audit init --wizard --profile team
mcp-audit policy check --policy .mcp-audit-policy.toml --profile team
```

The wizard writes `.mcp-audit.toml` and `.mcp-audit-policy.toml` with enforced team defaults.

## Rule Profiles

```text
starter  - high-signal rules only; excludes medium network/tool/env passthrough heuristics
balanced - default profile for individual repositories
team     - same rule set as balanced, with stricter generated config defaults
```

## Client Notes

Global client settings are not scanned by default. Scan them explicitly when you want to audit a user-level client config:

```bash
mcp-audit scan --config ~/.cline/data/settings/cline_mcp_settings.json
```

## Local Development

From this directory:

```bash
python3 -m pip install -e ".[dev]"
python3 -m pytest tests -q
PYTHONPATH=src python3 -m mcp_audit.cli --version
PYTHONPATH=src python3 -m mcp_audit --version
PYTHONPATH=src python3 -m mcp_audit.cli doctor
PYTHONPATH=src python3 -m mcp_audit.cli init
PYTHONPATH=src python3 -m mcp_audit.cli scan --config examples/high-risk-mcp.json --format markdown
PYTHONPATH=src python3 -m mcp_audit.cli scan --config examples/high-risk-mcp.json --format json
PYTHONPATH=src python3 -m mcp_audit.cli scan --config examples/high-risk-mcp.json --format sarif
PYTHONPATH=src python3 -m mcp_audit.cli rules
```

Use `scan` without `--config` only in a repository that contains one of the bounded default config paths.

The CLI is local-first. It does not upload configs, send telemetry, or execute scanned commands.

For CI, start with:

```bash
mcp-audit scan --config ./mcp.json --format sarif --output mcp-audit.sarif --fail-on high
```

For existing repositories with accepted findings, create a reviewed baseline:

```bash
mcp-audit baseline --config ./mcp.json --output .mcp-audit-baseline.json \
  --review-output .mcp-audit-baseline.review.toml \
  --approved-by security-team \
  --reason "accepted known MCP risks"
mcp-audit scan --config ./mcp.json --profile team \
  --baseline .mcp-audit-baseline.json \
  --baseline-review .mcp-audit-baseline.review.toml \
  --policy .mcp-audit-policy.toml
```

Treat baseline updates as code-review events. A baseline is an acceptance record, not proof that the finding is safe.
When a baseline suppresses findings, reports still show the suppressed finding count in the summary.
To remove accepted findings that no longer appear, prune the baseline:

```bash
mcp-audit baseline --config ./mcp.json --baseline .mcp-audit-baseline.json --prune --output .mcp-audit-baseline.json
```

Markdown is intended for human review. JSON and SARIF are intended for automation.

## Non-Goals

```text
- No runtime sandboxing
- No dashboard
- No hosted service
- No claim that the tool prevents all MCP or agent security issues
```

## First Milestone

```text
v0.1: scan example MCP / agent configs and generate a useful local risk report.
```

Success means at least three real users are willing to scan their own MCP or agent configuration and discuss the result.

## Related Docs

- [Operating Model](./ops/README.md)
- [Rules Draft](./docs/rules.md)
- [Real-World Sample Matrix](./docs/real-world-sample-matrix.md)
- [Release Checklist](./docs/release-checklist.md)
- [Rule Tuning And False Positive Workflow](./docs/rule-tuning.md)
- [Rule Tuning Findings](./docs/rule-tuning-findings.md)
- [Distribution And Team Policy Roadmap](./docs/distribution-and-team-policy.md)
- [Team Policy Schema](./docs/team-policy-schema.md)
- [Team Adoption Playbook](./docs/team-adoption-playbook.md)
- [Homebrew Packaging](./docs/homebrew.md)
- [Publishing](./docs/publishing.md)
- [Example High-Risk Config](./examples/high-risk-mcp.json)
