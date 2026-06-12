# Homebrew Packaging

`mcp-audit` should publish to the official X-One tap before attempting `homebrew-core`.

## User Install

```bash
brew install x-one-ai/tap/mcp-audit
mcp-audit --version
```

## Tap Repository

Use this GitHub repository for the tap:

```text
X-One-AI/homebrew-tap
```

The formula should live at:

```text
Formula/mcp-audit.rb
```

## Formula Requirements

- Install the Python CLI as `mcp-audit`.
- Use the released `xone-mcp-audit` source distribution.
- Vendor Python dependencies as Homebrew resources.
- Run `mcp-audit --version` in the formula test.
- Keep the tap README bilingual enough to link English and Simplified Chinese docs.

## Release Update Flow

1. Publish the new `xone-mcp-audit` version to PyPI.
2. Fetch the PyPI source distribution URL and SHA256.
3. Fetch resource URLs and SHA256 values for Python dependencies.
4. Update `Formula/mcp-audit.rb`.
5. Run `brew test mcp-audit` when Homebrew is available locally.
6. Commit and push the tap update.

## Current Target

```text
xone-mcp-audit==0.4.0
```
