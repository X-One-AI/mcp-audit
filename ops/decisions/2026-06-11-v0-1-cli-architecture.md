# v0.1 CLI Architecture

## Context

`mcp-audit` needs a first production-usable implementation path. The product requirements call for local-first static auditing, stable rule IDs, Markdown and JSON reports, and no hidden network behavior.

## Decision

Use a Python CLI for v0.1 with clear module boundaries:

```text
- CLI
- scan orchestration
- config discovery
- parsers
- rule engine
- findings model
- redaction
- report renderers
- tests and fixtures
```

Support JSON configuration parsing first. Keep YAML as an extension point, but do not add a YAML dependency until validated by a v0.1 user/config need.

Use Markdown as the human review format and JSON as the automation contract.

## Alternatives Considered

```text
1. TypeScript CLI
   Rejected for v0.1 because Python standard-library parsing is enough for the first local auditor and keeps dependencies low.

2. Runtime gate or proxy
   Rejected because v0.1 is audit-only and should not overclaim enforcement.

3. Hosted service
   Rejected because local-first privacy is a core product constraint.

4. Full YAML and multi-format support immediately
   Rejected until user validation proves those formats are necessary for v0.1.
```

## Consequences

```text
- v0.1 can be implemented with a small dependency surface.
- Tests can focus on rule fixtures and report contracts.
- Future GitHub Action support can reuse JSON output.
- Node-based distribution may need a later decision if early users expect npm-based install.
```
