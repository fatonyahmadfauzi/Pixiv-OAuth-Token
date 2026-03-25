#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION_JSON = ROOT / "version.json"
CLI_FILE = ROOT / "app" / "pixiv_login.py"
GUI_FILE = ROOT / "app" / "pixiv_login_gui.py"
RUNTIME_VERSION_FILE = ROOT / "app" / "pixiv_login_version.txt"


def _load_identity() -> tuple[str, str]:
    if not VERSION_JSON.exists():
        return "1.0.0", "REL-LOCAL"
    data = json.loads(VERSION_JSON.read_text(encoding="utf-8"))
    version = str(data.get("version", "1.0.0")).strip()
    build_code = str(data.get("build_code", "REL-LOCAL")).strip() or "REL-LOCAL"
    return version, build_code


def _replace_constant(path: Path, name: str, value: str) -> None:
    text = path.read_text(encoding="utf-8")
    pattern = rf'^{name}\s*=\s*".*?"\s*$'
    repl = f'{name} = "{value}"'
    new_text, count = re.subn(pattern, repl, text, flags=re.MULTILINE)
    if count == 0:
        raise RuntimeError(f"Constant {name} not found in {path}")
    path.write_text(new_text, encoding="utf-8")


def _ensure_gui_constants(path: Path, version: str, build_code: str) -> None:
    text = path.read_text(encoding="utf-8")
    if re.search(r"^APP_VERSION\s*=", text, flags=re.MULTILINE):
        text = re.sub(r'^APP_VERSION\s*=\s*".*?"\s*$', f'APP_VERSION = "v{version}"', text, flags=re.MULTILINE)
    else:
        marker = 'DEVELOPER_NAME = "Fatony Ahmad Fauzi"\n'
        text = text.replace(marker, marker + f'APP_VERSION = "v{version}"\nAPP_BUILD_CODE = "{build_code}"\n', 1)

    if re.search(r"^APP_BUILD_CODE\s*=", text, flags=re.MULTILINE):
        text = re.sub(r'^APP_BUILD_CODE\s*=\s*".*?"\s*$', f'APP_BUILD_CODE = "{build_code}"', text, flags=re.MULTILINE)

    path.write_text(text, encoding="utf-8")


def main() -> None:
    version, build_code = _load_identity()
    _replace_constant(CLI_FILE, "APP_VERSION", f"v{version}")
    _replace_constant(CLI_FILE, "APP_BUILD_CODE", build_code)
    _ensure_gui_constants(GUI_FILE, version, build_code)
    RUNTIME_VERSION_FILE.write_text(
        json.dumps({"version": f"v{version}", "build_code": build_code}, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Synced identity: v{version} / {build_code}")


if __name__ == "__main__":
    main()
