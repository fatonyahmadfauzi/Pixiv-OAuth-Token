#!/usr/bin/env python
import json, os

ROOT = os.path.dirname(__file__)
VERSION_FILE = os.path.join(ROOT, "version.json")
OUT_FILE = os.path.join(ROOT, "version_info.txt")

# Edit these if you want:
COMPANY = "Fatony Ahmad Fauzi Dev"
PRODUCT = "Pixiv Login CLI"
DESCRIPTION = "Pixiv OAuth Login Tool"
INTERNAL = "pixiv_login_plus"
ORIGINAL = "pixiv_login_plus.exe"

def ver_tuple(v: str):
    parts = (v.split(".") + ["0","0","0","0"])[:4]
    return tuple(int(x) for x in parts)

def main():
    with open(VERSION_FILE, "r", encoding="utf-8") as f:
        v = json.load(f)["version"]

    fv = ver_tuple(v)
    filevers = f"({fv[0]},{fv[1]},{fv[2]},0)"
    prodvers = filevers

    content = (
        "# UTF-8\n"
        "VSVersionInfo(\n"
        "  ffi=FixedFileInfo(\n"
        f"    filevers={filevers},\n"
        f"    prodvers={prodvers},\n"
        "    mask=0x3f,\n"
        "    flags=0x0,\n"
        "    OS=0x40004,\n"
        "    fileType=0x1,\n"
        "    subtype=0x0,\n"
        "    date=(0, 0)\n"
        "  ),\n"
        "  kids=[\n"
        "    StringFileInfo(\n"
        "      [\n"
        "        StringTable(\n"
        "          '040904B0',\n"
        "          [StringStruct('CompanyName', '" + COMPANY + "'),\n"
        "           StringStruct('FileDescription', '" + DESCRIPTION + "'),\n"
        "           StringStruct('FileVersion', '" + v + "'),\n"
        "           StringStruct('InternalName', '" + INTERNAL + "'),\n"
        "           StringStruct('OriginalFilename', '" + ORIGINAL + "'),\n"
        "           StringStruct('ProductName', '" + PRODUCT + "'),\n"
        "           StringStruct('ProductVersion', '" + v + "')])\n"
        "      ]),\n"
        "    VarFileInfo([VarStruct('Translation', [1033, 1200])])\n"
        "  ]\n"
        ")\n"
    )

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Wrote {OUT_FILE} (version {v})")

if __name__ == "__main__":
    main()
