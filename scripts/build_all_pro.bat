@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0\.."

REM ==========================================================
REM build_all_pro.bat
REM 1-click build for:
REM   - CLI portable (scripts\build_portable_pro.bat)   -> build\portable\
REM   - GUI portable (scripts\build_gui_pro.bat)        -> build\gui\
REM   - Installer (optional)                    -> build\installer\
REM   - Release ZIP (scripts\build_release_zip.bat)     -> PixivOAuthRelease_vX.Y.Z.zip
REM
REM Usage:
REM   build_all_pro.bat [patch|minor|major|none] [noinst] [nosign] [nozip] [nogui] [nopause]
REM ==========================================================

set BUMP=patch
set SKIP_INST=0
set SKIP_SIGN=0
set SKIP_ZIP=0
set SKIP_GUI=0
set NO_PAUSE=0
set ICON_FILE=app\pixiv_oauth.ico

if not "%~1"=="" set BUMP=%~1

for %%A in (%*) do (
  if /I "%%~A"=="noinst" set SKIP_INST=1
  if /I "%%~A"=="nosign" set SKIP_SIGN=1
  if /I "%%~A"=="nozip"  set SKIP_ZIP=1
  if /I "%%~A"=="nogui"  set SKIP_GUI=1
  if /I "%%~A"=="nopause" set NO_PAUSE=1
)

echo.
echo ===== Pixiv OAuth - Build All =====
echo Folder : %cd%
echo Bump   : %BUMP%
echo Icon   : %ICON_FILE%
if %SKIP_GUI%==1 (echo GUI      : SKIP) else (echo GUI      : YES)
if %SKIP_INST%==1 (echo Installer: SKIP) else (echo Installer: AUTO)
if %SKIP_SIGN%==1 (echo Signing  : SKIP) else (echo Signing  : AUTO if scripts\sign_auto.bat exists)
if %SKIP_ZIP%==1  (echo ZIP      : SKIP) else (echo ZIP      : YES)
echo.

REM --- Clean old artifacts first (avoid stacking old files) ---
if exist build\portable (
  del /q build\portable\*_v*.exe 2>nul
  del /q "build\portable\Pixiv OAuth CLi (Portable) x86.exe" 2>nul
  del /q "build\portable\Pixiv OAuth CLi (Portable) x64.exe" 2>nul
  del /q "build\portable\Pixiv OAuth CLi (Portable) ARM64.exe" 2>nul
)
if exist build\gui (
  del /q build\gui\*_v*.exe 2>nul
  del /q "build\gui\Pixiv OAuth GUi (Portable) x86.exe" 2>nul
  del /q "build\gui\Pixiv OAuth GUi (Portable) x64.exe" 2>nul
  del /q "build\gui\Pixiv OAuth GUi (Portable) ARM64.exe" 2>nul
)
if exist build\installer (
  del /q "build\installer\Pixiv OAuth CLi Setup_v*.exe" 2>nul
  del /q "build\installer\Pixiv OAuth GUi Setup_v*.exe" 2>nul
)
if exist build\downloads (
  del /q "build\downloads\Pixiv OAuth CLi Setup_v*.exe" 2>nul
  del /q "build\downloads\Pixiv OAuth GUi Setup_v*.exe" 2>nul
  del /q "build\downloads\PixivOAuthRelease_v*.zip" 2>nul
)
if exist build\releases del /q "build\releases\PixivOAuthRelease_v*.zip" 2>nul
del /q "PixivOAuthRelease_v*.zip" 2>nul

if exist scripts\clean_build.bat (
  call scripts\clean_build.bat
)

if not exist "%ICON_FILE%" (
  echo [ERROR] Icon file not found: %ICON_FILE%
  exit /b 1
)

python scripts\check_icon_square.py "%ICON_FILE%"
if errorlevel 1 exit /b 1

set BUILD_ICON=%ICON_FILE%

REM --- Build CLI (this bumps version by default) ---
if not exist scripts\build_portable_pro.bat (
  echo [ERROR] scripts\build_portable_pro.bat not found.
  exit /b 1
)
call scripts\build_portable_pro.bat %BUMP%
if errorlevel 1 (
  echo [ERROR] CLI build failed.
  exit /b 1
)

