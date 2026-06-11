# mcp-audit

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
- CI and PR safety gaps
```

## Example CLI

```bash
mcp-audit doctor
mcp-audit scan
mcp-audit scan --config ./mcp.json
mcp-audit scan --format markdown
mcp-audit scan --format json
mcp-audit scan --format sarif --output mcp-audit.sarif
mcp-audit scan --fail-on high
mcp-audit explain XONE001
```

## Install

From this repository:

```bash
python3 -m pip install -e .
mcp-audit --version
```

If your Python environment cannot fetch build dependencies because of network or certificate restrictions, use the local development commands below until packaging dependencies are available.

Without `--config`, `scan` checks only bounded default locations:

```text
mcp.json
.mcp.json
.cursor/mcp.json
.vscode/mcp.json
```

It does not recursively scan the repository.

## Local Development

From this directory:

```bash
python3 -m pytest tests -q
PYTHONPATH=src python3 -m mcp_audit.cli --version
PYTHONPATH=src python3 -m mcp_audit.cli doctor
PYTHONPATH=src python3 -m mcp_audit.cli scan --config examples/high-risk-mcp.json --format markdown
PYTHONPATH=src python3 -m mcp_audit.cli scan --config examples/high-risk-mcp.json --format json
PYTHONPATH=src python3 -m mcp_audit.cli scan --config examples/high-risk-mcp.json --format sarif
```

Use `scan` without `--config` only in a repository that contains one of the bounded default config paths.

The CLI is local-first. It does not upload configs, send telemetry, or execute scanned commands.

For CI, start with:

```bash
mcp-audit scan --config ./mcp.json --format sarif --output mcp-audit.sarif --fail-on high
```

Markdown is intended for human review. JSON and SARIF are intended for automation.

## Non-Goals

```text
- No runtime policy enforcement in v0.1
- No dashboard in v0.1
- No hosted service in v0.1
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
- [Example High-Risk Config](./examples/high-risk-mcp.json)
