@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

REM ==========================================================
REM build_gui_pro.bat
REM Build GUI exe (Tkinter) with:
REM  - icon
REM  - Windows version-info (from version.json via generate_version_info.py)
REM  - output copied to dist_gui\ (also a versioned copy)
REM
REM Usage:
REM   build_gui_pro.bat [patch|minor|major|none]
REM     - If none: do NOT bump version (keeps current version.json)
REM ==========================================================

set SCRIPT=pixiv_login_gui.py
set NAME=pixiv_login_gui
set ICON=pixiv_login_pro.ico

set BUMP=none
if not "%~1"=="" set BUMP=%~1

REM Ensure deps
python -m pip install -r requirements.txt

REM Optionally bump version
if /I not "%BUMP%"=="none" (
  for /f "usebackq delims=" %%v in (`python bump_version.py %BUMP%`) do set VER=%%v
) else (
  for /f "usebackq delims=" %%v in (`python -c "import json;print(json.load(open('version.json'))['version'])"`) do set VER=%%v
)

REM Generate version_info.txt for PyInstaller
python generate_version_info.py
if errorlevel 1 (
  echo [ERROR] generate_version_info.py failed.
  exit /b 1
)

REM Clean minimal (GUI only)
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
del /q *.spec 2>nul

REM Build (windowed = no console)
pyinstaller --noconfirm --onefile --windowed ^
  --name %NAME% ^
  --icon=%ICON% ^
  --version-file=version_info.txt ^
  %SCRIPT%

if errorlevel 1 (
  echo [ERROR] PyInstaller failed.
  exit /b 1
)

REM Copy outputs
if not exist dist_gui mkdir dist_gui
copy /y dist\%NAME%.exe dist_gui\%NAME%.exe >nul
copy /y dist\%NAME%.exe dist_gui\%NAME%_v%VER%.exe >nul

echo.
echo GUI built:
echo   dist_gui\%NAME%.exe
echo   dist_gui\%NAME%_v%VER%.exe
echo.
exit /b 0
