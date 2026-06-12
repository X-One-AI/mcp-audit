# Publishing

`mcp-audit` uses GitHub Actions and PyPI Trusted Publishing for package publication. Trusted Publishing uses OpenID Connect instead of a long-lived package token.

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
2. Tag the release, for example `v0.2.0`.
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
