@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

REM ==========================================================
REM build_all_pro.bat (UPDATED)
REM 1-click build for:
REM   - CLI portable (build_portable_pro.bat)   -> dist_portable\
REM   - GUI (build_gui_pro.bat)                -> dist_gui\
REM   - Installer (optional)                   -> dist_installer\
REM   - Release ZIP (build_release_zip.bat)    -> PixivLoginRelease_vX.Y.Z.zip
REM
REM Usage:
REM   build_all_pro.bat [patch|minor|major|none] [noinst] [nosign] [nozip] [nogui] [nopause]
REM
REM Notes:
REM   - Version bump is applied ONLY on CLI build (so CLI+GUI+Installer share same version.json).
REM   - GUI build is invoked with "none" to keep version consistent.
REM   - Installer step will auto-detect ISCC.exe if a .iss exists:
REM       pixiv_login_installer_dual.iss (preferred) or pixiv_login_installer.iss
REM ==========================================================

set BUMP=patch
set SKIP_INST=0
set SKIP_SIGN=0
set SKIP_ZIP=0
set SKIP_GUI=0
set NO_PAUSE=0

if not "%~1"=="" set BUMP=%~1

for %%A in (%*) do (
  if /I "%%~A"=="noinst" set SKIP_INST=1
  if /I "%%~A"=="nosign" set SKIP_SIGN=1
  if /I "%%~A"=="nozip"  set SKIP_ZIP=1
  if /I "%%~A"=="nogui"  set SKIP_GUI=1
  if /I "%%~A"=="nopause" set NO_PAUSE=1
)

echo.
echo ===== Pixiv Login - Build All (CLI + GUI + Installer + ZIP) =====
echo Folder : %cd%
echo Bump   : %BUMP%
if %SKIP_GUI%==1 (echo GUI     : SKIP) else (echo GUI     : YES)
if %SKIP_INST%==1 (echo Installer: SKIP) else (echo Installer: AUTO)
if %SKIP_SIGN%==1 (echo Signing : SKIP) else (echo Signing : AUTO if sign_auto.bat exists)
if %SKIP_ZIP%==1  (echo ZIP     : SKIP) else (echo ZIP     : YES)
echo.

REM --- Clean (optional) ---
if exist clean_build.bat (
  call clean_build.bat
)

REM --- Build CLI (this bumps version by default) ---
if not exist build_portable_pro.bat (
  echo [ERROR] build_portable_pro.bat not found.
  exit /b 1
)
call build_portable_pro.bat %BUMP%
if errorlevel 1 (
  echo [ERROR] CLI build failed.
  exit /b 1
)

REM --- Build GUI (keep version consistent; do NOT bump here) ---
if %SKIP_GUI%==1 goto after_gui
if not exist build_gui_pro.bat (
  echo [ERROR] build_gui_pro.bat not found. (Download/update it first)
  exit /b 1
)
call build_gui_pro.bat none
if errorlevel 1 (
  echo [ERROR] GUI build failed.
  exit /b 1
)
:after_gui

REM --- Build installer (optional) ---
if %SKIP_INST%==1 goto after_inst

set ISS_FILE=
if exist pixiv_login_installer_dual.iss set ISS_FILE=pixiv_login_installer_dual.iss
if "%ISS_FILE%"=="" if exist pixiv_login_installer.iss set ISS_FILE=pixiv_login_installer.iss

if "%ISS_FILE%"=="" (
  echo [WARN] No .iss installer script found. Skipping installer.
  goto after_inst
)

REM If there is a generator for dual iss, run it first (optional)
if exist make_installer_iss_dual.py (
  python make_installer_iss_dual.py
) else if exist make_installer_iss.py (
  python make_installer_iss.py
)

set ISCC_PATH=
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" set ISCC_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
if exist "C:\Program Files\Inno Setup 6\ISCC.exe" set ISCC_PATH=C:\Program Files\Inno Setup 6\ISCC.exe
if "%ISCC_PATH%"=="" (
  where ISCC.exe >nul 2>nul
  if not errorlevel 1 set ISCC_PATH=ISCC.exe
)

if "%ISCC_PATH%"=="" (
  echo [WARN] ISCC.exe not found. Skipping installer build.
  echo Install Inno Setup, then ensure ISCC.exe is in PATH.
  goto after_inst
)

echo.
echo ===== Building Installer =====
echo Using: "%ISCC_PATH%"
echo Script: %ISS_FILE%
"%ISCC_PATH%" "%ISS_FILE%"
if errorlevel 1 (
  echo [ERROR] Installer build failed.
  exit /b 1
)

:after_inst

REM --- Signing (optional) ---
if %SKIP_SIGN%==1 goto after_sign
if exist sign_auto.bat (
  call sign_auto.bat
) else (
  echo [WARN] sign_auto.bat not found. Skipping signing.
)
:after_sign

REM --- Release ZIP ---
if %SKIP_ZIP%==1 goto done
if exist build_release_zip.bat (
  call build_release_zip.bat
) else (
  echo [WARN] build_release_zip.bat not found. Skipping ZIP.
)

:done
echo.
echo ===== DONE =====
if exist dist_portable\pixiv_login_plus.exe echo CLI : dist_portable\pixiv_login_plus.exe
if exist dist_gui\pixiv_login_gui.exe echo GUI : dist_gui\pixiv_login_gui.exe
echo Installer: dist_installer\ (if built)
echo ZIP      : PixivLoginRelease_vX.Y.Z.zip (if built)
echo.

if %NO_PAUSE%==1 exit /b 0
pause
