@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

REM ==========================================================
REM build_release_zip.bat (FINAL)
REM Creates: PixivLoginRelease_vX.Y.Z.zip
REM Contents:
REM   - dist_portable\pixiv_login_plus.exe
REM   - dist_gui\pixiv_login_gui.exe
REM   - latest dist_installer\PixivLoginSetup_v*.exe (if exists)
REM   - version.json
REM   - README.md / CHANGELOG.md / LICENSE* / SECURITY.md (if exists)
REM ==========================================================

for /f "usebackq delims=" %%v in (`python -c "import json;print(json.load(open('version.json'))['version'])"`) do set VER=%%v

set RELEASE_DIR=release
set ZIP_NAME=PixivLoginRelease_v%VER%.zip

if not exist "%RELEASE_DIR%" mkdir "%RELEASE_DIR%"
del /q "%RELEASE_DIR%\*" 2>nul

if exist "dist_portable\pixiv_login_plus.exe" copy /y "dist_portable\pixiv_login_plus.exe" "%RELEASE_DIR%\pixiv_login_plus.exe" >nul
if exist "dist_gui\pixiv_login_gui.exe" copy /y "dist_gui\pixiv_login_gui.exe" "%RELEASE_DIR%\pixiv_login_gui.exe" >nul

for /f "delims=" %%f in ('dir /b /o:-d dist_installer\PixivLoginSetup_v*.exe 2^>nul') do (
  copy /y "dist_installer\%%f" "%RELEASE_DIR%\%%f" >nul
  goto :copied_inst
)
:copied_inst

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
