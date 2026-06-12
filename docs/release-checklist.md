# mcp-audit Release Checklist

Use this checklist before tagging or announcing a release.

## Required Verification

```bash
python -m pytest tests -q
python -m build
mcp-audit --version
mcp-audit doctor
mcp-audit rules
mcp-audit rules --profile starter
mcp-audit init --profile team
mcp-audit scan --config examples/high-risk-mcp.json --format json --output /tmp/mcp-audit.json
mcp-audit scan --config examples/high-risk-mcp.json --format sarif --output /tmp/mcp-audit.sarif
mcp-audit scan --config tests/fixtures/high-risk-agent.yaml --format json --output /tmp/mcp-audit-yaml.json
mcp-audit scan --config tests/fixtures/high-risk-agent.toml --format json --output /tmp/mcp-audit-toml.json
mcp-audit scan --config tests/fixtures/high-risk-real-world.json --format json --output /tmp/mcp-audit-real-world.json
mcp-audit baseline --config examples/high-risk-mcp.json --output /tmp/mcp-audit-baseline.json
mcp-audit scan --config examples/high-risk-mcp.json --baseline /tmp/mcp-audit-baseline.json --format json --output /tmp/mcp-audit-baselined.json
mcp-audit baseline --config examples/high-risk-mcp.json --baseline /tmp/mcp-audit-baseline.json --prune --output /tmp/mcp-audit-baseline-pruned.json
python -m json.tool /tmp/mcp-audit.json >/dev/null
python -m json.tool /tmp/mcp-audit.sarif >/dev/null
python -m json.tool /tmp/mcp-audit-baseline.json >/dev/null
python -m json.tool /tmp/mcp-audit-baselined.json >/dev/null
python -m json.tool /tmp/mcp-audit-baseline-pruned.json >/dev/null
python -m json.tool /tmp/mcp-audit-yaml.json >/dev/null
python -m json.tool /tmp/mcp-audit-toml.json >/dev/null
python -m json.tool /tmp/mcp-audit-real-world.json >/dev/null
```

## Release Gates

- GitHub CI is green on the release commit.
- `README.md` and `README.zh-CN.md` describe the same core commands.
- `CHANGELOG.md` has an entry for the release.
- `docs/rules.md` mentions every registered rule.
- Baseline docs say baseline means risk acceptance, not safety proof.
- Reports show suppressed finding count when baseline is used.
- Baseline prune removes stale accepted findings.
- Doctor shows project configuration status and effective scan defaults.
- Rule profiles are documented and smoke-tested.
- JSON, YAML, and TOML config smoke checks pass.
- Real-world shaped fixture smoke check passes.
- Sanitized real-world corpus and client-format fixtures pass.
- Package artifacts are built under `dist/`.
- CI uploads package artifacts for the release commit.
- False-positive workflow exists under `.github/ISSUE_TEMPLATE/`.
- No report or baseline exposes raw secret fixture values.

## Tagging

Only tag after all required verification passes:

```bash
git tag -a v0.1.0 -m "mcp-audit v0.1.0"
git push origin v0.1.0
```
