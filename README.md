# Codex CLI 使用指南

Codex CLI 是 OpenAI 官方推出的命令行体验，能够让你以“自然语言 + 命令行工具”的方式与 Codex Agent 协作。你既可以像聊天一样与代理进行多轮对话，也可以在自动化脚本中一次性触发任务。本文基于最新 Codex CLI 文档整理，聚焦核心概念、常用命令与高频场景，帮助团队更快在日常开发、运维和自动化流程中落地该工具。

## 快速安装

Codex CLI 提供 macOS、Linux 与 Windows（x64/AArch64）预编译发行包，可通过以下方式获取：

```bash
# 方式一：直接使用官方安装脚本（需 Python ≥ 3.8）
python scripts/codex_installer.py

# 方式二：手动下载解压
curl -LO https://download.openai.com/codex/cli/latest/codex-cli-linux-x64.tar.gz
mkdir -p ~/codex-cli && tar -xzf codex-cli-linux-x64.tar.gz -C ~/codex-cli
```

安装后建议将 CLI 目录加入 PATH：

```bash
source ~/codex-cli/codex-path.sh
```

首次运行前执行登录：

```bash
codex login
```

> 如果你需要安装指定渠道（如 `nightly`、`stable`）或企业内自建镜像，可使用 `scripts/codex_installer.py --channel <name>` 或 `--download-url <URL>`。详见 [scripts/README.md](scripts/README.md)。

## 命令结构速览

```text
Usage: codex [OPTIONS] [PROMPT]
       codex [OPTIONS] [PROMPT] <COMMAND>

Commands:
  exec        在非交互模式运行 Codex（别名：e）
  login       管理 Codex 账户登录
  logout      清除本地凭据
  mcp         以 MCP 服务器形式运行 Codex（实验性）
  proto       通过 stdin/stdout 直接访问协议流（别名：p）
  apply       将最新 diff 以 `git apply` 方式落地（别名：a）
  resume      恢复历史会话，可搭配 `--last`
  completion  生成 Shell 自动补全脚本
  debug       调试命令
  help        查看全局或子命令帮助
```

命令调用可选一个初始提示词 `PROMPT`，CLI 会据此与 Codex Agent 对话。如果需要自动执行 CLI 子命令，将 `PROMPT` 置于命令前，例如：

```bash
codex "请为我的项目写一个 README" exec
```

## 核心使用场景

| 场景 | 推荐命令/选项 | 说明 |
|------|---------------|------|
| 多轮协作开发 | `codex` 交互模式 + `resume` | 直接在终端与代理对话，使用 `resume --last` 延续最近上下文 |
| 单次自动化任务 | `codex exec "指令"` | 适合 CI/CD 或脚本中执行一次性任务 |
| 自动补全 | `codex completion --shell zsh` | 生成 Shell 补全文件，提高效率 |
| 快速同步 diff | `codex apply` | 将代理给出的最新补丁应用到工作区 |
| 协同安全管控 | `--sandbox`、`--ask-for-approval` | 控制命令执行权限、人工审批策略 |
| Web 搜索增强 | `--search` | 启用原生 web_search 工具（默认关闭） |

## 常用选项解读

- `-m, --model <MODEL>`：指定要使用的模型，支持官方及自建提供方。
- `--oss`：快速切换到本地开源模型提供方，要求本地 Ollama 正在运行。
- `-c, --config key=value`：覆盖 `~/.codex/config.toml` 中的任意配置项，可用点分路径访问嵌套字段，值支持 JSON。
- `-p, --profile <PROFILE>`：加载配置文件中的预设档案，便于不同项目共享默认选项。
- `-s, --sandbox <MODE>`：约束模型生成命令的执行权限，支持 `read-only`、`workspace-write`、`danger-full-access`。
- `-a, --ask-for-approval <POLICY>`：定义何时需要人工确认（`untrusted`、`on-failure`、`on-request`、`never`）。
- `--full-auto`：`-a on-failure` + `--sandbox workspace-write` 的组合捷径，适合半自动化开发。
- `--dangerously-bypass-approvals-and-sandbox`：完全跳过沙箱与确认提示，仅限在额外受控环境使用。
- `-C, --cd <DIR>`：为代理指定根工作目录，避免手动 `cd`。
- `-i, --image <FILE>`：随提示词上传图片，触发多模态分析。
- `--search`：为模型开启联网搜索能力，无需逐条批准。

## 工作流建议

1. **初始化项目助手**：使用交互模式建立上下文，让代理熟悉项目结构，必要时上传设计图或日志。
2. **严格控制执行权限**：在生产或敏感环境下结合 `--sandbox read-only` 与 `-a on-request`，确保每一步执行都可控。
3. **版本化管理 diff**：当代理给出补丁后先在临时分支或 `git apply --stat` 等命令中检查变更，再正式执行 `codex apply`。
4. **集成 CI/CD**：在流水线上使用 `codex exec` 自动生成文档、重写提交信息或执行代码审查，并根据 exit code 判断成功与否。
5. **恢复历史会话**：通过 `codex resume` 与 `codex resume --last` 找回上下文，实现“随时断线继续”。

## 常见问题

- **无法登录**：检查网络代理与防火墙，必要时使用 `codex login --interactive` 重新授权。
- **命令执行失败**：查看终端输出，若是权限问题，可调整 `--sandbox` 和审批策略。
- **找不到模型**：确认模型名称拼写正确，或先用 `codex config list-models`（若文档提供）了解可用项。
- **自动补全不起效**：确保补全脚本放入 Shell 对应路径，并重新加载配置文件。

## 延伸阅读

- [Codex CLI 官方文档](https://developers.openai.com/codex/cli/)
- [OpenAI 平台文档](https://platform.openai.com/docs)
- [Ollama 本地模型服务](https://ollama.ai/)

> 提醒：在任何自动化场景中，请谨慎使用跳过审批或关闭沙箱的选项，避免对生产环境造成不可控影响。
