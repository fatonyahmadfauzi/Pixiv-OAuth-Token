#!/usr/bin/env bash
set -eu
(set -o pipefail) 2>/dev/null || true

OUT="pixiv_login_plus_linux"

python3 -m pip install -r requirements.txt
rm -rf dist build "$OUT" *.spec
pyinstaller --onefile --name "$OUT" pixiv_login.py

mkdir -p dist_linux
cp -f "dist/$OUT" "dist_linux/$OUT"
cp -f "dist/$OUT" "$OUT"

echo "Build done."
echo "  dist_linux/$OUT"
echo "  $OUT"
