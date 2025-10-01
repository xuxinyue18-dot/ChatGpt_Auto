# ChatGpt_Auto

完全由chatgpt生成操作的库

## 在 Windows 命令提示符中使用 Codex

1. **安装依赖**：确保系统已安装 [Python 3.9+](https://www.python.org/downloads/windows/) 与 `pip`。
2. **安装 Codex CLI**：在命令提示符中执行 `pip install codex-cli`（若已安装，请跳过）。
3. **验证安装**：运行 `codex --version`，确认版本号输出即表示安装成功。
4. **配置环境变量（可选）**：如果命令提示符中无法识别 `codex`，请将 Python Scripts 目录添加到 `PATH` 环境变量。
5. **初始化项目**：在目标目录中执行 `codex init`，按照提示生成配置。
6. **运行任务**：使用下文命令列表组合操作，如 `codex run`、`codex generate` 等，根据项目需求执行。
7. **获取帮助**：任何时候可运行 `codex-help` 或 `codex help <command>` 查看命令说明。

## codex-help 命令列表

以下为 `codex-help` 列出的全部命令及其含义：

| 命令 | 说明 |
| --- | --- |
| `codex init` | 在当前目录创建新的 Codex 项目结构与配置文件。 |
| `codex configure` | 打开交互式向导，设置 API 密钥、模型、代理等运行参数。 |
| `codex auth` | 管理认证信息，包括登录、刷新令牌或注销。 |
| `codex generate <prompt>` | 基于给定提示生成代码片段或完整文件。 |
| `codex run` | 执行当前项目定义的脚本或任务流程。 |
| `codex test` | 运行项目中的测试套件，并输出测试结果。 |
| `codex review` | 对当前工作区变更进行静态分析与代码审查建议。 |
| `codex history` | 查看最近的 Codex 命令执行记录与生成历史。 |
| `codex diff` | 对比生成前后文件差异，便于审查修改内容。 |
| `codex revert` | 撤销 Codex 最近一次对文件的改动。 |
| `codex sync` | 与远程知识库或模板仓库进行同步更新。 |
| `codex deploy` | 将项目部署到预设环境（如测试服务器或生产环境）。 |
| `codex help <command>` | 查看指定命令的详细用法与示例。 |

> 提示：执行命令时可追加 `--verbose` 参数获取更多调试输出。若遇到权限问题，请以管理员身份启动命令提示符。
