@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

REM ==========================================================
REM build_all_pro.bat (FULL RELEASE)
REM - Clean
REM - Build portable (auto bump)
REM - Generate .iss
REM - Delete old installers (optional)
REM - Build installer (auto-detect ISCC)
REM - Auto-sign IF codesign.pfx exists
REM - Build release ZIP
REM
REM Usage:
REM   build_all_pro.bat [patch|minor|major|none] [noinst] [nosign] [nozip] [nopause]
REM ==========================================================

set BUMP=patch
set SKIP_INST=0
set SKIP_SIGN=0
set SKIP_ZIP=0
set NO_PAUSE=0

if not "%~1"=="" set BUMP=%~1

for %%A in (%*) do (
  if /I "%%~A"=="noinst" set SKIP_INST=1
  if /I "%%~A"=="nosign" set SKIP_SIGN=1
  if /I "%%~A"=="nozip"  set SKIP_ZIP=1
  if /I "%%~A"=="nopause" set NO_PAUSE=1
)

echo.
echo ===== Pixiv Login - FULL RELEASE =====
echo Folder : %cd%
echo Bump   : %BUMP%
if %SKIP_INST%==1 (echo Installer: SKIP) else (echo Installer: YES)
if %SKIP_SIGN%==1 (echo Signing : SKIP) else (echo Signing : AUTO if PFX exists)
if %SKIP_ZIP%==1  (echo ZIP     : SKIP) else (echo ZIP     : YES)
echo.

REM 1) Clean
call clean_build.bat

REM 2) Build portable
call build_portable_pro.bat %BUMP%
if errorlevel 1 (
  echo [ERROR] Portable build failed.
  exit /b 1
)

REM 3) Generate .iss
python make_installer_iss.py

REM 4) Installer
if %SKIP_INST%==1 goto after_inst

REM Delete old installers (keeps folder clean)
if exist dist_installer (
  del /q dist_installer\PixivLoginSetup_v*.exe 2>nul
)

set ISCC_PATH=
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" set ISCC_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
if exist "C:\Program Files\Inno Setup 6\ISCC.exe" set ISCC_PATH=C:\Program Files\Inno Setup 6\ISCC.exe

if "%ISCC_PATH%"=="" (
  where ISCC.exe >nul 2>nul
  if not errorlevel 1 set ISCC_PATH=ISCC.exe
)

if "%ISCC_PATH%"=="" (
  echo [WARN] ISCC.exe not found. Skipping installer.
) else (
  echo.
  echo ===== Building installer =====
  echo Using: "%ISCC_PATH%"
  "%ISCC_PATH%" pixiv_login_installer.iss
)

:after_inst

REM 5) Signing (auto if PFX exists)
if %SKIP_SIGN%==1 goto after_sign
call sign_auto.bat

:after_sign

REM 6) ZIP release
if %SKIP_ZIP%==1 goto done
call build_release_zip.bat

:done
echo.
echo ===== DONE =====
echo Portable : dist_portable\pixiv_login_plus.exe
echo Installer: dist_installer\PixivLoginSetup_vX.Y.Z.exe (if built)
echo Release  : PixivLoginRelease_vX.Y.Z.zip (if built)
echo.

if %NO_PAUSE%==1 exit /b 0
pause