REM --- Build GUI (keep version consistent; do NOT bump here) ---
if %SKIP_GUI%==1 goto after_gui
if not exist scripts\build_gui_pro.bat (
  echo [ERROR] scripts\build_gui_pro.bat not found.
  exit /b 1
)
call scripts\build_gui_pro.bat none
if errorlevel 1 (
  echo [ERROR] GUI build failed.
  exit /b 1
)
:after_gui

REM --- Build installer (optional) ---
if %SKIP_INST%==1 goto after_inst

if exist scripts\make_installer_iss_dual.py (
  python scripts\make_installer_iss_dual.py
) else if exist make_installer_iss.py (
  python make_installer_iss.py
)

set ISS_FILE=
if exist scripts\pixiv_login_installer_dual.iss set ISS_FILE=scripts\pixiv_login_installer_dual.iss
if "%ISS_FILE%"=="" if exist pixiv_login_installer_dual.iss set ISS_FILE=pixiv_login_installer_dual.iss
if "%ISS_FILE%"=="" if exist scripts\pixiv_login_installer.iss set ISS_FILE=scripts\pixiv_login_installer.iss
if "%ISS_FILE%"=="" if exist pixiv_login_installer.iss set ISS_FILE=pixiv_login_installer.iss

if "%ISS_FILE%"=="" (
  echo [WARN] No .iss installer script found. Skipping installer.
  goto after_inst
)

set ISCC_PATH=
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" set ISCC_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
if exist "C:\Program Files\Inno Setup 6\ISCC.exe" set ISCC_PATH=C:\Program Files\Inno Setup 6\ISCC.exe
if exist "C:\Program Files (x86)\Inno Setup 7\ISCC.exe" set ISCC_PATH=C:\Program Files (x86)\Inno Setup 7\ISCC.exe
if exist "C:\Program Files\Inno Setup 7\ISCC.exe" set ISCC_PATH=C:\Program Files\Inno Setup 7\ISCC.exe
if "%ISCC_PATH%"=="" (
  where ISCC.exe >nul 2>nul
  if not errorlevel 1 set ISCC_PATH=ISCC.exe
)

if "%ISCC_PATH%"=="" (
  echo [WARN] ISCC.exe not found. Skipping installer build.
  goto after_inst
)

echo.
echo ===== Building Installer =====
"%ISCC_PATH%" "%ISS_FILE%"
if errorlevel 1 (
  echo [ERROR] Installer build failed.
  exit /b 1
)

for /f "usebackq delims=" %%v in (`python -c "import json;d=json.load(open('version.json'));print(d.get('version','0.0.0'))"`) do set VER=%%v
for /f "usebackq delims=" %%b in (`python -c "import json;d=json.load(open('version.json'));print(d.get('build_code','BUILD-UNKNOWN'))"`) do set BCODE=%%b
for /f "delims=" %%f in ('dir /b /o:-d "build\installer\PixivLoginSetup_v*.exe" 2^>nul') do set LATEST_SETUP_RAW=%%f
if defined LATEST_SETUP_RAW (
  del /q "build\installer\Pixiv OAuth CLi Setup_v*.exe" 2>nul
  del /q "build\installer\Pixiv OAuth GUi Setup_v*.exe" 2>nul
  copy /y "build\installer\!LATEST_SETUP_RAW!" "build\installer\Pixiv OAuth CLi Setup_v!VER!_!BCODE!.exe" >nul
  copy /y "build\installer\!LATEST_SETUP_RAW!" "build\installer\Pixiv OAuth GUi Setup_v!VER!_!BCODE!.exe" >nul
)

:after_inst

REM --- Signing (optional) ---
if %SKIP_SIGN%==1 goto after_sign
if exist scripts\sign_auto.bat (
  call scripts\sign_auto.bat
) else (
  echo [WARN] scripts\sign_auto.bat not found. Skipping signing.
)
:after_sign

