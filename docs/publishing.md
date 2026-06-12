# Publishing

`mcp-audit` uses GitHub Actions and PyPI Trusted Publishing for package publication. Trusted Publishing uses OpenID Connect instead of a long-lived package token.

As of `2026-06-13`, the Python distribution package is `xone-mcp-audit`. The installed CLI command remains `mcp-audit`.

The original package name `mcp-audit` was rejected by TestPyPI as too similar to an existing project. Use `xone-mcp-audit` for PyPI and TestPyPI project configuration.

The first TestPyPI publish attempt for `v0.3.0` failed at the trusted publishing exchange with `invalid-publisher`, meaning TestPyPI did not have a publisher matching these claims:

```text
project: xone-mcp-audit
repository: X-One-AI/mcp-audit
workflow: .github/workflows/publish.yml
ref: refs/tags/v0.3.0
environment: testpypi
subject: repo:X-One-AI/mcp-audit:environment:testpypi
```

GitHub run: https://github.com/X-One-AI/mcp-audit/actions/runs/27424380172

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
Project: xone-mcp-audit
Owner: X-One-AI
Repository: mcp-audit
Workflow: publish.yml
Environment: testpypi or pypi
```

For TestPyPI, the pending publisher for project `xone-mcp-audit` and environment `testpypi` has been verified with tag `v0.3.1`.

For PyPI, create the pending publisher for project `xone-mcp-audit` and environment `pypi` before running the workflow against the production index.

## Publish Order

1. Merge and verify a green CI run on `main`.
2. Tag the release, for example `v0.3.1`.
3. Create the GitHub release and attach CI-built artifacts.
4. Run `Publish Python Package` with `repository = testpypi`.
5. Verify a clean TestPyPI install.
6. Run `Publish Python Package` with `repository = pypi` from the release tag after approval.
7. Verify a clean PyPI install.

## TestPyPI Install Check

```bash
python -m venv /tmp/mcp-audit-testpypi
/tmp/mcp-audit-testpypi/bin/python -m pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  xone-mcp-audit
/tmp/mcp-audit-testpypi/bin/mcp-audit --version
```

If the local Python certificate store is broken, verify the environment before changing project publishing configuration. The local macOS verification run required adding `--trusted-host test-files.pythonhosted.org` because TestPyPI serves package files from that host.

## Current Package Index Status

TestPyPI is published and install-verified:

- Package: `xone-mcp-audit==0.3.1`
- CLI: `mcp-audit 0.3.1`
- Workflow run: https://github.com/X-One-AI/mcp-audit/actions/runs/27429045294
- Index metadata: https://test.pypi.org/pypi/xone-mcp-audit/json

PyPI production publishing is still pending the production Trusted Publisher setup for project `xone-mcp-audit` with environment `pypi`.

## GitHub Release Install Path

Install from GitHub release assets when package-index publication is not desired:

```bash
python3 -m pip install https://github.com/X-One-AI/mcp-audit/releases/download/v0.3.1/xone_mcp_audit-0.3.1-py3-none-any.whl
mcp-audit --version
```
