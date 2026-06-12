# Sanitized Fixture Workflow

Use this internal workflow when a public GitHub config is useful for rule tuning but should not be copied directly into the test corpus.

## Command

```bash
PYTHONPATH=src python scripts/sanitize_github_config.py \
  https://github.com/<owner>/<repo>/blob/<ref>/<path-to-config> \
  --output tests/fixtures/real-world-corpus-v2/<sample-name>.json \
  --metadata-output /tmp/<sample-name>.source.txt
```

The command also accepts `https://raw.githubusercontent.com/...` URLs.

## Sanitization Boundary

The tool redacts:

- GitHub tokens.
- OpenAI-style API keys.
- AWS access key IDs.
- Bearer token values.
- Secret-like key assignments such as `apiKey`, `token`, `secret`, and `password`.
- Personal `/Users/<name>` and `/home/<name>` paths.

The output is still a review artifact. Before committing a fixture:

1. Keep only the minimal structure needed to reproduce the rule behavior.
2. Remove organization names, hostnames, and project-specific labels unless they are essential to the rule.
3. Run `mcp-audit scan --config <fixture> --format json`.
4. Add or update a test that locks the expected rule boundary.
5. Record the source and sampling reason in `docs/real-world-sample-matrix.md`.

## Product Constraint

Do not make this a top-level CLI command yet. It is an internal corpus-maintenance workflow, so the main user entry remains focused on `scan`, `baseline`, `rules`, `explain`, `init`, and `doctor`.
