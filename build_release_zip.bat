@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

REM ==========================================================
REM build_release_zip.bat
REM Creates: PixivOAuthRelease_vX.Y.Z.zip
REM Contents:
REM   - Pixiv OAuth CLi (Portable).exe
REM   - Pixiv OAuth GUi (Portable).exe
REM   - Pixiv OAuth CLi Setup_vX.Y.Z.exe (if exists)
REM   - Pixiv OAuth GUi Setup_vX.Y.Z.exe (if exists)
REM   - version.json + docs
REM ==========================================================

for /f "usebackq delims=" %%v in (`python -c "import json;print(json.load(open('version.json'))['version'])"`) do set VER=%%v

set RELEASE_DIR=release
set ZIP_NAME=PixivOAuthRelease_v%VER%.zip

if not exist "%RELEASE_DIR%" mkdir "%RELEASE_DIR%"
del /q "%RELEASE_DIR%\*" 2>nul

if exist "dist_portable\Pixiv OAuth CLi (Portable).exe" copy /y "dist_portable\Pixiv OAuth CLi (Portable).exe" "%RELEASE_DIR%\Pixiv OAuth CLi (Portable).exe" >nul
if exist "dist_gui\Pixiv OAuth GUi (Portable).exe" copy /y "dist_gui\Pixiv OAuth GUi (Portable).exe" "%RELEASE_DIR%\Pixiv OAuth GUi (Portable).exe" >nul
if exist "pixiv_login_plus_linux" copy /y "pixiv_login_plus_linux" "%RELEASE_DIR%\pixiv_login_plus_linux" >nul
if exist "dist_linux\pixiv_login_plus_linux" copy /y "dist_linux\pixiv_login_plus_linux" "%RELEASE_DIR%\pixiv_login_plus_linux" >nul

for /f "delims=" %%f in ('dir /b /o:-d "dist_installer\Pixiv OAuth CLi Setup_v*.exe" 2^>nul') do (
  copy /y "dist_installer\%%f" "%RELEASE_DIR%\%%f" >nul
  goto :copied_cli_inst
)
:copied_cli_inst

for /f "delims=" %%f in ('dir /b /o:-d "dist_installer\Pixiv OAuth GUi Setup_v*.exe" 2^>nul') do (
  copy /y "dist_installer\%%f" "%RELEASE_DIR%\%%f" >nul
  goto :copied_gui_inst
)
:copied_gui_inst

if exist "version.json" copy /y "version.json" "%RELEASE_DIR%\version.json" >nul

if exist "README.md" copy /y "README.md" "%RELEASE_DIR%\README.md" >nul
if exist "CHANGELOG.md" copy /y "CHANGELOG.md" "%RELEASE_DIR%\CHANGELOG.md" >nul
if exist "SECURITY.md" copy /y "SECURITY.md" "%RELEASE_DIR%\SECURITY.md" >nul
if exist "LICENSE.txt" copy /y "LICENSE.txt" "%RELEASE_DIR%\LICENSE.txt" >nul
if exist "LICENSE" copy /y "LICENSE" "%RELEASE_DIR%\LICENSE" >nul

powershell -NoProfile -Command ^
  "if (Test-Path '%ZIP_NAME%') {Remove-Item -Force '%ZIP_NAME%'}; Compress-Archive -Path '%RELEASE_DIR%\*' -DestinationPath '%ZIP_NAME%'" >nul

echo Release ZIP created:
echo   %ZIP_NAME%
exit /b 0
