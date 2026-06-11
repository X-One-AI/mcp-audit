# mcp-audit 产品面扩展 OPT 计划

## 1. Product Manager

### 问题

`mcp-audit` 已经具备稳定 CLI 产品闭环，但要覆盖更大的真实产品面，还需要支持更多配置来源、更多配置格式、更多真实风险规则、正式 release/package 流程，以及误报调优反馈闭环。

### 目标

- 支持 JSON、YAML、TOML agent/MCP 配置扫描。
- 扩展 bounded default discovery，覆盖更多常见 MCP 客户端项目内配置路径。
- 增加高信号规则和真实世界风格 fixture。
- 建立正式 tag/release/package 流程，至少能生成可审计的 release artifact。
- 建立误报反馈模板和调优流程，避免规则演进只靠直觉。

### 非目标

- 不扫描用户 home 目录中的隐私配置，除非用户显式传 `--config`。
- 不做 hosted service 或 dashboard。
- 不把所有 agent 配置生态一次性穷尽。
- 不为了减少误报牺牲明显高风险信号。

### 需求

| ID | Requirement | Acceptance |
| --- | --- | --- |
| SURF-001 | YAML config scanning | `scan --config agent.yaml` can parse YAML object configs and run rules |
| SURF-002 | TOML config scanning | `scan --config agent.toml` can parse TOML object configs and run rules |
| SURF-003 | More bounded client discovery | default `scan` checks documented project-local MCP/client config paths |
| SURF-004 | More rules | add at least two high-signal rules with positive/negative fixtures |
| SURF-005 | Real-world fixtures | fixtures represent common Cursor/Claude/Continue/agent config shapes without real secrets |
| SURF-006 | Release/package path | CI verifies package build or release artifact generation path |
| SURF-007 | Feedback loop | docs include false-positive report template and rule tuning workflow |
| SURF-008 | Multilingual docs | English and Simplified Chinese README remain semantically aligned |

## 2. Architect

### Module Boundaries

- `parsers/`: format-specific parsers and parser selection.
- `config_discovery.py`: bounded project-local discovery only.
- `rules/`: high-signal rules with registry metadata and fixture coverage.
- `fixtures/`: safe/high-risk and client-shaped examples.
- `docs/`: release, feedback, and rule-tuning process.
- `.github/workflows/ci.yml`: install, tests, CLI smoke, build/package smoke.

### Data Flow

```text
default discovery / --config
  -> parser selection by extension
  -> normalized ConfigDocument
  -> registered rules
  -> report renderers / baseline / CI fail-on
```

### Dependency Decision

- TOML uses Python stdlib `tomllib` for Python 3.11+.
- YAML uses `PyYAML` because YAML needs a real parser. Ad-hoc parsing is not acceptable for production behavior.

### Risk Controls

| Risk | Mitigation |
| --- | --- |
| YAML parser dependency increases supply-chain surface | pin minimum version and cover CI install |
| default discovery scans too much | keep bounded project-local candidate list only |
| new rules create false positives | require positive/negative fixtures and feedback template |
| package release is claimed without artifact check | CI must build distribution artifacts before release |

## 3. QA Engineer

### Required Tests

- JSON existing tests remain green.
- YAML positive fixture triggers expected findings.
- TOML positive fixture triggers expected findings.
- Unsupported extension returns user-facing parse error.
- Default discovery includes new project-local candidates.
- Every rule has positive and negative fixture coverage.
- New rule docs mention every registered rule.
- CI builds source/wheel artifacts.
- Feedback template exists and asks for enough reproduction context.

## 4. Developer Plan

### Batch A: Multi-format parsing and discovery

- Add parser selector.
- Add YAML and TOML parsers.
- Add YAML dependency.
- Expand bounded default candidates.
- Add fixtures and tests.

### Batch B: Rule expansion and real-world fixtures

- Add two high-signal rules.
- Add Cursor/Claude/Continue/agent-shaped fixtures.
- Update rules docs and coverage tests.

### Batch C: Release/package and feedback loop

- Add build backend verification and CI package build.
- Add feedback template and tuning docs.
- Create release artifact path and, if checks pass, tag v0.1.0.

## 5. Completion Gate

- OPT plan exists before implementation.
- Local tests pass.
- CI passes on final commit.
- Release/package path is verified.
- README English and Chinese are updated.
- No raw secret fixture values appear in reports.
