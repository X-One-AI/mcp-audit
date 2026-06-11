# Rule Tuning And False Positive Workflow

`mcp-audit` should keep high-signal rules useful in real repositories. False-positive reports are product feedback, not noise.

## When To Tune A Rule

Tune a rule when at least one of these is true:

- A safe, common configuration pattern is repeatedly flagged.
- The finding evidence is technically correct but not actionable.
- The remediation is too vague for a reviewer to decide.
- A rule fires on configs outside its intended domain.

## Required Evidence

Every tuning change needs:

```text
- minimal config snippet that reproduces the finding
- expected result
- actual result
- why the configuration is acceptable
- whether the rule, severity, evidence, or remediation should change
```

## Change Rules

- Add a negative fixture for every false-positive fix.
- Add or update a positive fixture if the rule boundary changes.
- Keep rule IDs stable.
- Do not weaken high-severity rules without documenting why.
- Update English and Chinese README only when user-facing behavior changes.

## Review Checklist

```text
- Does the fix reduce noise without hiding a real high-risk pattern?
- Does the fixture describe the product scenario?
- Does the report remain actionable?
- Do JSON, Markdown, and SARIF contracts still pass?
```
