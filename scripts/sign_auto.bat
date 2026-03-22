@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

REM ========= CONFIG =========
set PFX_PATH=%~dp0codesign.pfx
set PFX_PASS=YOUR_PASSWORD_HERE
set TS_URL=http://timestamp.digicert.com

set PORTABLE=dist_portable\Pixiv OAuth CLi (Portable).exe

set INSTALLER_CLI=
for /f "delims=" %%f in ('dir /b /o:-d "dist_installer\Pixiv OAuth CLi Setup_v*.exe" 2^>nul') do (
  set INSTALLER_CLI=dist_installer\%%f
  goto :found_cli
)
:found_cli

set INSTALLER_GUI=
for /f "delims=" %%f in ('dir /b /o:-d "dist_installer\Pixiv OAuth GUi Setup_v*.exe" 2^>nul') do (
  set INSTALLER_GUI=dist_installer\%%f
  goto :found_gui
)
:found_gui

where signtool.exe >nul 2>nul
if errorlevel 1 (
  for /f "delims=" %%S in ('dir /b /s "C:\Program Files (x86)\Windows Kits\10\bin\*\x64\signtool.exe" 2^>nul') do (
    set "SDK_SIGNTOOL=%%S"
    goto :have_signtool
  )
  echo [WARN] signtool.exe not found. Install Windows SDK / VS Build Tools.
  exit /b 0
)

:have_signtool
if defined SDK_SIGNTOOL (
  for %%D in ("!SDK_SIGNTOOL!") do set "SDK_DIR=%%~dpD"
  set "PATH=!SDK_DIR!;!PATH!"
)

if not exist "%PFX_PATH%" (
  echo [WARN] PFX not found: "%PFX_PATH%"
  exit /b 0
)

if exist "%PORTABLE%" (
  signtool sign /f "%PFX_PATH%" /p "%PFX_PASS%" /tr "%TS_URL%" /td sha256 /fd sha256 "%PORTABLE%"
)

if not "%INSTALLER_CLI%"=="" if exist "%INSTALLER_CLI%" (
  signtool sign /f "%PFX_PATH%" /p "%PFX_PASS%" /tr "%TS_URL%" /td sha256 /fd sha256 "%INSTALLER_CLI%"
)

if not "%INSTALLER_GUI%"=="" if exist "%INSTALLER_GUI%" (
  signtool sign /f "%PFX_PATH%" /p "%PFX_PASS%" /tr "%TS_URL%" /td sha256 /fd sha256 "%INSTALLER_GUI%"
)

echo Done signing.
exit /b 0
