# Codex Installer 使用指南

`scripts/codex_installer.py` 是一个跨平台的辅助脚本，用于在自定义目录中下载、解压并初始化 Codex CLI。脚本会自动识别当前操作系统与 CPU 架构，为你挑选匹配的安装包，并在安装完成后可选地发起 `codex login` 登陆流程。

## 脚本亮点

- **自动平台识别**：基于 `platform.system()`/`platform.machine()` 映射到预设下载链接，无需手动判断。对 Windows、macOS（Intel/Apple Silicon）与主流 Linux 架构均提供默认包。 
- **安全解压**：使用 `_is_within_directory` 校验，阻止压缩包中的目录穿越（Zip Slip/Tar Slip）风险。
- **使用体验友好**：生成 `codex-launcher.sh` 及 `codex-path.sh`，方便快速启动或将 CLI 加入 PATH。
- **可控的覆盖策略**：在安装目录非空时默认保护已有文件，可通过 `--force` 明确覆盖。

## 环境要求

- Python 3.8 或更高版本。
- 可访问 `https://download.openai.com` 的网络环境，以下载 Codex CLI 安装包。
- Windows 用户建议在 PowerShell 或 Git Bash 等支持 POSIX 行为的终端中运行，以正确处理脚本生成的 Shell 启动器。

## 快速开始

```bash
python scripts/codex_installer.py
```

默认行为包括：

1. 检测系统及架构，并匹配默认下载链接。
2. 将安装包下载到临时目录并解压到 `~/codex-cli`。
3. 确保 CLI 二进制具有可执行权限。
4. 在安装目录生成 `codex-launcher.sh` 与 `codex-path.sh`。
5. 自动调用 `codex login` 完成交互式登录（除非设置 `--skip-launch`）。

完成后，终端会输出 CLI 二进制、启动脚本及 PATH 片段的位置。

## 命令行选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--install-dir PATH` | 指定安装目录。目录存在且非空时需搭配 `--force` 才会覆盖。 | `~/codex-cli` |
| `--download-url URL` | 覆盖默认下载链接，适用于私有镜像或离线环境。 | 根据系统自动选择 |
| `--force` | 强制清理目标目录后重新安装。 | `False` |
| `--skip-launch` | 安装完成后不自动运行 `codex login`。 | `False` |
| `--binary-name NAME` | 指定解压后 CLI 的文件名。Windows 环境自动兼容 `.exe` 后缀。 | `codex` |
| `--channel NAME` | 日志标记，便于记录安装来源（不影响功能）。 | `latest` |

## 核心流程解析

1. **准备安装目录**：通过 `ensure_install_dir` 创建或清理目录，除非显式传入 `--force`，否则保护非空目录。
2. **下载与解压**：在临时目录下载压缩包，支持 `.tar.gz`、`.tgz` 与 `.zip`，并在解压时验证路径安全性。
3. **二进制定位**：递归搜索解压结果中与 `--binary-name` 匹配的文件，确保 CLI 主程序就绪。
4. **辅助脚本生成**：
   - `codex-launcher.sh` 会设置 `PATH` 并执行 CLI 主程序。
   - `codex-path.sh` 为 Shell Profile 准备 PATH 追加语句。
5. **可选登录**：除非设置 `--skip-launch`，脚本会调用 `codex login` 并将退出码返回给调用者。

## 使用案例

### 1. 安装到自定义路径

在容器或服务器上部署时，可指定绝对路径：

```bash
python scripts/codex_installer.py --install-dir /opt/tools/codex-cli
```

### 2. 离线环境先行下载

配合内网镜像或预下载的安装包：

```bash
python scripts/codex_installer.py \
  --download-url https://intranet.example.com/codex/codex-cli-linux-x64.tar.gz \
  --channel internal
```

### 3. 仅升级 CLI，稍后再登录

当仅需覆盖旧版本而暂时无法登录时：

```bash
python scripts/codex_installer.py --force --skip-launch
```

稍后可通过生成的启动器手动登录：

```bash
~/codex-cli/codex-launcher.sh login
```

### 4. 指定非默认二进制名称

如果下载包中 CLI 主程序命名为 `codex-cli`：

```bash
python scripts/codex_installer.py --binary-name codex-cli
```

### 5. Windows PowerShell 示例

```powershell
py scripts\codex_installer.py --install-dir C:\Codex --skip-launch
& "C:\Codex\codex-launcher.sh" login
```

## 安装后操作

- 将 CLI 加入当前会话 PATH：
  ```bash
  source ~/codex-cli/codex-path.sh
  ```
- 或直接使用启动器运行 Codex CLI：
  ```bash
  ~/codex-cli/codex-launcher.sh
  ```
- 重新登录：
  ```bash
  ~/codex-cli/codex login
  ```

## 常见问题排查

- **提示目录非空**：添加 `--force` 或更换 `--install-dir`。
- **找不到可执行文件**：确认压缩包内的文件名与 `--binary-name` 对应，或在 Windows 平台确保带有 `.exe` 后缀。
- **登录流程退出码非零**：检查网络连接及账户权限，可先加 `--skip-launch` 再手动执行登录。
- **不支持的平台**：当 `detect_platform` 无法匹配默认链接时，需手动提供 `--download-url` 指向合适的安装包。

有关更详细的实现逻辑与异常处理，请参考源码 `scripts/codex_installer.py`。
