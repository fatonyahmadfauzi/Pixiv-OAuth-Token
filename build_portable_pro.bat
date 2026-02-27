@echo off
setlocal enabledelayedexpansion

REM --- config ---
set SCRIPT=pixiv_login.py
set ICON=pixiv_login_pro.ico
set OUTNAME=pixiv_login_plus
set PORTABLE_LABEL=Pixiv OAuth CLi (Portable)

REM --- ensure deps ---
python -m pip install -r requirements.txt

REM --- clean ---
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
del /q *.spec 2>nul

REM --- bump version (patch by default). Usage: build_portable_pro.bat minor|major|patch|none ---
set BUMP=patch
if not "%~1"=="" set BUMP=%~1

for /f "usebackq delims=" %%v in (`python bump_version.py %BUMP%`) do set VER=%%v
python generate_version_info.py

REM --- build portable ---
pyinstaller --noconfirm --onefile ^
  --name %OUTNAME% ^
  --icon=%ICON% ^
  --version-file=version_info.txt ^
  %SCRIPT%

if errorlevel 1 (
  echo [ERROR] PyInstaller failed. Stopping.
  exit /b 1
)

REM --- copy portable output ---
if not exist dist_portable mkdir dist_portable
del /q dist_portable\*_v*.exe 2>nul
copy /y dist\%OUTNAME%.exe dist_portable\%OUTNAME%_v%VER%.exe >nul
copy /y dist\%OUTNAME%.exe dist_portable\%OUTNAME%.exe >nul
copy /y dist\%OUTNAME%.exe "dist_portable\%PORTABLE_LABEL%.exe" >nul

echo.
echo Portable built:
echo   dist_portable\%OUTNAME%.exe
echo   dist_portable\%OUTNAME%_v%VER%.exe
echo   dist_portable\%PORTABLE_LABEL%.exe
echo.

exit /b 0
