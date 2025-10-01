# Codex CLI

Codex CLI 是一个命令行工具，允许开发者通过自然语言驱动的方式与 Codex Agent 进行交互式或非交互式协作。本文档按照官方帮助信息的格式整理，并补充了核心命令、常用选项的解释以及典型应用案例，帮助你快速上手。

## 使用方式

```
Codex CLI 
 
Usage: codex [OPTIONS] [PROMPT]
       codex [OPTIONS] [PROMPT] <COMMAND>

Commands:
  exec        Run Codex non-interactively [aliases: e]
  login       Manage login
  logout      Remove stored authentication credentials
  mcp         [experimental] Run Codex as an MCP server and manage MCP servers
  proto       Run the Protocol stream via stdin/stdout [aliases: p]
  completion  Generate shell completion scripts
  debug       Internal debugging commands
  apply       Apply the latest diff produced by Codex agent as a `git apply` to your local working tree [aliases: a]
  resume      Resume a previous interactive session (picker by default; use --last to continue the most recent)
  help        Print this message or the help of the given subcommand(s)

Arguments:
  [PROMPT]  Optional user prompt to start the session

Options:
  -c, --config <key=value>
          Override a configuration value that would otherwise be loaded from `~/.codex/config.toml`. Use a dotted path
          (`foo.bar.baz`) to override nested values. The `value` portion is parsed as JSON. If it fails to parse as
          JSON, the raw string is used as a literal
  -i, --image <FILE>...
          Optional image(s) to attach to the initial prompt
  -m, --model <MODEL>
          Model the agent should use
      --oss
          Convenience flag to select the local open source model provider. Equivalent to -c model_provider=oss; verifies
          a local Ollama server is running
  -p, --profile <CONFIG_PROFILE>
          Configuration profile from config.toml to specify default options
  -s, --sandbox <SANDBOX_MODE>
          Select the sandbox policy to use when executing model-generated shell commands [possible values: read-only,
          workspace-write, danger-full-access]
  -a, --ask-for-approval <APPROVAL_POLICY>
          Configure when the model requires human approval before executing a command [possible values: untrusted,
          on-failure, on-request, never]
      --full-auto
          Convenience alias for low-friction sandboxed automatic execution (-a on-failure, --sandbox workspace-write)
      --dangerously-bypass-approvals-and-sandbox
          Skip all confirmation prompts and execute commands without sandboxing. EXTREMELY DANGEROUS. Intended solely
          for running in environments that are externally sandboxed
  -C, --cd <DIR>
          Tell the agent to use the specified directory as its working root
      --search
          Enable web search (off by default). When enabled, the native Responses `web_search` tool is available to the
          model (no per‑call approval)
  -h, --help
          Print help (see more with '--help')
  -V, --version
          Print version
```

## 命令与功能详解

- **exec / e**：在非交互模式下运行 Codex，适合执行单条自然语言任务脚本。
- **login / logout**：管理 Codex 的认证凭据，确保命令调用具备合法身份。
- **mcp**：以 MCP 服务器模式运行 Codex，便于与外部多模态控制平面集成（实验功能）。
- **proto / p**：通过标准输入输出直接操作协议流，适用于自定义集成场景。
- **completion**：为常见 Shell（Bash、Zsh 等）生成自动补全脚本，提高命令效率。
- **apply / a**：将 Codex Agent 输出的最新 diff 直接应用到本地工作区，便于快速同步修改。
- **resume**：恢复上一段交互会话，可使用 `--last` 继续最近一次的上下文。
- **help**：查看全局帮助或特定子命令的帮助信息。

## 常见选项说明

- `--config`：临时覆盖配置文件中的任意键值，支持 JSON 解析，适合快速切换模型、代理等设置。
- `--image`：为提示词附加图片，增强多模态理解能力。
- `--model` / `--oss`：指定所用模型或启用本地开源模型提供方（需本地 Ollama 服务）。
- `--profile`：切换到指定的配置档案，方便在不同项目之间共享预设。
- `--sandbox` 与 `--ask-for-approval`：组合使用以控制命令执行权限和审批策略，从安全到全自动皆可覆盖。
- `--full-auto` 与 `--dangerously-bypass-approvals-and-sandbox`：快速进入自动化模式，后一选项仅建议在外部环境已做隔离时使用。
- `--cd`：在启动时切换工作目录，免去后续 `cd` 操作。
- `--search`：启用内置 Web 搜索工具，在具备网络的环境下扩展信息获取能力。

## 应用案例

1. **自动化脚本执行**：结合 `codex exec "为项目生成 README"`，在 CI/CD 中自动生成文档或代码片段。
2. **安全受控的命令执行**：在生产环境使用 `--sandbox read-only` 与 `-a on-request`，确保每一步命令都需人工确认。
3. **多模态协助**：通过 `codex -i diagram.png "分析该架构图"`，快速获得对设计图的解析与建议。
4. **团队协作配置**：使用 `--profile team-dev`，让团队成员共享统一的模型、审批和沙箱策略。
5. **恢复上下文继续工作**：当网络中断时，通过 `codex resume --last` 继续最近一次未完成的对话或任务。

## 相关资源

- [Codex CLI 文档](https://developers.openai.com/codex/cli/)
- [Ollama 本地模型服务](https://ollama.ai/)：启用 `--oss` 时的依赖环境

> 提示：首次使用前，请确保已通过 `codex login` 完成授权，并在受信任的环境中慎用危险选项。
