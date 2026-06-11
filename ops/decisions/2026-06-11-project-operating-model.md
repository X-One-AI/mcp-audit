# Project Operating Model

## Context

`mcp-audit` is the first active X-One project. It must be production-usable, not demo-only, while still using the One Person Team workflow as a reference.

The project also needs room for project-specific knowledge, constraints, and role adjustments without modifying global OPT files.

## Decision

Use a project-local operating layer:

```text
mcp-audit/ops/
```

This layer references OPT and stores:

```text
- local role overlays
- production constraints
- project knowledge
- skill evolution rules
- decision records
```

The public `mcp-audit/README.md` stays concise and links to `ops/README.md`.

## Alternatives Considered

```text
1. Modify OPT directly
   Rejected because changes would leak project-specific behavior into global workflow.

2. Put all constraints in README
   Rejected because it would make the main entry too crowded for outside users.

3. Keep constraints only in chat history
   Rejected because future workers would not inherit them reliably.
```

## Consequences

```text
- Project-specific behavior is versioned with the project.
- OPT remains clean and reusable.
- Future constraints and local skill overlays can evolve without crowding the public entrypoint.
- Contributors need to know that ops/ contains maintainer and agent-worker context.
```
