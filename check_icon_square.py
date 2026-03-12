#!/usr/bin/env python3
"""Validate ICO has square frames to avoid stretched icons in Windows."""
import struct
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_icon_square.py <icon.ico>")
        return 2

    icon_path = Path(sys.argv[1])
    if not icon_path.exists():
        print(f"[ERROR] Icon file not found: {icon_path}")
        return 1

    data = icon_path.read_bytes()
    if len(data) < 6:
        print(f"[ERROR] Invalid ICO header: {icon_path}")
        return 1

    _reserved, icon_type, count = struct.unpack_from("<HHH", data, 0)
    if icon_type != 1 or count <= 0:
        print(f"[ERROR] Invalid ICO metadata: {icon_path}")
        return 1

    bad = []
    for i in range(count):
        w, h = struct.unpack_from("<BB", data, 6 + i * 16)
        w = 256 if w == 0 else w
        h = 256 if h == 0 else h
        if w != h:
            bad.append(f"{w}x{h}")

    if bad:
        print("[ERROR] Icon frames must be square (w==h) to avoid stretched logo:", ", ".join(bad))
        return 1

    print(f"[OK] Icon frames are square: {icon_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())