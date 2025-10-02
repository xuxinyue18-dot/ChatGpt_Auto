# Codex Installer 使用指南

`scripts/codex_installer.py` 是一个用于在自定义目录中下载并安装 Codex CLI 的实用脚本，同时可选地触发登录流程。本文档介绍脚本的工作流程、可配置选项以及常见使用场景，帮助你快速完成 Codex CLI 的部署。

## 环境要求

- Python 3.8 及以上版本。
- 可访问 `https://download.openai.com` 的网络环境，以便下载 Codex CLI 安装包。
- 在 Windows 平台上运行时，建议在支持 POSIX 的终端（如 PowerShell、Git Bash）执行，以便正确处理脚本生成的启动器。

## 基本用法

```bash
python scripts/codex_installer.py [选项]
```

默认情况下脚本会：

1. 自动识别当前操作系统与 CPU 架构，并从默认映射表中选取合适的 Codex CLI 下载链接。
2. 将安装包下载到临时目录并解压到 `~/codex-cli` 目录（可通过 `--install-dir` 修改）。
3. 查找并赋予 Codex CLI 主程序可执行权限。
4. 在安装目录中生成 `codex-launcher.sh` 启动器与 `codex-path.sh` PATH 追加脚本。
5. 若未指定 `--skip-launch`，自动执行 `codex login` 触发交互式登录。

完成后，脚本会输出安装目录、启动脚本以及 PATH 追加脚本的位置。

## 命令行选项

| 选项 | 说明 |
|------|------|
| `--install-dir PATH` | 指定安装目录，默认 `~/codex-cli`。目录存在且非空时需搭配 `--force` 才会覆盖。|
| `--download-url URL` | 覆盖默认下载链接，适用于测试渠道或离线环境。|
| `--force` | 强制清理既有安装目录后重新安装。|
| `--skip-launch` | 安装完成后不自动运行 `codex login`。|
| `--binary-name NAME` | 指定安装包中 Codex CLI 可执行文件的名称，默认 `codex`。Windows 环境会自动兼容 `.exe`。|
| `--channel NAME` | 仅用于日志输出，标记本次安装所使用的逻辑渠道名称，默认 `latest`。|

## 常见场景

### 指定安装目录

```bash
python scripts/codex_installer.py --install-dir /opt/codex-cli
```

### 使用自定义下载源

```bash
python scripts/codex_installer.py \
  --download-url https://example.com/codex-cli-custom.tar.gz
```

### 覆盖已有安装并跳过登录

```bash
python scripts/codex_installer.py --force --skip-launch
```

## 安装后的步骤

- 将安装目录加入 PATH：
  ```bash
  source ~/codex-cli/codex-path.sh
  ```
- 或直接执行脚本生成的启动器：
  ```bash
  ~/codex-cli/codex-launcher.sh
  ```
- 如需再次登录，可运行：
  ```bash
  ~/codex-cli/codex login
  ```

## 常见问题排查

- **提示目录非空**：使用 `--force` 覆盖旧安装，或改用其他 `--install-dir`。
- **找不到可执行文件**：确认下载包结构是否包含 `codex` 或指定的 `--binary-name`。
- **登录流程退出码非零**：检查终端网络连通性以及 Codex CLI 凭据是否有效，可搭配 `--skip-launch` 手动稍后登录。

更多细节可参考脚本源码 `scripts/codex_installer.py`，以了解具体实现逻辑与错误处理方式。
