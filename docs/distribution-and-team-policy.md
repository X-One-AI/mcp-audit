# Distribution And Team Policy Roadmap

This document records the next product phase after `v0.1.0`: make `mcp-audit` easier to adopt in real repositories without weakening rule quality.

## Product Decision

Prepare package publishing now, but keep PyPI production publish behind Trusted Publishing setup, TestPyPI verification, and release approval. Real-user scanning data is still preferred, but `v0.2.0` uses public sample review as a substitute until 3-5 external users can scan private configs.

## Real Repository Sampling

Use a sanitized corpus instead of vendoring full public configs.

```text
1. Search public repositories for MCP and agent config shapes.
2. Record source URL and sampling reason in the corpus manifest.
3. Keep only the minimal structure needed to reproduce product behavior.
4. Remove real hostnames, credentials, personal paths, and organization-specific values.
5. Add one expectation test per behavior boundary.
```

The current corpus lives under `tests/fixtures/real-world-corpus`.

Use `docs/public-sample-feedback-loop.md` when real-user feedback is unavailable.

## Configuration Guidance

The first non-interactive setup surface is:

```bash
mcp-audit init --profile starter
mcp-audit init --profile balanced
mcp-audit init --profile team
```

Profile defaults:

| Profile | Use when | Generated defaults |
| --- | --- | --- |
| starter | A repository is being scanned for the first time and noise risk is high. | `profile = "starter"`, `fail_on = "high"` |
| balanced | A developer wants local review coverage. | `profile = "balanced"`, `fail_on = "high"` |
| team | A team wants CI policy with stronger review gates. | `profile = "team"`, `fail_on = "medium"` |

Avoid a crowded main entrypoint. Future setup improvements should extend `init` rather than adding top-level commands.

## Rule Profile Strategy

Profiles tune rule membership, not rule semantics.

- Keep rule IDs stable across profiles.
- Prefer moving a noisy rule out of `starter` before weakening its detection.
- Record every profile change in `CHANGELOG.md`.
- Require a positive and negative fixture when a rule boundary changes.

## Team Policy Strategy

Team adoption should be file-based and reviewable.

Recommended team rollout:

```text
1. Run `mcp-audit init --profile starter`.
2. Scan representative repos and collect false-positive reports.
3. Tune rules with fixtures.
4. Move to `balanced` for local development.
5. Move CI to `team` only after medium findings are accepted as blocking.
```

Team policy fields are drafted in `docs/team-policy-schema.md` and demonstrated by `examples/team-policy.toml`. They should remain file-based and avoid remote service dependencies in the CLI path.

Global client settings, including Cline user-level settings, should be audited with explicit `--config` paths. They should not become default discovery targets because that would surprise users by reading home-directory configuration.

## PyPI Roadmap

Use PyPI Trusted Publishers for release publishing instead of a long-lived API token. PyPI documents Trusted Publishers as an OIDC-based relationship between a package project and CI workflow.

Readiness gates:

- Reserve and verify the `mcp-audit` project name.
- Add a release workflow using manual dispatch, GitHub environments, and tag-gated production publishing.
- Use PyPI Trusted Publishing with a GitHub Actions environment.
- Publish first to TestPyPI.
- Verify install from a clean virtual environment.
- Publish to PyPI only after GitHub release assets and CI are green.

Reference: https://docs.pypi.org/trusted-publishers/

## Homebrew Roadmap

Start with an X-One tap before attempting `homebrew-core`. Homebrew's Python formula guidance treats CLI applications differently from importable libraries, which fits `mcp-audit`.

Readiness gates:

- PyPI or GitHub release source archive is stable.
- Formula installs a runnable `mcp-audit` executable.
- Formula test runs `mcp-audit --version`.
- Document whether the tap is the official installation path or an early adopter channel.

References:

- https://docs.brew.sh/Python-for-Formula-Authors
- https://docs.brew.sh/Formula-Cookbook

## Non-Goals For This Phase

- No PyPI production publish yet.
- No Homebrew tap creation yet.
- No hosted policy service.
- No organization dashboard.
- No recursive repository scan by default.
