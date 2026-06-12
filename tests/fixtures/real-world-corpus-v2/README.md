# Real-World Corpus V2

These fixtures are sanitized minimal reproductions from twelve public repositories selected for product coverage, not popularity alone.

## Sanitization policy

- Keep only the smallest structure needed to exercise a parser, rule, or false-positive boundary.
- Replace real tokens, hostnames, local usernames, and organization values with safe placeholders.
- Preserve source URL, commit reference, category, and sampling reason in `docs/real-world-sample-matrix.md`.
- Do not vendor full upstream config files.

## Fixtures

| Fixture | Source repository | Coverage |
| --- | --- | --- |
| `agentdesk-browser-tools-floating-package.json` | AgentDeskAI/browser-tools-mcp | Cursor/Cline/Zed compatible package install with `@latest`. |
| `cline-official-settings-path.json` | cline/cline | Official Cline settings-path behavior represented as a sanitized local settings fixture. |
| `confluent-local-node-config.json` | confluentinc/mcp-confluent | Claude config with local node entrypoint and local config file. |
| `danlee-mcp-setup-aggregate.json` | danlee-dev/mcp-setup | Multi-server aggregation with filesystem home access and unpinned packages. |
| `task-master-cursor-roo-npx.json` | eyaltoledano/claude-task-master | Cursor/Roo/Windsurf-compatible `mcpServers` example with unpinned `npx`. |
| `github-mcp-docker-env.json` | github/github-mcp-server | Docker MCP server with token environment passthrough. |
| `grab-cursor-figma-bunx-latest.json` | grab/cursor-talk-to-figma-mcp | Cursor Figma MCP install using `bunx` and floating version. |
| `hassanaftab-pentest-docker.json` | hassanaftab93/pentesting-mcp-setup | Security/pentest Docker MCP shape. |
| `ingenimax-devops-agent.yaml` | Ingenimax/agent-sdk-go | YAML DevOps agent MCP shape. |
| `kubernetes-http-enable-all-tools.yaml` | containers/kubernetes-mcp-server | Kubernetes HTTP MCP with broad tool enablement. |
| `nyldn-zed-context-servers.json` | nyldn/claude-octopus | Zed `context_servers` shape with env placeholders. |
| `run-llama-claude-llamacloud.json` | run-llama/llamacloud-mcp | Claude config with `uvx`, `@latest`, placeholder API key, and filesystem. |
