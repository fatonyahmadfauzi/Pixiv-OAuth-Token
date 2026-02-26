#!/usr/bin/env bash
set -euo pipefail
python3 -m pip install -r requirements.txt
pyinstaller --onefile --name pixiv_login pixiv_login.py
echo "Build done. Check dist/pixiv_login"
