# Codex Installer 脚本指南

`scripts/codex_installer.py` 是一款跨平台辅助脚本，可自动下载、解压并初始化 Codex CLI。最新版支持选择发布渠道（`latest`、`stable`、`nightly` 等），并在需要时覆盖默认下载地址，帮助你在企业镜像或离线环境中快速部署。

## 功能总览

- **智能平台识别**：根据 `platform.system()` 与 `platform.machine()` 匹配官方发行包，涵盖主流 macOS、Linux、Windows x64/AArch64 平台。
- **安全解压**：所有归档在释放前均进行路径校验，防止 Zip Slip/Tar Slip。
- **PATH 快速集成**：自动生成 `codex-launcher.sh` 与 `codex-path.sh`，便于即刻启动或写入 Shell Profile。
- **可选登录流程**：安装完成后默认调用 `codex login`，也可通过 `--skip-launch` 跳过。
- **自定义渠道/镜像**：`--channel` 会在下载 URL 中替换路径段，适配 `latest`、`stable`、`nightly` 等分发；若提供 `--download-url` 则完全使用自定义链接。

## 运行前提

- Python 3.8 及以上版本。
- 可访问 `https://download.openai.com`，或提供企业内网镜像。
- Windows 用户建议在 PowerShell 或 Git Bash 中运行，确保生成的 Shell 启动器能被正确执行。

## 快速开始

```bash
python scripts/codex_installer.py
```

默认流程：

1. 检测操作系统/架构并拼接下载地址（默认渠道 `latest`）。
2. 下载并解压到 `~/codex-cli`。
3. 为 CLI 二进制赋予可执行权限。
4. 生成 `codex-launcher.sh`（启动器）与 `codex-path.sh`（PATH 片段）。
5. 自动执行 `codex login`，完成凭据授权（可用 `--skip-launch` 关闭）。

完成后终端会提示二进制位置、启动脚本路径以及如何加入 PATH。

## 命令行选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--install-dir PATH` | 安装目录，目录已存在且非空时需配合 `--force`。 | `~/codex-cli` |
| `--download-url URL` | 完全覆盖下载地址，常用于离线/镜像环境。 | 自动推断 |
| `--force` | 清空目标目录后重新安装。 | `False` |
| `--skip-launch` | 安装后不自动执行 `codex login`。 | `False` |
| `--binary-name NAME` | 安装包内 CLI 主程序名称。Windows 会自动匹配 `.exe`。 | `codex` |
| `--channel NAME` | 发行渠道标识，会注入到默认下载 URL 中。 | `latest` |

## 典型使用场景

### 安装 nightly 版本

```bash
python scripts/codex_installer.py --channel nightly
```

### 强制覆盖旧版本并跳过登录

```bash
python scripts/codex_installer.py --force --skip-launch
```

### 使用企业镜像

```bash
python scripts/codex_installer.py \
  --channel stable \
  --download-url https://mirror.example.com/codex-cli-linux-x64.tar.gz
```

### 指定自定义二进制名

```bash
python scripts/codex_installer.py --binary-name codex-cli
```

## 常见问题

- **提示目录非空**：添加 `--force` 或选择新的 `--install-dir`。
- **找不到二进制**：确认安装包内文件名与 `--binary-name` 一致，Windows 需包含 `.exe` 扩展名。
- **登录失败**：检查网络连接、账户权限；若在自动化环境，可加 `--skip-launch` 后手动登录。
- **未知平台**：脚本无法推断下载地址时，请显式提供 `--download-url` 对应包。

更多细节请查阅源码 [`scripts/codex_installer.py`](codex_installer.py)。
