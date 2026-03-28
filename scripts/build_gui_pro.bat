@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0\.."

REM ==========================================================
REM scripts\build_gui_pro.bat
REM Build GUI exe (Tkinter) with:
REM  - icon
REM  - Windows version-info (from version.json via scripts\generate_version_info.py)
REM  - output copied to dist_gui\ (also a versioned copy)
REM
REM Usage:
REM   scripts\build_gui_pro.bat [patch|minor|major|none]
REM     - If none: do NOT bump version (keeps current version.json)
REM ==========================================================

set SCRIPT=app\pixiv_login_gui.py
set NAME=pixiv_login_gui
set ICON=app\pixiv_oauth.ico
set PORTABLE_LABEL=Pixiv OAuth GUi (Portable)
set ADD_TUTORIAL=

set BUMP=none
if not "%~1"=="" set BUMP=%~1

REM Set TCL/TK environment for Python 3.11
set TCL_LIBRARY=C:\Users\faton\AppData\Local\Programs\Python\Python311\tcl\tcl8.6
set TK_LIBRARY=C:\Users\faton\AppData\Local\Programs\Python\Python311\tcl\tk8.6

REM Ensure deps
python -m pip install -r app\requirements.txt

if not exist "%ICON%" (
  echo [ERROR] Icon file not found: %ICON%
  exit /b 1
)
python scripts\check_icon_square.py "%ICON%"
if errorlevel 1 exit /b 1

REM Optionally bump version
if /I not "%BUMP%"=="none" (
  for /f "usebackq delims=" %%v in (`python scripts\bump_version.py %BUMP%`) do set VERLINE=%%v
  for /f "tokens=1,2 delims=|" %%a in ("%VERLINE%") do (
    set VER=%%a
    set BUILD_CODE=%%b
  )
) else (
  for /f "usebackq delims=" %%v in (`python -c "import json;print(json.load(open('version.json'))['version'])"`) do set VER=%%v
)

python scripts\sync_app_identity.py

REM Generate version_info.txt for PyInstaller
python scripts\generate_version_info.py
if errorlevel 1 (
  echo [ERROR] scripts\generate_version_info.py failed.
  exit /b 1
)

REM Clean minimal (GUI only)
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
del /q *.spec 2>nul

REM Bundle tutorial images if available
if exist "tutorial_images" set ADD_TUTORIAL=--include-data-dir="tutorial_images=tutorial_images"

REM Build (windowed = no console)
python -m nuitka --onefile --windows-disable-console ^
  --output-dir=dist ^
  --output-filename=%NAME%.exe ^
  --windows-icon-from-ico=%ICON% ^
  --enable-plugin=tk-inter ^
  --windows-product-version=%VER%.0 ^
  --windows-file-version=%VER%.0 ^
  --windows-company-name="Fatony Ahmad Fauzi" ^
  --windows-product-name="Pixiv OAuth GUI" ^
  --windows-file-description="Pixiv OAuth Graphical Interface" ^
  --remove-output ^
  --assume-yes-for-downloads ^
  %ADD_TUTORIAL% ^
  %SCRIPT%

if errorlevel 1 (
  echo [ERROR] Nuitka compilation failed.
  exit /b 1
)

REM Copy outputs
if not exist dist_gui mkdir dist_gui
del /q dist_gui\*_v*.exe 2>nul
copy /y dist\%NAME%.exe dist_gui\%NAME%.exe >nul
copy /y dist\%NAME%.exe "dist_gui\%PORTABLE_LABEL%.exe" >nul

echo.
echo GUI built:
echo   dist_gui\%NAME%.exe
echo   dist_gui\%PORTABLE_LABEL%.exe
echo.
exit /b 0
