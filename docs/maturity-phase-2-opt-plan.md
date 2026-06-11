# mcp-audit 成熟化二阶段 OPT 计划

## 1. Product Manager

### 问题

`mcp-audit` 已经具备稳定产品最小闭环，但真实团队继续使用时会遇到三个成熟度问题：

- baseline 会隐藏 finding，但报告没有说明隐藏了多少，容易让审查者误以为完全无风险。
- baseline 会随配置变化逐渐变旧，需要维护入口清理已经不存在的 accepted findings。
- 项目配置存在后，用户需要能诊断当前目录是否启用了配置、baseline 和 fail-on 策略。

### 目标

- 扫描报告必须透明展示 suppressed finding 数量。
- baseline 文件必须可维护，至少支持 prune 掉当前扫描中已经不存在的 accepted finding。
- `doctor` 必须展示项目配置状态和有效 scan 默认值。
- 所有新增能力都要进入英文/中文 README、QA 计划、CI 或测试门禁。

### 非目标

- 不做复杂策略语言。
- 不做交互式批准流程。
- 不做服务端状态或数据库。
- 不把 baseline 解释为风险安全证明。

### 需求

| ID | Requirement | Acceptance |
| --- | --- | --- |
| MAT2-001 | 报告展示 suppressed 数量 | JSON summary 和 Markdown summary 都包含 suppressed findings 数量 |
| MAT2-002 | SARIF 记录 suppressed 数量 | SARIF run properties 包含 suppressed finding count |
| MAT2-003 | baseline prune | CLI 能基于当前扫描结果输出只保留仍存在 findings 的 baseline |
| MAT2-004 | doctor 配置诊断 | `doctor` 显示 `.mcp-audit.toml` 是否存在，以及有效 `fail_on` / `baseline` |
| MAT2-005 | 文档同步 | README 中英文、QA 和 release checklist 说明新增成熟能力 |

## 2. Architect

### 模块边界

- `model.py`: 增加 suppressed findings 与 summary 计数。
- `baseline.py`: 负责 baseline load、filter、prune 和 rendering。
- `project_config.py`: 提供配置加载和展示所需的稳定对象。
- `cli.py`: 命令组合和参数优先级。
- `renderers/*`: 透明输出 suppressed count。

### 数据流

```text
scan -> findings -> baseline filter -> visible findings + suppressed findings -> report
baseline + current findings -> prune -> updated baseline
project config -> doctor -> effective config diagnostics
```

### 合同

- suppressed finding 不默认展开，以免重新制造噪音；但数量必须透明。
- prune 不修改原文件，除非用户显式把 `--output` 指向同一路径。
- 显式 CLI 参数继续优先于项目配置。
- baseline 维护命令不得输出 raw secret。

## 3. QA Engineer

### 必测路径

- 无 baseline 时 suppressed count 为 0。
- 使用 baseline 抑制全部 findings 后 summary findings 为 0，suppressed count 大于 0。
- Markdown 包含 suppressed count。
- SARIF properties 包含 suppressed count。
- baseline prune 删除 stale fingerprint，保留仍存在 fingerprint。
- doctor 展示项目配置存在状态和有效 scan 默认值。

## 4. Developer Plan

### Batch A: Suppression Transparency

- Extend report model with suppressed findings.
- Update baseline filter to retain suppressed findings.
- Update JSON, Markdown, SARIF renderers.
- Update tests and docs.

### Batch B: Baseline Maintenance

- Add baseline prune CLI path.
- Preserve accepted finding metadata for still-current findings.
- Add tests, README, release checklist updates.

### Batch C: Config Diagnostics

- Extend doctor with project config visibility.
- Add tests and CI smoke.
- Run completion gate and wait for remote CI.

## 5. Completion Gate

- OPT plan exists before implementation.
- Local tests pass.
- JSON/SARIF smoke passes.
- Markdown fences and `git diff --check` pass.
- Each completed batch is committed and pushed.
- Remote GitHub CI passes on final commit.
