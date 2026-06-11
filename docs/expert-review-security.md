# mcp-audit Security Expert Review

## Expert Type

security-expert

## Trigger

Mandatory trigger: `mcp-audit` scans files that may contain credentials, permission grants, command execution paths, CI workflow details, and agent/tool configuration. The product also produces security-adjacent findings that could be misunderstood as guarantees.

## Scope Reviewed

- `mcp-audit/docs/prd.md`
- `mcp-audit/docs/architecture.md`
- `mcp-audit/ops/constraints/production.md`
- `mcp-audit/ops/skills/local-overlays.md`
- `mcp-audit/docs/rules.md`
- `mcp-audit/examples/high-risk-mcp.json`

## Findings

Severity vocabulary: critical | high | medium | low

| Severity | Finding | Required remediation |
| --- | --- | --- |
| high | Human-readable output may expose literal secrets if redaction is not applied before Markdown rendering. | Redaction must run before Markdown rendering. Add tests proving known token patterns are redacted in Markdown output. |
| high | Rule output could overclaim security if language implies prevention or guarantees. | CLI, reports, README, and docs must use risk-review wording only: detect, highlight, review, remediate. Avoid "secure", "prevent", "guarantee", and equivalent claims. |
| high | Static rule findings may create false confidence if no limitations are visible. | Markdown and JSON reports must include a limitations section or metadata explaining that findings are risk signals, not complete security coverage. |
| medium | Secret detection can create both false positives and false negatives. | Each secret rule must include positive and negative fixtures, confidence level, and remediation that avoids exposing raw values. |
| medium | Unsafe command findings may be noisy for legitimate MCP servers that use wrappers. | Command rules must include evidence and confidence. Default `--fail-on` must remain `never` in v0.1. |
| medium | Broad filesystem access rules can behave differently across macOS, Linux, and Windows path conventions. | v0.1 must test macOS and Linux path patterns. Windows support must be documented as unverified until tests exist. |
| medium | Future config discovery can scan too broadly and surprise users. | v0.1 should prioritize explicit `--config` scans. Discovery must be bounded to known candidate filenames and documented paths. |
| low | Example high-risk config contains a fake GitHub token-like value. | Keep the example clearly fake and ensure documentation never instructs users to paste real secrets into fixtures. |

## Decision

pass

The architecture may proceed to QA planning and implementation planning, provided the required remediations above become testable implementation requirements.

## Residual Risk

- Static auditing cannot detect all MCP or agent risk.
- Users may still misinterpret findings as complete security coverage.
- Secret detection will remain heuristic in v0.1.
- YAML and client-specific config formats may introduce unsupported cases.
- Runtime behavior, tool prompt injection, and actual command execution are out of scope for v0.1.
