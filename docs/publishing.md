# Publishing

`mcp-audit` uses GitHub Actions and PyPI Trusted Publishing for package publication. Trusted Publishing uses OpenID Connect instead of a long-lived package token.

As of `2026-06-12`, `mcp-audit` is not present on PyPI or TestPyPI. Both package indexes returned `404` for `/pypi/mcp-audit/json`. The publish workflow is ready, but actual publication requires creating the package projects and configuring Trusted Publishers in the package indexes.

References:

- https://docs.pypi.org/trusted-publishers/
- https://github.com/pypa/gh-action-pypi-publish

## GitHub Environments

Create two GitHub environments:

- `testpypi`
- `pypi`

The `pypi` environment should require manual approval before publishing.

## Package Index Setup

Configure Trusted Publishers in TestPyPI and PyPI with:

```text
Owner: X-One-AI
Repository: mcp-audit
Workflow: publish.yml
Environment: testpypi or pypi
```

## Publish Order

1. Merge and verify a green CI run on `main`.
2. Tag the release, for example `v0.3.0`.
3. Create the GitHub release and attach CI-built artifacts.
4. Run `Publish Python Package` with `repository = testpypi`.
5. Verify a clean TestPyPI install.
6. Run `Publish Python Package` with `repository = pypi` from the release tag after approval.
7. Verify a clean PyPI install.

## TestPyPI Install Check

```bash
python -m venv /tmp/mcp-audit-testpypi
/tmp/mcp-audit-testpypi/bin/python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ mcp-audit
/tmp/mcp-audit-testpypi/bin/mcp-audit --version
```

## Current Verified Install Path

Until PyPI/TestPyPI are configured, install from GitHub release assets:

```bash
python3 -m pip install https://github.com/X-One-AI/mcp-audit/releases/download/v0.3.0/mcp_audit-0.3.0-py3-none-any.whl
mcp-audit --version
```

GitHub release artifacts are the verified install path until package-index publication succeeds.
