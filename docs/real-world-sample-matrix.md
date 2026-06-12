# Real-World Sample Matrix

Snapshot date: 2026-06-12

This matrix turns public MCP and agent configuration examples into a repeatable product sampling program. Samples are selected for behavioral coverage, not only repository popularity.

## Acceptance Criteria

| ID | Requirement | Acceptance |
| --- | --- | --- |
| RWS-001 | Source traceability | Every fixture records repository, source URL, commit/reference, and sampling reason. |
| RWS-002 | Sanitization | Fixtures contain no real tokens, local usernames, private paths, or full upstream config dumps. |
| RWS-003 | Product coverage | The set covers public repo messiness, MCP server examples, AI coding clients, and security-high-risk shapes. |
| RWS-004 | Rule tuning | Each sample maps to expected findings or an explicit rule gap. |
| RWS-005 | Regression value | Corpus tests fail when parsers, rule boundaries, or redaction regress. |

## Sample Set

| Fixture | Repository | Stars / Forks | Source | Category | Coverage | Expected result |
| --- | --- | ---: | --- | --- | --- | --- |
| `agentdesk-browser-tools-floating-package.json` | `AgentDeskAI/browser-tools-mcp` | 7237 / 529 | README quickstart | MCP server example, AI coding client | Cursor/Cline/Zed compatible install with `npx ...@latest` | `XONE003` |
| `cline-official-settings-path.json` | `cline/cline` | 63115 / 6664 | `apps/examples/desktop-app/sidecar/paths.ts` | Cline client sample | Official `cline_mcp_settings.json` path behavior represented as local settings fixture | Scan succeeds; no remote-package finding |
| `confluent-local-node-config.json` | `confluentinc/mcp-confluent` | 159 / 54 | `example.claude_desktop_config.json` | MCP server example | Claude config with local node entrypoint | Scan succeeds; no remote-package finding |
| `danlee-mcp-setup-aggregate.json` | `danlee-dev/mcp-setup` | 0 / 0 | `mcp-settings.json` | Public repo messiness, high-risk | Many MCP servers, `${HOME}`, unpinned packages, env references | `XONE003`, `XONE004` |
| `task-master-cursor-roo-npx.json` | `eyaltoledano/claude-task-master` | 27393 / 2566 | README Cursor/Windsurf/Roo setup | AI coding client, MCP server example | `mcpServers` and unpinned `npx task-master-ai` with env references | `XONE003` |
| `github-mcp-docker-env.json` | `github/github-mcp-server` | 30606 / 4371 | README local Docker install | MCP server example, high-risk | Docker command, token env passthrough, GitHub PAT placeholder | `XONE009`, `XONE010` |
| `grab-cursor-figma-bunx-latest.json` | `grab/cursor-talk-to-figma-mcp` | 6831 / 743 | README Cursor setup | Cursor client, MCP server example | Cursor config with `bunx ...@latest` | `XONE003` |
| `hassanaftab-pentest-docker.json` | `hassanaftab93/pentesting-mcp-setup` | 1 / 2 | `mcp-settings.json` | High-risk security sample | Pentest Docker MCP, env passthrough, docker exec | `XONE009`, `XONE010` |
| `ingenimax-devops-agent.yaml` | `Ingenimax/agent-sdk-go` | 569 / 127 | `examples/mcp/standalone_mcp_config.yaml` | YAML agent, DevOps | Filesystem MCP, monitoring env flags, git tool | `XONE003` |
| `kubernetes-http-enable-all-tools.yaml` | `containers/kubernetes-mcp-server` | 1677 / 365 | `evals/mcp-config.yaml` | MCP server example, high-risk | Kubernetes HTTP MCP, `enableAllTools` | `XONE008` |
| `nyldn-zed-context-servers.json` | `nyldn/claude-octopus` | 3575 / 334 | `config/ide-templates/zed-settings.json` | AI coding client | Zed `context_servers`, env placeholders, `npx tsx` | `XONE003` |
| `run-llama-claude-llamacloud.json` | `run-llama/llamacloud-mcp` | 223 / 48 | `claude_desktop_config.json` | MCP server example, Claude config | `uvx`, `@latest`, placeholder API key, filesystem MCP | `XONE003`; no placeholder secret finding |

## Coverage By Product Category

| Category | Samples |
| --- | --- |
| Open public repositories / ecosystem messiness | `danlee-dev/mcp-setup`, `hassanaftab93/pentesting-mcp-setup`, `eyaltoledano/claude-task-master` |
| MCP server examples / standard config | `github/github-mcp-server`, `run-llama/llamacloud-mcp`, `confluentinc/mcp-confluent`, `containers/kubernetes-mcp-server`, `grab/cursor-talk-to-figma-mcp` |
| AI coding client behavior | Cursor: `grab/cursor-talk-to-figma-mcp`, `eyaltoledano/claude-task-master`; Cline: `cline/cline`; Claude: `run-llama/llamacloud-mcp`; Zed: `nyldn/claude-octopus` |
| Security-high-risk shapes | `github/github-mcp-server`, `containers/kubernetes-mcp-server`, `danlee-dev/mcp-setup`, `hassanaftab93/pentesting-mcp-setup`, `Ingenimax/agent-sdk-go` |

## Change Control

- Keep this matrix in sync with `tests/fixtures/real-world-corpus-v2/README.md`.
- Add a row before adding a fixture.
- Record star/fork counts only as a snapshot; do not treat them as live truth.
- If a fixture starts representing a different behavior, rename it instead of silently changing its meaning.
