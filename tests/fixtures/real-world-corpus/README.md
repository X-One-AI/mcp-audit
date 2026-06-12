# Real-World Corpus Fixtures

These fixtures are sanitized, minimal reproductions of configuration shapes observed in public repositories.
They preserve product-relevant structure and risk boundaries without copying private values or full upstream files.

## Sources

| Fixture | Source | Why sampled |
| --- | --- | --- |
| `claude-llamacloud-sanitized.json` | https://github.com/run-llama/llamacloud-mcp/blob/ebc66ba1c0b772cc3eced4db170c3e7eb9679f1e/claude_desktop_config.json | Claude desktop shape with `uvx`, `@latest`, placeholder API key, and filesystem MCP server. |
| `cursor-chrome-devtools-sanitized.json` | https://github.com/HarimaGoncalves/pagination-token-api/blob/50e49e741ef8e6da1c9011005b3fff1033408f84/mcp.json | Project-local `mcp.json` shape with `npx` and `@latest`. |
| `claude-local-node-sanitized.json` | https://github.com/confluentinc/mcp-confluent/blob/24fefd931c76e1209309e3ac0a0b3197c7b403d5/example.claude_desktop_config.json | Local node entrypoint shape that should not be treated as remote package execution. |
| `yaml-nested-agent-filesystem.yaml` | https://github.com/Ingenimax/agent-sdk-go/blob/b3fb0713784fc9b5a2ee89ab8d8920ced5d84eed/examples/simple_yaml_agent/agents.yaml | Nested agent shape where MCP servers live below agent-specific keys. |
| `zed-context-server-sanitized.json` | https://github.com/meimingqi222/mcp-sync/blob/0ca9e17f44636f7dd1aa5f5eff1d557c175ea392/agents.yaml | Zed-style `context_servers` shape discovered through client mapping metadata. |
