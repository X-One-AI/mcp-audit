# mcp-audit

[![CI](https://github.com/X-One-AI/mcp-audit/actions/workflows/ci.yml/badge.svg)](https://github.com/X-One-AI/mcp-audit/actions/workflows/ci.yml)

语言：[English](./README.md) | 中文

扫描 MCP 和 AI agent 配置中的高风险权限、明文密钥、不安全命令和 CI 安全风险。

## 目的

`mcp-audit` 是 X-One 的第一个活跃项目。

它帮助团队在 AI agent 接触代码仓库、终端、凭据、CI 任务或内部系统之前，审查 MCP 工具和 AI agent 工作流的安全风险。

## 定位

```text
Agentic DevSecOps / Safe Agent Operations
```

`mcp-audit` 不是运行时沙箱，也不声称能阻止所有攻击。第一个版本是本地优先的审计工具，输出可执行、易审查的风险报告。

## 目标用户

```text
- 使用 MCP 工具的开发者
- 正在采用 AI coding agents 的团队
- DevTools 和平台工程师
- DevSecOps 和安全平台团队
- 希望在工程流程中使用 AI agents 但不盲目信任的创始人
```

## MVP 范围

第一个版本应该把四件事做好：

```text
1. 读取 MCP / agent 配置文件
2. 检测高信号风险
3. 生成 Markdown、JSON 和 SARIF 报告
4. 用具体修复建议解释每条规则
```

## 第一批规则方向

```text
- 明文密钥
- 不安全 shell / exec / eval 使用
- 未固定版本的远程包执行
- 过宽的文件系统访问
- 不受限制的网络访问
- 过宽的环境变量暴露
- 危险容器启动参数
- CI 和 PR 安全缺口
```

## CLI 示例

```bash
mcp-audit doctor
mcp-audit init
mcp-audit scan
mcp-audit scan --config ./mcp.json
mcp-audit scan --config ./agent.yaml
mcp-audit scan --config ./agent.toml
mcp-audit scan --format markdown
mcp-audit scan --format json
mcp-audit scan --format sarif --output mcp-audit.sarif
mcp-audit scan --fail-on high
mcp-audit baseline --config ./mcp.json --output .mcp-audit-baseline.json
mcp-audit scan --config ./mcp.json --baseline .mcp-audit-baseline.json --fail-on high
mcp-audit baseline --config ./mcp.json --baseline .mcp-audit-baseline.json --prune --output .mcp-audit-baseline.json
mcp-audit rules
mcp-audit explain XONE001
```

## 安装

在本仓库中运行：

```bash
python3 -m pip install -e .
mcp-audit --version
```

如果你的 Python 环境因为网络或证书限制无法拉取构建依赖，请先使用下面的本地开发命令，直到 packaging 依赖可用。

不传 `--config` 时，`scan` 只检查有限的默认位置：

```text
mcp.json
.mcp.json
mcp.yaml
mcp.yml
agent.yaml
agent.yml
agent.toml
.cursor/mcp.json
.vscode/mcp.json
.claude/mcp.json
.continue/config.json
.continue/config.yaml
```

它不会递归扫描整个仓库。显式 `--config` 支持 JSON、YAML 和 TOML object 配置。

## 项目配置

创建项目配置：

```bash
mcp-audit init
```

该命令会写入 `.mcp-audit.toml`：

```toml
[scan]
fail_on = "high"
baseline = ".mcp-audit-baseline.json"
```

显式 CLI 参数优先级高于项目配置。
可以用 `mcp-audit doctor` 检查配置文件是否被识别，以及当前生效的 scan 默认值。

## 本地开发

在本目录运行：

```bash
python3 -m pip install -e ".[dev]"
python3 -m pytest tests -q
PYTHONPATH=src python3 -m mcp_audit.cli --version
PYTHONPATH=src python3 -m mcp_audit --version
PYTHONPATH=src python3 -m mcp_audit.cli doctor
PYTHONPATH=src python3 -m mcp_audit.cli init
PYTHONPATH=src python3 -m mcp_audit.cli scan --config examples/high-risk-mcp.json --format markdown
PYTHONPATH=src python3 -m mcp_audit.cli scan --config examples/high-risk-mcp.json --format json
PYTHONPATH=src python3 -m mcp_audit.cli scan --config examples/high-risk-mcp.json --format sarif
PYTHONPATH=src python3 -m mcp_audit.cli rules
```

只在包含默认配置路径之一的仓库里使用不带 `--config` 的 `scan`。

CLI 本地优先。它不会上传配置、发送遥测，也不会执行被扫描的命令。

CI 可以先从这个命令开始：

```bash
mcp-audit scan --config ./mcp.json --format sarif --output mcp-audit.sarif --fail-on high
```

对于已有仓库中已经审查并接受的 findings，可以创建 baseline：

```bash
mcp-audit baseline --config ./mcp.json --output .mcp-audit-baseline.json
mcp-audit scan --config ./mcp.json --baseline .mcp-audit-baseline.json --fail-on high
```

baseline 更新应当进入代码审查。baseline 是风险接受记录，不代表 finding 本身安全。
当 baseline 抑制 findings 时，报告 summary 仍会显示被抑制的 finding 数量。
如果要移除当前扫描中已经不存在的 accepted findings，可以 prune baseline：

```bash
mcp-audit baseline --config ./mcp.json --baseline .mcp-audit-baseline.json --prune --output .mcp-audit-baseline.json
```

Markdown 面向人工审查。JSON 和 SARIF 面向自动化。

## 非目标

```text
- v0.1 不做运行时策略执行
- v0.1 不做 dashboard
- v0.1 不做 hosted service
- 不声称该工具能阻止所有 MCP 或 agent 安全问题
```

## 第一个里程碑

```text
v0.1：扫描示例 MCP / agent 配置并生成有用的本地风险报告。
```

成功标准是至少三个真实用户愿意扫描自己的 MCP 或 agent 配置，并讨论结果。

## 相关文档

- [运行模型](./ops/README.md)
- [规则草案](./docs/rules.md)
- [发布检查清单](./docs/release-checklist.md)
- [高风险配置示例](./examples/high-risk-mcp.json)
