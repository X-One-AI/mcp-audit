# Local Skill Overlays

This file contains project-local guidance for agentic workers.

It supplements OPT. It does not replace or modify OPT.

## Product Overlay

Reject features that are only impressive in a demo.

Every accepted feature must answer:

```text
- Who would use this in a real repository?
- What risk does it reduce or make visible?
- What report, rule, or workflow becomes better?
- How will we know it is useful?
```

## Architecture Overlay

Prefer small, stable boundaries:

```text
- config discovery
- parsers
- rule engine
- findings model
- report renderers
- CLI commands
- fixtures
```

Do not mix rule detection, report rendering, and CLI presentation in the same module.

## Security Overlay

Assume scanned configs may contain secrets.

Required behavior:

```text
- no hidden uploads
- no telemetry by default
- redact sensitive values in human-readable reports
- keep raw config handling isolated
- avoid overclaiming security guarantees
```

## QA Overlay

Every rule needs:

```text
- positive fixture
- negative fixture
- severity expectation
- remediation expectation
```

Every report format needs a contract test.

## Developer Overlay

Implement the smallest production-usable path.

Avoid:

```text
- demo-only shortcuts
- global mutable state
- hardcoded local paths
- network calls during scan
- broad dependencies for simple parsing
```
