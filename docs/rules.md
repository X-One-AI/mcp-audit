# mcp-audit Rules Draft

This file defines the first rule set for `mcp-audit`.

Rule IDs use the `XONE` prefix until the project has a stable public naming convention.

## Severity Model

| Severity | Meaning |
|---|---|
| high | A reviewer should stop and inspect before using this config. |
| medium | The config may be acceptable, but needs an explicit reason or tighter policy. |
| low | Informational risk or missing documentation. |

## Implemented v0.1 Rules

| Rule | Severity | Category | Title | Finding |
|---|---|---|---|
| XONE001 | high | Secret exposure | Literal secret appears in configuration | Config appears to contain a literal API key, token, or credential. |
| XONE002 | high | Command execution | Unsafe command execution path | MCP server starts with shell, exec, eval, or equivalent unrestricted command execution. |
| XONE003 | high | Supply chain | Unpinned remote package execution | MCP server launches an unpinned remote package through npx, uvx, curl, or similar tooling. |
| XONE004 | high | Filesystem | Broad filesystem access | Filesystem access includes home, root, or broad workspace paths. |
| XONE005 | medium | Network | Broad network access | Tool allows broad outbound network access without host allowlist or explanation. |
| XONE006 | high | Secret exposure | Broad environment exposure | Tool receives the full process environment instead of explicit variables. |
| XONE007 | high | Command execution | Dangerous container option | Container launch uses privileged, host namespace, or host-root mount options. |

## Reserved Future Rule Areas

These are intentionally not implemented in the first CLI path:

| Area | Reason |
|---|---|
| CI safety | Requires supported workflow scanning and PR context. |
| GitHub token scopes | Requires more precise workflow and permission model parsing. |
| Documentation completeness | Lower signal than direct config risk in v0.1. |

## Remediation Style

Each rule should explain:

```text
- what was detected
- why it matters
- when it might be acceptable
- how to reduce the risk
```

The tool should avoid dramatic language. Reports should be useful for engineering review, not fear-based security theater.
