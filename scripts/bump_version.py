#!/usr/bin/env python
import json, os, sys, re
from datetime import datetime, timezone

VERSION_FILE = os.path.join(os.path.dirname(__file__), "..", "version.json")

def parse(v: str):
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)$", v.strip())
    if not m:
        raise ValueError(f"Invalid version '{v}'. Expected X.Y.Z")
    return [int(m.group(1)), int(m.group(2)), int(m.group(3))]

def main():
    bump = sys.argv[1].lower() if len(sys.argv) >= 2 else "patch"

    data: dict = {"version": "1.0.0", "build_code": "BUILD-UNKNOWN"}
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            if isinstance(loaded, dict):
                data.update(loaded)

    major, minor, patch = parse(data.get("version", "1.0.0"))

    if bump == "major":
        major += 1; minor = 0; patch = 0
    elif bump == "minor":
        minor += 1; patch = 0
    elif bump == "patch":
        patch += 1
    elif bump == "none":
        pass
    else:
        raise SystemExit("Usage: python bump_version.py [major|minor|patch|none]")

    data["version"] = f"{major}.{minor}.{patch}"
    if bump != "none":
        now_utc = datetime.now(timezone.utc)
        unix_ms = int(now_utc.timestamp() * 1000)
        data["build_code"] = f"REL-U{unix_ms}"
    elif not data.get("build_code"):
        data["build_code"] = "BUILD-UNKNOWN"

    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"{data['version']}|{data['build_code']}")

if __name__ == "__main__":
    main()
