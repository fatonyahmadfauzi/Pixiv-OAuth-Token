@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

REM ========= CONFIG =========
REM Letakkan file sertifikat di folder project ini, misalnya: codesign.pfx
set PFX_PATH=%~dp0codesign.pfx
set PFX_PASS=YOUR_PASSWORD_HERE
set TS_URL=http://timestamp.digicert.com

set PORTABLE=dist_portable\pixiv_login_plus.exe

REM Cari installer terbaru (kalau ada)
set INSTALLER=
for /f "delims=" %%f in ('dir /b /o:-d dist_installer\PixivLoginSetup_v*.exe 2^>nul') do (
  set INSTALLER=dist_installer\%%f
  goto :found
)
:found

REM ========= AUTO-DETECT signtool.exe =========
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

REM ========= ONLY SIGN IF PFX EXISTS =========
if not exist "%PFX_PATH%" (
  echo [WARN] PFX not found: "%PFX_PATH%"
  echo        Skipping signing. (Place codesign.pfx in project folder)
  exit /b 0
)

if not exist "%PORTABLE%" (
  echo [WARN] Portable exe not found: %PORTABLE%
  exit /b 0
)

echo Signing with PFX: "%PFX_PATH%"
echo Timestamp: %TS_URL%
echo.

signtool sign /f "%PFX_PATH%" /p "%PFX_PASS%" /tr "%TS_URL%" /td sha256 /fd sha256 "%PORTABLE%"
if errorlevel 1 (
  echo [ERROR] Failed signing portable.
  exit /b 1
)

if not "%INSTALLER%"=="" (
  if exist "%INSTALLER%" (
    signtool sign /f "%PFX_PATH%" /p "%PFX_PASS%" /tr "%TS_URL%" /td sha256 /fd sha256 "%INSTALLER%"
    if errorlevel 1 (
      echo [ERROR] Failed signing installer.
      exit /b 1
    )
  )
)

echo Done signing.
exit /b 0