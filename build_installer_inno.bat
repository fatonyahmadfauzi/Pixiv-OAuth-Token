@echo off
setlocal enabledelayedexpansion

REM Usage: build_installer_inno.bat [major|minor|patch|none]
set BUMP=patch
if not "%~1"=="" set BUMP=%~1

call build_portable_pro.bat %BUMP%
python make_installer_iss.py

REM Requires Inno Setup installed and ISCC.exe available in PATH.
ISCC.exe pixiv_login_installer.iss

echo.
echo Installer output should be in dist_installer\
echo.
pause
