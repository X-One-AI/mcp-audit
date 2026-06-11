# mcp-audit Knowledge Base

This is the project-local knowledge base.

It stores domain facts, validated assumptions, user feedback, release lessons, and rule rationale.

Do not store general OPT instructions here. Store only knowledge that improves `mcp-audit`.

## Knowledge Types

| Type | File |
|---|---|
| Domain assumptions | [domain.md](./domain.md) |
| User feedback | `feedback.md` when real feedback exists |
| Rule rationale | `rule-rationale.md` when rules become stable |
| Release lessons | `release-lessons.md` after first release |

## Promotion Rule

Knowledge should move through this path:

```text
observation -> validated assumption -> constraint/rule -> test fixture -> documentation
```

If it never becomes a rule, fixture, or documented limitation, it should not grow endlessly.
