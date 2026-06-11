# Main Entry Constraint

The public entrypoint must stay small.

For `mcp-audit`, the main entrypoint is:

```text
mcp-audit/README.md
```

## README Should Contain

```text
- one-line value proposition
- who it is for
- quick install / run command once implementation exists
- minimal example output
- links to deeper docs
```

## README Should Not Contain

```text
- full OPT workflow
- long strategy explanations
- complete rule catalog
- internal role overlays
- historical decision notes
- every future project direction
```

## Routing Rule

Put deeper content here:

```text
- operating model -> ops/
- rule catalog -> docs/rules.md
- design decisions -> ops/decisions/
- project knowledge -> ops/knowledge/
- local skill overlays -> ops/skills/
```

This keeps the project credible to outside users while preserving enough context for agentic workers.
