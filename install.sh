#!/usr/bin/env bash
# =============================================================
#  Pixiv OAuth Token CLI - Quick Installer (Bash)
#  Supports: Bash, Zsh, WSL, Git Bash, macOS Terminal
#  Usage:
#    bash <(curl -sL https://raw.githubusercontent.com/.../install.sh)
#    bash <(curl -sL https://raw.githubusercontent.com/.../install.sh) --lang jp
#    PIXIV_LANG=jp bash <(curl -sL https://raw.githubusercontent.com/.../install.sh)
# =============================================================
#  Supported --lang values: en, jp, kr, zh, id, de, fr, es, ru, pt, pl
# =============================================================

set -e

RAW_BASE="https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master"
FILE_URL="$RAW_BASE/app/pixiv_login.py"
OUT_FILE="pixiv_login.py"

# ---- Language detection ----
# Priority: --lang flag > $PIXIV_LANG env > $LANG/$LC_ALL OS env > English
RESOLVED_LANG="en"
SUPPORTED_LANGS="en jp kr zh id de fr es ru pt pl"

# Helper: map POSIX locale string to our lang code
map_locale_to_lang() {
  local loc
  loc=$(echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/_/-/g' | cut -d. -f1)
  case "$loc" in
    ja|ja-jp)   echo "jp" ;;
    ko|ko-kr)   echo "kr" ;;
    zh|zh-cn|zh-tw|zh-sg|zh-hk) echo "zh" ;;
    id|in|id-id) echo "id" ;;
    de|de-de)   echo "de" ;;
    fr|fr-fr)   echo "fr" ;;
    es|es-es)   echo "es" ;;
    ru|ru-ru)   echo "ru" ;;
    pt|pt-br|pt-pt) echo "pt" ;;
    pl|pl-pl)   echo "pl" ;;
    en*)        echo "en" ;;
    *)          echo "" ;;
  esac
}

is_supported_lang() {
  echo "$SUPPORTED_LANGS" | grep -qw "$1"
}

# 1. Parse --lang from script arguments
while [ $# -gt 0 ]; do
  case "$1" in
    --lang)
      shift
      if is_supported_lang "$1"; then RESOLVED_LANG="$1"; fi
      shift ;;
    --lang=*)
      val="${1#--lang=}"
      if is_supported_lang "$val"; then RESOLVED_LANG="$val"; fi
      shift ;;
    *) shift ;;
  esac
done

# 2. Try $PIXIV_LANG env var (only if not already set via --lang)
if [ "$RESOLVED_LANG" = "en" ] && [ -n "$PIXIV_LANG" ] && is_supported_lang "$PIXIV_LANG"; then
  RESOLVED_LANG="$PIXIV_LANG"
fi

# 3. Auto-detect from OS locale
if [ "$RESOLVED_LANG" = "en" ]; then
  for loc_var in "$LC_ALL" "$LANG" "$LANGUAGE"; do
    if [ -n "$loc_var" ]; then
      detected=$(map_locale_to_lang "$loc_var")
      if [ -n "$detected" ]; then
        RESOLVED_LANG="$detected"
        break
      fi
    fi
  done
fi
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BOLD='\033[1m'
DIM='\033[2m'
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
info()  { echo -e "  ${DIM}[i]${RESET} $1"; }

banner
info "Language: ${CYAN}${RESOLVED_LANG}${RESET}"

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
    step "Python 3.11+ not found."
    step "Attempting auto-installation..."
    if command -v apt &>/dev/null; then
        sudo apt update
        sudo apt install -y python3 python3-pip python3-venv
        PYTHON_CMD="python3"
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y python3 python3-pip
        PYTHON_CMD="python3"
    elif command -v pacman &>/dev/null; then
        sudo pacman -Sy --noconfirm python python-pip
        PYTHON_CMD="python"
    elif command -v brew &>/dev/null; then
        brew install python
        PYTHON_CMD="python3"
    else
        err "Could not find a supported package manager. Install Python 3.11+ manually from https://www.python.org/downloads/"
        exit 1
    fi
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
if [ "$RESOLVED_LANG" != "en" ]; then
  echo -e "    ${CYAN}$PYTHON_CMD pixiv_login.py --lang $RESOLVED_LANG${RESET}"
else
  echo -e "    ${CYAN}$PYTHON_CMD pixiv_login.py${RESET}"
fi
echo ""
echo -e "  ${DIM}[i] Language '$RESOLVED_LANG' was auto-detected from your OS.${RESET}"
echo -e "  ${DIM}    To override: PIXIV_LANG=jp bash <(curl -sL ..../install.sh)${RESET}"
echo ""
