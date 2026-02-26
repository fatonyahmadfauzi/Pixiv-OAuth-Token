@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

REM Read version from version.json using Python (already in project)
for /f "usebackq delims=" %%v in (`python -c "import json;print(json.load(open('version.json'))['version'])"`) do set VER=%%v

set RELEASE_DIR=release
set ZIP_NAME=PixivLoginRelease_v%VER%.zip

if not exist "%RELEASE_DIR%" mkdir "%RELEASE_DIR%"

REM Copy portable + installer latest (if exists)
if exist "dist_portable\pixiv_login_plus.exe" (
  copy /y "dist_portable\pixiv_login_plus.exe" "%RELEASE_DIR%\pixiv_login_plus.exe" >nul
)

for /f "delims=" %%f in ('dir /b /o:-d dist_installer\PixivLoginSetup_v*.exe 2^>nul') do (
  copy /y "dist_installer\%%f" "%RELEASE_DIR%\%%f" >nul
  goto :copied_inst
)
:copied_inst

REM Optional: copy docs/config
if exist "README.md" copy /y "README.md" "%RELEASE_DIR%\README.md" >nul
if exist "version.json" copy /y "version.json" "%RELEASE_DIR%\version.json" >nul

REM Create ZIP using PowerShell
powershell -NoProfile -Command ^
  "if (Test-Path '%ZIP_NAME%') {Remove-Item -Force '%ZIP_NAME%'}; Compress-Archive -Path '%RELEASE_DIR%\*' -DestinationPath '%ZIP_NAME%'" >nul

echo Release ZIP created:
echo   %ZIP_NAME%
exit /b 0