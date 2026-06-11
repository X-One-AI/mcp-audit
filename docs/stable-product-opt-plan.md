# mcp-audit 稳定成熟产品 OPT 计划

## 1. Product Manager

### 问题

`mcp-audit` 已达到 v0.1 生产可用，但真实团队长期使用还缺少成熟产品闭环：

- 不能区分“已审查接受的历史风险”和“新增风险”
- 需要靠命令参数记忆项目策略
- release、CI、README 多语言和规则文档同步仍需要更强约束
- finding 缺少稳定身份，不利于 baseline、审计和代码审查

### 目标

- 支持稳定 finding fingerprint。
- 支持 baseline 工作流，让团队可以只阻断新增未接受风险。
- 支持项目级配置，减少重复 CLI 参数。
- 保持本地优先、无遥测、无隐藏网络调用。
- 保持英文和中文 README 同步。
- 每批完成后验证、提交、推送。

### 非目标

- 不做 hosted service。
- 不做 dashboard。
- 不做运行时 sandbox。
- 不引入数据库或后台服务。
- 不把 baseline 解释为风险安全证明。

### 需求

| ID | Requirement | Acceptance |
| --- | --- | --- |
| MAT-001 | Finding 有稳定 fingerprint | JSON、Markdown、SARIF 输出包含 fingerprint；相同 finding 多次扫描保持一致 |
| MAT-002 | 支持 baseline 创建 | `mcp-audit baseline --config ... --output ...` 输出 accepted findings |
| MAT-003 | 支持 baseline 抑制 | `scan --baseline ...` 只隐藏匹配 fingerprint 的 finding |
| MAT-004 | 支持项目配置 | `.mcp-audit.toml` 能声明默认 `fail_on` 和 `baseline` |
| MAT-005 | 支持 init | `mcp-audit init` 创建默认项目配置 |
| MAT-006 | 文档双语同步 | 英文和中文 README 都说明成熟功能 |
| MAT-007 | CI 覆盖成熟路径 | CI 至少跑安装、测试、CLI smoke、JSON/SARIF smoke |

## 2. Architect

### 模块边界

- `model.py`: finding、report、summary 等稳定数据模型。
- `baseline.py`: baseline schema、fingerprint 过滤、baseline rendering。
- `project_config.py`: `.mcp-audit.toml` 读取和默认配置写入。
- `cli.py`: 参数解析、命令路由、项目配置合并。
- `renderers/*`: Markdown、JSON、SARIF 输出契约。

### 数据流

```text
config file -> parser -> rules -> findings
findings -> fingerprint -> report renderers
findings -> baseline renderer -> .mcp-audit-baseline.json
project config -> scan defaults -> baseline filtering -> fail-on decision
```

### 契约

- Fingerprint 由稳定字段生成，不包含 raw secret。
- Baseline 文件只记录接受所需的最小信息：fingerprint、rule、severity、path、title。
- `.mcp-audit.toml` 初始只支持 `[scan] fail_on` 和 `baseline`，避免主入口拥挤。
- 显式 CLI 参数优先级高于项目配置。

### 风险

| Risk | Severity | Mitigation |
| --- | --- | --- |
| baseline 被误解为安全证明 | high | README 和报告文档明确 baseline 是风险接受记录 |
| fingerprint 不稳定导致 baseline 失效 | high | contract tests 固定字段，并避免 raw evidence |
| 项目配置过早膨胀 | medium | 只支持 scan 默认值，不引入复杂策略语言 |
| 多语言 README 漂移 | medium | 测试检查双语入口和核心命令 |

## 3. QA Engineer

### 必测路径

- baseline 生成包含 fingerprint。
- scan 使用 baseline 后 findings 为 0。
- `--fail-on high` 在 baseline 抑制后不失败。
- `mcp-audit init` 写入默认 `.mcp-audit.toml`。
- `.mcp-audit.toml` 中的 baseline 和 fail_on 被 scan 使用。
- 显式 CLI 参数覆盖项目配置。
- JSON/SARIF 可被标准 JSON 工具解析。
- raw secret 不出现在报告和 baseline 中。

### 回归范围

- 现有规则检测不变。
- 默认无配置时仍可用。
- CI 安装和 CLI smoke 继续通过。
- README 英文和中文都包含核心成熟功能。

## 4. Developer Plan

### Batch A: Baseline

- Add finding fingerprint.
- Add baseline schema and filtering.
- Add CLI `baseline` and `scan --baseline`.
- Update renderers and docs.

### Batch B: Project Config

- Add `.mcp-audit.toml` loading.
- Add `mcp-audit init`.
- Merge project defaults with explicit CLI args.
- Update README and tests.

### Batch C: Release Maturity

- Add release checklist or release notes policy.
- Strengthen CI smoke for baseline/config path.
- Run full verification and wait for remote CI.

## 5. Completion Gate

Work is not complete until:

- local tests pass
- Markdown fences and `git diff --check` pass
- JSON/SARIF smoke passes
- baseline/config smoke passes
- changes are committed and pushed
- GitHub CI passes on pushed commit
