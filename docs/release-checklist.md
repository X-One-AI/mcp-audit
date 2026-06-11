# mcp-audit Release Checklist

Use this checklist before tagging or announcing a release.

## Required Verification

```bash
python -m pytest tests -q
mcp-audit --version
mcp-audit doctor
mcp-audit rules
mcp-audit scan --config examples/high-risk-mcp.json --format json --output /tmp/mcp-audit.json
mcp-audit scan --config examples/high-risk-mcp.json --format sarif --output /tmp/mcp-audit.sarif
mcp-audit baseline --config examples/high-risk-mcp.json --output /tmp/mcp-audit-baseline.json
mcp-audit scan --config examples/high-risk-mcp.json --baseline /tmp/mcp-audit-baseline.json --format json --output /tmp/mcp-audit-baselined.json
python -m json.tool /tmp/mcp-audit.json >/dev/null
python -m json.tool /tmp/mcp-audit.sarif >/dev/null
python -m json.tool /tmp/mcp-audit-baseline.json >/dev/null
python -m json.tool /tmp/mcp-audit-baselined.json >/dev/null
```

## Release Gates

- GitHub CI is green on the release commit.
- `README.md` and `README.zh-CN.md` describe the same core commands.
- `CHANGELOG.md` has an entry for the release.
- `docs/rules.md` mentions every registered rule.
- Baseline docs say baseline means risk acceptance, not safety proof.
- Reports show suppressed finding count when baseline is used.
- No report or baseline exposes raw secret fixture values.

## Tagging

Only tag after all required verification passes:

```bash
git tag v0.1.0
git push origin v0.1.0
```
