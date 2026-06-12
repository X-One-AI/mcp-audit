# Rule Tuning Findings

Snapshot date: 2026-06-12

These findings come from the twelve-sample real-world corpus v2. They should drive rule design only after fixture evidence exists.

## Current Confirmed Boundaries

| Boundary | Evidence | Decision |
| --- | --- | --- |
| Local node entrypoints should not be remote-package findings. | `cline-official-settings-path.json`, `confluent-local-node-config.json` | Keep `XONE003` scoped to remote package runners. |
| Floating package versions should be high-signal. | `agentdesk-browser-tools-floating-package.json`, `grab-cursor-figma-bunx-latest.json`, `run-llama-claude-llamacloud.json` | Keep `@latest` and similar versions in `XONE003`. |
| Placeholder secret values should not be treated as real secrets. | `run-llama-claude-llamacloud.json` | Keep placeholder suppression. |
| Environment variable references should not be literal-secret findings. | `task-master-cursor-roo-npx.json`, `cline-official-settings-path.json` | Keep `${TOKEN}` style references outside `XONE001`. |

## Rule Gaps

### XONE008 candidate: Broad tool enablement

Evidence:

- `kubernetes-http-enable-all-tools.yaml` contains `enableAllTools: true`.

Why it matters:

- Some clients and servers expose many tools behind one MCP endpoint. Enabling every tool can be a higher-risk decision than connecting to a narrow server.

Proposed behavior:

- Add a medium or high confidence finding when keys such as `enableAllTools`, `allowAllTools`, or `tools: "*"` are present.

### Docker image pinning

Evidence:

- `github-mcp-docker-env.json` runs `ghcr.io/github/github-mcp-server`.
- `hassanaftab-pentest-docker.json` runs `mcp/brave-search`.

Why it matters:

- Docker images without tag or digest are floating supply-chain inputs.

Proposed behavior:

- Extend supply-chain checks to Docker image references in `docker run` args.
- Treat `image:latest` and untagged images as unpinned.
- Treat digest-pinned images as acceptable.

### Docker env passthrough

Evidence:

- `github-mcp-docker-env.json` uses `docker run -e GITHUB_PERSONAL_ACCESS_TOKEN`.
- `hassanaftab-pentest-docker.json` uses `docker run -e BRAVE_API_KEY`.

Why it matters:

- `-e NAME` passes host environment values into containers without showing the actual secret in config.

Proposed behavior:

- Consider a medium finding when a container receives sensitive-looking env variable names through `-e`.
- Do not report raw secret values.

### Cline path coverage

Evidence:

- `cline/cline` source confirms `~/.cline/data/settings/cline_mcp_settings.json` for the desktop sidecar.

Why it matters:

- Project-local discovery should stay bounded, but docs should explain explicit `--config` for Cline global paths.

Proposed behavior:

- Do not scan home/global paths by default.
- Add docs showing Cline users how to run `mcp-audit scan --config PATH`.

## Deferred Decisions

- Whether broad network access should flag every HTTP MCP endpoint or only wildcard/broad hosts.
- Whether Docker MCP commands should belong to `supply-chain`, `command`, or a new `container` category.
- Whether team profile should enable future Docker and broad-tool rules by default.
