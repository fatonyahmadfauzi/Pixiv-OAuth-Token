#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION_JSON = ROOT / "version.json"
LATEST_JSON = ROOT / "latest.json"
REPO = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token"
DOWNLOAD = f"{REPO}/releases/latest/download"


def main() -> None:
    payload = json.loads(VERSION_JSON.read_text(encoding="utf-8"))
    version = str(payload.get("version", "1.0.0")).strip()
    build_code = str(payload.get("build_code", "REL-LOCAL")).strip() or "REL-LOCAL"

    manifest = {
        "version": version,
        "build_code": build_code,
        "published_at": None,
        "notes_url": f"{REPO}/releases/latest",
        "assets": {
            "cli_portable": {
                "x86": f"{DOWNLOAD}/Pixiv%20OAuth%20CLi%20(Portable)%20x86_latest.exe",
                "x64": f"{DOWNLOAD}/Pixiv%20OAuth%20CLi%20(Portable)%20x64_latest.exe",
                "arm64": f"{DOWNLOAD}/Pixiv%20OAuth%20CLi%20(Portable)%20ARM64_latest.exe",
            },
            "gui_portable": {
                "x86": f"{DOWNLOAD}/Pixiv%20OAuth%20GUi%20(Portable)%20x86_latest.exe",
                "x64": f"{DOWNLOAD}/Pixiv%20OAuth%20GUi%20(Portable)%20x64_latest.exe",
                "arm64": f"{DOWNLOAD}/Pixiv%20OAuth%20GUi%20(Portable)%20ARM64_latest.exe",
            },
            "cli_setup": {
                "x86": f"{DOWNLOAD}/Pixiv%20OAuth%20CLi%20Setup%20x86_latest.exe",
                "x64": f"{DOWNLOAD}/Pixiv%20OAuth%20CLi%20Setup%20x64_latest.exe",
                "arm64": f"{DOWNLOAD}/Pixiv%20OAuth%20CLi%20Setup%20ARM64_latest.exe",
            },
            "gui_setup": {
                "x86": f"{DOWNLOAD}/Pixiv%20OAuth%20GUi%20Setup%20x86_latest.exe",
                "x64": f"{DOWNLOAD}/Pixiv%20OAuth%20GUi%20Setup%20x64_latest.exe",
                "arm64": f"{DOWNLOAD}/Pixiv%20OAuth%20GUi%20Setup%20ARM64_latest.exe",
            },
            "release_zip": f"{DOWNLOAD}/PixivOAuthRelease_v{version}_{build_code}.zip",
        },
    }

    LATEST_JSON.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {LATEST_JSON} ({version} / {build_code})")


if __name__ == "__main__":
    main()
