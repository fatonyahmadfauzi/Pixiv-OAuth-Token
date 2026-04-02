# =============================================================
#  Pixiv OAuth Token CLI - Quick Installer (PowerShell)
#  Supports: PowerShell 5.1+, PowerShell 7+
#  Usage:
#    irm https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/install.ps1 | iex
# =============================================================

$ErrorActionPreference = "Stop"

$RAW_BASE  = "https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master"
$FILE_URL  = "$RAW_BASE/app/pixiv_login.py"
$OUT_FILE  = "pixiv_login.py"

function Write-Banner {
    Write-Host ""
    Write-Host "  ╔══════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "  ║    Pixiv OAuth Token CLI - Installer     ║" -ForegroundColor Cyan
    Write-Host "  ║       by Fatony Ahmad Fauzi              ║" -ForegroundColor Cyan
    Write-Host "  ╚══════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step([string]$msg) {
    Write-Host "  [*] $msg" -ForegroundColor Yellow
}

function Write-Ok([string]$msg) {
    Write-Host "  [+] $msg" -ForegroundColor Green
}

function Write-Err([string]$msg) {
    Write-Host "  [!] $msg" -ForegroundColor Red
}

Write-Banner

# --- 1. Check Python ---
Write-Step "Checking Python installation..."
try {
    $pyVer = python --version 2>&1
    if ($pyVer -match "Python (\d+)\.(\d+)") {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 11)) {
            Write-Err "Python 3.11+ is required. Found: $pyVer"
            Write-Err "Download Python from https://www.python.org/downloads/"
            exit 1
        }
        Write-Ok "Found $pyVer"
    } else {
        throw "Cannot parse version"
    }
} catch {
    Write-Err "Python not found. Install Python 3.11+ from https://www.python.org/downloads/"
    exit 1
}

# --- 2. Download pixiv_login.py ---
Write-Step "Downloading pixiv_login.py from GitHub..."
try {
    Invoke-WebRequest -Uri $FILE_URL -OutFile $OUT_FILE -UseBasicParsing
    Write-Ok "Downloaded: $OUT_FILE"
} catch {
    Write-Err "Download failed: $_"
    Write-Err "Check your internet connection or download manually:"
    Write-Err "  $FILE_URL"
    exit 1
}

# --- 3. Install dependencies ---
Write-Step "Installing dependencies (requests)..."
try {
    python -m pip install requests --quiet --disable-pip-version-check
    Write-Ok "requests installed"
} catch {
    Write-Err "pip install failed. Try manually: pip install requests"
}

# --- 4. Done ---
Write-Host ""
Write-Host "  ╔══════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "  ║           Installation complete!         ║" -ForegroundColor Green
Write-Host "  ╚══════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "  Run with:" -ForegroundColor White
Write-Host "    python pixiv_login.py" -ForegroundColor Cyan
Write-Host ""
