@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0\.."

REM ========= CONFIG =========
set PFX_PATH=%~dp0codesign.pfx
set PFX_PASS=PixivOAuthSign2025
set TS_URL=http://timestamp.digicert.com

REM Ensure we have the certificate
if not exist "%PFX_PATH%" (
    echo [!] Certificate not found at: %PFX_PATH%
    echo     Please run create_selfsigned_cert.ps1 first.
    exit /b 1
)

REM Find signtool.exe
set SIGNTOOL=
where signtool.exe >nul 2>nul
if not errorlevel 1 (
    set SIGNTOOL=signtool.exe
    goto :found_signtool
)

REM Prefer x64, fallback to x86, never use arm/arm64 on standard pcs
for /f "delims=" %%S in ('dir /b /s "C:\Program Files (x86)\Windows Kits\10\bin\signtool.exe" 2^>nul') do (
    echo "%%S" | findstr /i "\\x64\\" >nul
    if not errorlevel 1 (
        set "SIGNTOOL=%%S"
        goto :found_signtool
    )
)
for /f "delims=" %%S in ('dir /b /s "C:\Program Files (x86)\Windows Kits\10\bin\signtool.exe" 2^>nul') do (
    echo "%%S" | findstr /i "\\x86\\" >nul
    if not errorlevel 1 (
        set "SIGNTOOL=%%S"
        goto :found_signtool
    )
)
:found_signtool

if "%SIGNTOOL%"=="" (
    echo [!] signtool.exe not found. Please install Windows SDK.
    exit /b 1
)

echo [*] Using signtool: %SIGNTOOL%
echo [*] Certificate: %PFX_PATH%
echo.

REM --- Sign Portable Executables ---
echo [*] Signing portable executables...
for %%f in ("build\portable\*.exe" "build\gui\*.exe") do (
    echo   - Signing: %%f
    "%SIGNTOOL%" sign /v /f "%PFX_PATH%" /p "%PFX_PASS%" /fd SHA256 /tr %TS_URL% /td SHA256 "%%f"
)

REM --- Sign Installers & Downloads ---
echo.
echo [*] Signing installer and downloads executables...
for %%f in ("build\installer\*.exe" "build\downloads\*.exe") do (
    echo   - Signing: %%f
    "%SIGNTOOL%" sign /v /f "%PFX_PATH%" /p "%PFX_PASS%" /fd SHA256 /tr %TS_URL% /td SHA256 "%%f"
)

echo.
echo [V] All signing complete!
exit /b 0