REM --- Release ZIP ---
if %SKIP_ZIP%==1 goto after_zip
if exist scripts\build_release_zip.bat (
  call scripts\build_release_zip.bat
) else (
  echo [WARN] scripts\build_release_zip.bat not found. Skipping ZIP.
)

:after_zip

if exist scripts\generate_latest_manifest.py (
  python scripts\generate_latest_manifest.py
)

REM --- Sync ONLY latest artifacts into build\downloads (4 files total) ---
if not exist build\downloads mkdir build\downloads

del /q "build\downloads\Pixiv OAuth CLi Setup_v*.exe" 2>nul
del /q "build\downloads\Pixiv OAuth GUi Setup_v*.exe" 2>nul
del /q "build\downloads\Pixiv OAuth CLi (Portable).exe" 2>nul
del /q "build\downloads\Pixiv OAuth GUi (Portable).exe" 2>nul
del /q "build\downloads\Pixiv OAuth CLi (Portable) *_latest.exe" 2>nul
del /q "build\downloads\Pixiv OAuth GUi (Portable) *_latest.exe" 2>nul
del /q "build\downloads\Pixiv OAuth CLi Setup *_latest.exe" 2>nul
del /q "build\downloads\Pixiv OAuth GUi Setup *_latest.exe" 2>nul
del /q "build\downloads\PixivOAuthRelease_v*.zip" 2>nul

if exist "build\portable\Pixiv OAuth CLi (Portable).exe" (
  copy /y "build\portable\Pixiv OAuth CLi (Portable).exe" "build\downloads\Pixiv OAuth CLi (Portable)_latest.exe" >nul
)
if exist "build\gui\Pixiv OAuth GUi (Portable).exe" (
  copy /y "build\gui\Pixiv OAuth GUi (Portable).exe" "build\downloads\Pixiv OAuth GUi (Portable)_latest.exe" >nul
)
for /f "delims=" %%f in ('dir /b /o:-d "build\installer\Pixiv OAuth CLi Setup_v*.exe" 2^>nul') do (
  copy /y "build\installer\%%f" "build\downloads\Pixiv OAuth CLi Setup_latest.exe" >nul
  goto :copied_dl_cli_inst
)
:copied_dl_cli_inst
for /f "delims=" %%f in ('dir /b /o:-d "build\installer\Pixiv OAuth GUi Setup_v*.exe" 2^>nul') do (
  copy /y "build\installer\%%f" "build\downloads\Pixiv OAuth GUi Setup_latest.exe" >nul
  goto :copied_dl_gui_inst
)
:copied_dl_gui_inst

REM --- Generate 3 architecture variants (x86/x64/ARM64) for portable and setup labels ---
for /f "usebackq delims=" %%v in (`python -c "import json;d=json.load(open('version.json'));print(d.get('version','0.0.0'))"`) do set VER=%%v
for /f "usebackq delims=" %%b in (`python -c "import json;d=json.load(open('version.json'));print(d.get('build_code','BUILD-UNKNOWN'))"`) do set BCODE=%%b

if exist "build\portable\Pixiv OAuth CLi (Portable).exe" (
  copy /y "build\portable\Pixiv OAuth CLi (Portable).exe" "build\portable\Pixiv OAuth CLi (Portable) x86.exe" >nul
  copy /y "build\portable\Pixiv OAuth CLi (Portable).exe" "build\portable\Pixiv OAuth CLi (Portable) x64.exe" >nul
  copy /y "build\portable\Pixiv OAuth CLi (Portable).exe" "build\portable\Pixiv OAuth CLi (Portable) ARM64.exe" >nul
  copy /y "build\portable\Pixiv OAuth CLi (Portable).exe" "build\downloads\Pixiv OAuth CLi (Portable) x86_latest.exe" >nul
  copy /y "build\portable\Pixiv OAuth CLi (Portable).exe" "build\downloads\Pixiv OAuth CLi (Portable) x64_latest.exe" >nul
  copy /y "build\portable\Pixiv OAuth CLi (Portable).exe" "build\downloads\Pixiv OAuth CLi (Portable) ARM64_latest.exe" >nul
)

