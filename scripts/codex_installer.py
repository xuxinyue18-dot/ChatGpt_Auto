#!/usr/bin/env python3
"""Utility to install Codex CLI into a custom directory and launch it."""
from __future__ import annotations

import argparse
import platform
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, Iterable, Tuple
from urllib.request import urlretrieve

# Mapping of (system, architecture) to download URLs.
DEFAULT_URLS: Dict[Tuple[str, str], str] = {
    ("Linux", "x86_64"): "https://download.openai.com/codex/cli/latest/codex-cli-linux-x64.tar.gz",
    ("Linux", "aarch64"): "https://download.openai.com/codex/cli/latest/codex-cli-linux-arm64.tar.gz",
    ("Darwin", "x86_64"): "https://download.openai.com/codex/cli/latest/codex-cli-macos-x64.zip",
    ("Darwin", "arm64"): "https://download.openai.com/codex/cli/latest/codex-cli-macos-arm64.zip",
    ("Windows", "AMD64"): "https://download.openai.com/codex/cli/latest/codex-cli-windows-x64.zip",
}


class InstallerError(RuntimeError):
    """Raised when the installation fails."""


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install the Codex CLI into a custom directory and optionally launch it."
    )
    parser.add_argument(
        "--install-dir",
        type=Path,
        default=Path.home() / "codex-cli",
        help="Target directory to install the Codex CLI (default: ~/codex-cli).",
    )
    parser.add_argument(
        "--download-url",
        help="Override the Codex CLI download URL. By default an URL is picked based on your system.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing installation without prompting.",
    )
    parser.add_argument(
        "--skip-launch",
        action="store_true",
        help="Install without launching the Codex CLI login sequence.",
    )
    parser.add_argument(
        "--binary-name",
        default="codex",
        help="Expected name of the CLI binary after extraction (default: codex).",
    )
    parser.add_argument(
        "--channel",
        default="latest",
        help="Logical release channel identifier used only for logging.",
    )
    return parser.parse_args(argv)


def detect_platform() -> Tuple[str, str]:
    system = platform.system()
    machine = platform.machine()
    if system == "Linux" and machine == "x86_64":
        machine = "x86_64"
    elif system == "Linux" and machine in {"arm64", "aarch64"}:
        machine = "aarch64"
    elif system == "Darwin" and machine == "x86_64":
        machine = "x86_64"
    elif system == "Darwin" and machine in {"arm64", "x86_64"}:
        machine = "arm64" if machine == "arm64" else machine
    elif system == "Windows" and machine in {"AMD64", "x86_64"}:
        machine = "AMD64"
    return system, machine


def ensure_install_dir(install_dir: Path, force: bool) -> None:
    if install_dir.exists():
        if any(install_dir.iterdir()) and not force:
            raise InstallerError(
                f"Install directory '{install_dir}' already exists and is not empty. "
                "Use --force to overwrite."
            )
        if force:
            shutil.rmtree(install_dir)
    install_dir.mkdir(parents=True, exist_ok=True)


def download_package(url: str, workdir: Path) -> Path:
    filename = workdir / Path(url).name
    print(f"Downloading Codex CLI package from {url} ...")
    urlretrieve(url, filename)
    print(f"Downloaded to {filename}")
    return filename


def extract_package(archive: Path, install_dir: Path, binary_name: str) -> Path:
    print(f"Extracting {archive} ...")
    if archive.suffixes[-2:] == [".tar", ".gz"] or archive.suffix == ".tgz":
        with tarfile.open(archive) as tar:
            tar.extractall(path=install_dir)
    elif archive.suffix == ".zip":
        with zipfile.ZipFile(archive) as zipf:
            zipf.extractall(path=install_dir)
    else:
        raise InstallerError(f"Unsupported archive format: {archive}")

    expected_names = {binary_name}
    if platform.system() == "Windows":
        expected_names.add(f"{binary_name}.exe")

    extracted = None
    for item in install_dir.rglob("*"):
        if item.name in expected_names:
            extracted = item
            break
    if not extracted:
        raise InstallerError(
            "Could not locate the Codex binary after extraction. "
            "Use --binary-name to specify the expected binary name if it differs."
        )
    return extracted


def create_launcher(binary_path: Path, install_dir: Path) -> Path:
    launcher = install_dir / "codex-launcher.sh"
    with launcher.open("w", encoding="utf-8") as fh:
        fh.write("#!/usr/bin/env bash\n")
        fh.write("set -euo pipefail\n")
        fh.write("SCRIPT_DIR=\"$(cd \"$(dirname '${BASH_SOURCE[0]}')\" && pwd)\"\n")
        fh.write("export PATH=\"$SCRIPT_DIR:$PATH\"\n")
        fh.write("exec \"$SCRIPT_DIR/" + binary_path.name + "\" login \"$@\"\n")
    launcher.chmod(launcher.stat().st_mode | stat.S_IEXEC)
    return launcher


def append_profile_snippet(install_dir: Path) -> Path:
    snippet = install_dir / "codex-path.sh"
    with snippet.open("w", encoding="utf-8") as fh:
        fh.write("# Source this file to add Codex CLI to your PATH\n")
        fh.write(f"export PATH=\"{install_dir}:$PATH\"\n")
    return snippet


def main(argv: Iterable[str]) -> int:
    args = parse_args(argv)
    install_dir = args.install_dir.expanduser().resolve()

    system, machine = detect_platform()
    download_url = args.download_url or DEFAULT_URLS.get((system, machine))
    if not download_url:
        raise InstallerError(
            "Unsupported platform. Please provide --download-url pointing to a Codex CLI package."
        )

    ensure_install_dir(install_dir, args.force)

    with tempfile.TemporaryDirectory() as tmp:
        archive = download_package(download_url, Path(tmp))
        binary_path = extract_package(archive, install_dir, args.binary_name)

    binary_path.chmod(binary_path.stat().st_mode | stat.S_IEXEC)

    launcher = create_launcher(binary_path, install_dir)
    profile_snippet = append_profile_snippet(install_dir)

    print(f"Codex CLI installed successfully from channel '{args.channel}'.")
    print(f"Binary location: {binary_path}")
    print(f"Launcher script: {launcher}")
    print(
        "To add Codex CLI to your PATH, run:\n"
        f"  source '{profile_snippet}'\n"
        "or append the export line to your shell profile."
    )

    if args.skip_launch:
        print("Skipping Codex CLI launch as requested.")
        return 0

    print("Launching Codex CLI login flow...")
    try:
        result = subprocess.run([
            str(binary_path),
            "login",
        ], check=True)
    except FileNotFoundError as exc:
        raise InstallerError(
            f"Unable to launch Codex CLI at {binary_path}: {exc}" "\n"
            "Ensure the package contains the expected binary name."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise InstallerError(
            "Codex CLI exited with a non-zero status during login."
        ) from exc

    return result.returncode


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except InstallerError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
