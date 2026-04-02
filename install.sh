#!/usr/bin/env bash
# =============================================================
#  Pixiv OAuth Token CLI - Quick Installer (Bash)
#  Supports: Bash, Zsh, WSL, Git Bash, macOS Terminal
#  Usage:
#    bash <(curl -sL https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/install.sh)
# =============================================================

set -e

RAW_BASE="https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master"
FILE_URL="$RAW_BASE/app/pixiv_login.py"
OUT_FILE="pixiv_login.py"

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BOLD='\033[1m'
RESET='\033[0m'

banner() {
    echo ""
    echo -e "  ${CYAN}╔══════════════════════════════════════════╗${RESET}"
    echo -e "  ${CYAN}║    Pixiv OAuth Token CLI - Installer     ║${RESET}"
    echo -e "  ${CYAN}║       by Fatony Ahmad Fauzi              ║${RESET}"
    echo -e "  ${CYAN}╚══════════════════════════════════════════╝${RESET}"
    echo ""
}

step()  { echo -e "  ${YELLOW}[*]${RESET} $1"; }
ok()    { echo -e "  ${GREEN}[+]${RESET} $1"; }
err()   { echo -e "  ${RED}[!]${RESET} $1" >&2; }

banner

# --- 1. Check Python ---
step "Checking Python installation..."

PYTHON_CMD=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        PY_VER=$("$cmd" --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
        MAJOR=$(echo "$PY_VER" | cut -d. -f1)
        MINOR=$(echo "$PY_VER" | cut -d. -f2)
        if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 11 ]; then
            PYTHON_CMD="$cmd"
            ok "Found $cmd $PY_VER"
            break
        else
            err "Found $cmd $PY_VER — requires 3.11+"
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    err "Python 3.11+ not found."
    err "Install from: https://www.python.org/downloads/"
    exit 1
fi

# --- 2. Check download tool ---
step "Checking download tool..."
if command -v curl &>/dev/null; then
    DOWNLOADER="curl"
    ok "Using curl"
elif command -v wget &>/dev/null; then
    DOWNLOADER="wget"
    ok "Using wget"
else
    err "Neither curl nor wget found. Install one and retry."
    exit 1
fi

# --- 3. Download pixiv_login.py ---
step "Downloading pixiv_login.py from GitHub..."
if [ "$DOWNLOADER" = "curl" ]; then
    curl -fsSL "$FILE_URL" -o "$OUT_FILE"
else
    wget -q "$FILE_URL" -O "$OUT_FILE"
fi
ok "Downloaded: $OUT_FILE"

# --- 4. Install dependencies ---
step "Installing dependencies (requests)..."
if "$PYTHON_CMD" -m pip install requests --quiet --disable-pip-version-check 2>/dev/null; then
    ok "requests installed"
else
    err "pip install failed. Try manually: $PYTHON_CMD -m pip install requests"
fi

# --- 5. Make executable (optional) ---
chmod +x "$OUT_FILE" 2>/dev/null || true

# --- Done ---
echo ""
echo -e "  ${GREEN}${BOLD}╔══════════════════════════════════════════╗${RESET}"
echo -e "  ${GREEN}${BOLD}║           Installation complete!         ║${RESET}"
echo -e "  ${GREEN}${BOLD}╚══════════════════════════════════════════╝${RESET}"
echo ""
echo -e "  Run with:"
echo -e "    ${CYAN}$PYTHON_CMD pixiv_login.py${RESET}"
echo ""
