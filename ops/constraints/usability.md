# Usability Constraint

`mcp-audit` must be useful and pleasant enough for real developers to keep using.

The bar is not:

```text
it works
```

The bar is:

```text
it is easy to understand, hard to misuse, and clear about the next action.
```

## Usability Standards

Every user-facing feature must satisfy these standards:

```text
- the first successful run explains what was scanned
- findings explain why they matter
- remediation is concrete enough to act on
- errors say what happened and how to fix it
- defaults are safe and unsurprising
- output is readable without color
- commands behave consistently across explicit and discovered config scans
- docs show the shortest useful path first
- public README files support at least English and Chinese when the project has external users
```

## Documentation Language Rules

Public user-facing README content must be available in at least:

```text
- English
- Simplified Chinese
```

Required:

```text
- `README.md` remains the English entry point unless a project explicitly chooses another default.
- `README.zh-CN.md` provides the Simplified Chinese version.
- Each language version links to the other near the top.
- Core usage commands, install commands, limitations, and CI guidance stay semantically aligned across languages.
```

When behavior changes, update every supported README language in the same write batch.

## CLI Experience Rules

CLI output should optimize for review, not spectacle.

Required:

```text
- concise summaries
- stable terminology
- predictable exit codes
- no raw secret leakage
- no noisy warnings without remediation
- no hidden network or telemetry behavior
```

Avoid:

```text
- vague findings
- walls of text before the useful result
- clever wording
- fear-based security language
- commands that succeed silently when nothing useful happened
```

## Definition Of Good

A feature is not ready if a target user can reasonably ask:

```text
- What did it scan?
- Why is this a problem?
- What should I do next?
- Did it expose my data?
- Can I trust this output in a review?
```

and the product does not answer clearly.

## Release Gate Addition

Before completion, every user-facing change must include at least one of:

```text
- CLI output test
- report contract test
- documentation update
- fixture proving the confusing case is handled
```

If a change only makes an internal API work but leaves the user path confusing, it is not complete.
