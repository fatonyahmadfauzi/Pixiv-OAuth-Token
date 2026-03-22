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
set ICON=pixiv_oauth.ico
set PORTABLE_LABEL=Pixiv OAuth GUi (Portable)
set ADD_TUTORIAL=

set BUMP=none
if not "%~1"=="" set BUMP=%~1

REM Set TCL/TK environment for Python 3.11
set TCL_LIBRARY=C:\Users\faton\AppData\Local\Programs\Python\Python311\tcl\tcl8.6
set TK_LIBRARY=C:\Users\faton\AppData\Local\Programs\Python\Python311\tcl\tk8.6

REM Ensure deps
python -m pip install -r requirements.txt

if not exist "%ICON%" (
  echo [ERROR] Icon file not found: %ICON%
  exit /b 1
)
python check_icon_square.py "%ICON%"
if errorlevel 1 exit /b 1

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

REM Bundle tutorial images if available
if exist "tutorial_images" set ADD_TUTORIAL=--add-data "tutorial_images;tutorial_images"

REM Build (windowed = no console)
python -m PyInstaller --noconfirm --onefile --windowed ^
  --name %NAME% ^
  --icon=%ICON% ^
  --version-file=version_info.txt ^
  --hidden-import tkinter ^
  --hidden-import tkinter.ttk ^
  --hidden-import _tkinter ^
  %ADD_TUTORIAL% ^
  %SCRIPT%

if errorlevel 1 (
  echo [ERROR] PyInstaller failed.
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