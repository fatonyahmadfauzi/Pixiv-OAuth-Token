@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0\.."

REM --- config ---
set SCRIPT=app\pixiv_login.py
set ICON=app\pixiv_oauth.ico
set OUTNAME=pixiv_login_plus
set PORTABLE_LABEL=Pixiv OAuth CLi (Portable)

REM --- ensure deps ---
python -m pip install -r app\requirements.txt

if not exist "%ICON%" (
  echo [ERROR] Icon file not found: %ICON%
  exit /b 1
)
python scripts\check_icon_square.py "%ICON%"
if errorlevel 1 exit /b 1

REM --- clean ---
if exist dist rmdir /s /q dist
if exist nuitka_tmp rmdir /s /q nuitka_tmp
del /q *.spec 2>nul

REM --- bump version (patch by default). Usage: scripts\build_portable_pro.bat minor|major|patch|none ---
set BUMP=patch
if not "%~1"=="" set BUMP=%~1

for /f "usebackq delims=" %%v in (`python scripts\bump_version.py %BUMP%`) do set VERLINE=%%v
for /f "tokens=1,2 delims=|" %%a in ("%VERLINE%") do (
  set VER=%%a
  set BUILD_CODE=%%b
)
python scripts\sync_app_identity.py
python scripts\generate_version_info.py

REM --- build portable ---
python -m nuitka --onefile ^
  --output-dir=dist ^
  --output-filename=%OUTNAME%.exe ^
  --windows-icon-from-ico=%ICON% ^
  --windows-product-version=%VER%.0 ^
  --windows-file-version=%VER%.0 ^
  --windows-company-name="Fatony Ahmad Fauzi" ^
  --windows-product-name="Pixiv OAuth CLI" ^
  --windows-file-description="Pixiv OAuth Command Line Interface" ^
  --remove-output ^
  --assume-yes-for-downloads ^
  %SCRIPT%

if errorlevel 1 (
  echo [ERROR] Nuitka compilation failed. Stopping.
  exit /b 1
)

REM --- copy portable output ---
if not exist build\portable mkdir build\portable
del /q build\portable\*_v*.exe 2>nul
copy /y dist\%OUTNAME%.exe build\portable\%OUTNAME%.exe >nul
copy /y dist\%OUTNAME%.exe "build\portable\%PORTABLE_LABEL%.exe" >nul

echo.
echo Portable built:
echo   build\portable\%OUTNAME%.exe
echo   build\portable\%PORTABLE_LABEL%.exe
echo.

exit /b 0
