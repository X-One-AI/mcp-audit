# Production-Usable Constraint

`mcp-audit` is not a demo project.

Every feature must be useful in a real repository, even if the first release is small.

## Required Standards

```text
- deterministic CLI behavior
- no hidden network calls
- local-first scanning
- clear error messages
- machine-readable JSON output
- human-readable Markdown output
- stable rule IDs
- documented severities
- fixture-based tests for rules
- explicit non-goals and limitations
- user-facing output that explains the next action
```

## Security Posture

The tool must not claim to make a project safe.

Allowed wording:

```text
- detects risk signals
- helps reviewers inspect agent and MCP configurations
- generates reviewable safety reports
- highlights risky permissions and unsafe execution paths
```

Avoid wording:

```text
- prevents attacks
- guarantees security
- secures MCP
- makes agents safe
```

## Release Gate

A feature cannot be called done unless:

```text
1. It has tests.
2. It has at least one fixture.
3. It has a documented rule or contract.
4. It has a clear failure mode.
5. It has a usable user path, not just a working code path.
6. It does not add noisy public README content unless required for first-run usage.
```

## Repository Discipline

`mcp-audit` is its own repository. Do not initialize git at the X-One organization root.

After each completed write batch:

```text
1. Run the relevant verification commands.
2. Commit inside the mcp-audit repository.
3. Push the commit to the remote repository.
```

If push is unavailable because the remote is missing or authentication fails, stop and report the exact blocker instead of continuing to accumulate unpushed work.
