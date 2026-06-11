# Domain Assumptions

These assumptions guide early `mcp-audit` design.

They must evolve as real users scan real MCP and agent configurations.

## Current Assumptions

```text
- MCP tools and AI agents increasingly receive access to files, shells, networks, credentials, and CI workflows.
- Teams want agent productivity but need reviewable evidence before trusting agent workflows.
- Static config auditing is a useful first step before runtime enforcement.
- High-signal findings are more valuable than a broad checklist with noisy warnings.
- Reports must be useful to both engineers and security reviewers.
```

## Early Risk Areas

```text
- literal secrets in config
- broad filesystem access
- shell execution
- unpinned package execution
- broad network access
- unclear GitHub token usage
- agent-generated changes without test or risk evidence
```

## Open Questions

```text
- Which MCP config formats are most common among early users?
- Which rule categories produce useful findings without too many false positives?
- Should the first GitHub Action comment on PRs or only write job summaries?
- How much policy customization is needed before teams try the tool?
```