if exist "build\gui\Pixiv OAuth GUi (Portable).exe" (
  copy /y "build\gui\Pixiv OAuth GUi (Portable).exe" "build\gui\Pixiv OAuth GUi (Portable) x86.exe" >nul
  copy /y "build\gui\Pixiv OAuth GUi (Portable).exe" "build\gui\Pixiv OAuth GUi (Portable) x64.exe" >nul
  copy /y "build\gui\Pixiv OAuth GUi (Portable).exe" "build\gui\Pixiv OAuth GUi (Portable) ARM64.exe" >nul
  copy /y "build\gui\Pixiv OAuth GUi (Portable).exe" "build\downloads\Pixiv OAuth GUi (Portable) x86_latest.exe" >nul
  copy /y "build\gui\Pixiv OAuth GUi (Portable).exe" "build\downloads\Pixiv OAuth GUi (Portable) x64_latest.exe" >nul
  copy /y "build\gui\Pixiv OAuth GUi (Portable).exe" "build\downloads\Pixiv OAuth GUi (Portable) ARM64_latest.exe" >nul
)

if exist "build\downloads\Pixiv OAuth CLi Setup_latest.exe" (
  copy /y "build\downloads\Pixiv OAuth CLi Setup_latest.exe" "build\installer\Pixiv OAuth CLi Setup_v!VER!_!BCODE!_x86.exe" >nul
  copy /y "build\downloads\Pixiv OAuth CLi Setup_latest.exe" "build\installer\Pixiv OAuth CLi Setup_v!VER!_!BCODE!_x64.exe" >nul
  copy /y "build\downloads\Pixiv OAuth CLi Setup_latest.exe" "build\installer\Pixiv OAuth CLi Setup_v!VER!_!BCODE!_ARM64.exe" >nul
  copy /y "build\downloads\Pixiv OAuth CLi Setup_latest.exe" "build\downloads\Pixiv OAuth CLi Setup x86_latest.exe" >nul
  copy /y "build\downloads\Pixiv OAuth CLi Setup_latest.exe" "build\downloads\Pixiv OAuth CLi Setup x64_latest.exe" >nul
  copy /y "build\downloads\Pixiv OAuth CLi Setup_latest.exe" "build\downloads\Pixiv OAuth CLi Setup ARM64_latest.exe" >nul
)

if exist "build\downloads\Pixiv OAuth GUi Setup_latest.exe" (
  copy /y "build\downloads\Pixiv OAuth GUi Setup_latest.exe" "build\installer\Pixiv OAuth GUi Setup_v!VER!_!BCODE!_x86.exe" >nul
  copy /y "build\downloads\Pixiv OAuth GUi Setup_latest.exe" "build\installer\Pixiv OAuth GUi Setup_v!VER!_!BCODE!_x64.exe" >nul
  copy /y "build\downloads\Pixiv OAuth GUi Setup_latest.exe" "build\installer\Pixiv OAuth GUi Setup_v!VER!_!BCODE!_ARM64.exe" >nul
  copy /y "build\downloads\Pixiv OAuth GUi Setup_latest.exe" "build\downloads\Pixiv OAuth GUi Setup x86_latest.exe" >nul
  copy /y "build\downloads\Pixiv OAuth GUi Setup_latest.exe" "build\downloads\Pixiv OAuth GUi Setup x64_latest.exe" >nul
  copy /y "build\downloads\Pixiv OAuth GUi Setup_latest.exe" "build\downloads\Pixiv OAuth GUi Setup ARM64_latest.exe" >nul
)

:done
echo.
echo ===== DONE =====
if exist "build\portable\Pixiv OAuth CLi (Portable).exe" echo CLI Portable : build\portable\Pixiv OAuth CLi (Portable).exe
if exist "build\gui\Pixiv OAuth GUi (Portable).exe" echo GUI Portable : build\gui\Pixiv OAuth GUi (Portable).exe
if exist build\installer echo Installer    : build\installer\
echo Variants     : x86, x64, ARM64 labels generated for Portable/Setup
echo ZIP          : build\releases\PixivOAuthRelease_vX.Y.Z.zip (not copied to build\downloads)
echo.

if %NO_PAUSE%==1 exit /b 0
pause
