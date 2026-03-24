@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0\.."

REM ==========================================================
REM scripts\build_release_zip.bat
REM Creates: dist_release\PixivOAuthRelease_vX.Y.Z.zip
REM Source priority:
REM   1) downloads\ (if present)
REM   2) dist_* / root fallback
REM ==========================================================

for /f "usebackq delims=" %%v in (`python -c "import json;d=json.load(open('version.json'));print(d.get('version','0.0.0'))"`) do set VER=%%v
for /f "usebackq delims=" %%b in (`python -c "import json;d=json.load(open('version.json'));print(d.get('build_code','REL-LOCAL'))"`) do set BCODE=%%b

set RELEASE_DIR=release
set ZIP_OUT_DIR=dist_release
set ZIP_NAME=%ZIP_OUT_DIR%\PixivOAuthRelease_v%VER%_%BCODE%.zip

if not exist "%RELEASE_DIR%" mkdir "%RELEASE_DIR%"
if not exist "%ZIP_OUT_DIR%" mkdir "%ZIP_OUT_DIR%"
del /q "%RELEASE_DIR%\*" 2>nul
del /q "%ZIP_OUT_DIR%\PixivOAuthRelease_v*.zip" 2>nul
del /q "downloads\PixivOAuthRelease_v*.zip" 2>nul

REM --- Portable (prefer downloads/) ---
if exist "downloads\Pixiv OAuth CLi (Portable).exe" (
  copy /y "downloads\Pixiv OAuth CLi (Portable).exe" "%RELEASE_DIR%\Pixiv OAuth CLi (Portable).exe" >nul
) else if exist "dist_portable\Pixiv OAuth CLi (Portable).exe" (
  copy /y "dist_portable\Pixiv OAuth CLi (Portable).exe" "%RELEASE_DIR%\Pixiv OAuth CLi (Portable).exe" >nul
)

if exist "downloads\Pixiv OAuth GUi (Portable).exe" (
  copy /y "downloads\Pixiv OAuth GUi (Portable).exe" "%RELEASE_DIR%\Pixiv OAuth GUi (Portable).exe" >nul
) else if exist "dist_gui\Pixiv OAuth GUi (Portable).exe" (
  copy /y "dist_gui\Pixiv OAuth GUi (Portable).exe" "%RELEASE_DIR%\Pixiv OAuth GUi (Portable).exe" >nul
)

REM --- Installer (prefer downloads/latest alias) ---
if exist "downloads\Pixiv OAuth CLi Setup_latest.exe" (
  copy /y "downloads\Pixiv OAuth CLi Setup_latest.exe" "%RELEASE_DIR%\Pixiv OAuth CLi Setup_v%VER%_%BCODE%.exe" >nul
) else (
  for /f "delims=" %%f in ('dir /b /o:-d "downloads\Pixiv OAuth CLi Setup_v*.exe" 2^>nul') do (
    copy /y "downloads\%%f" "%RELEASE_DIR%\%%f" >nul
    goto :copied_cli_inst
  )
  for /f "delims=" %%f in ('dir /b /o:-d "dist_installer\Pixiv OAuth CLi Setup_v*.exe" 2^>nul') do (
    copy /y "dist_installer\%%f" "%RELEASE_DIR%\%%f" >nul
    goto :copied_cli_inst
  )
)
:copied_cli_inst

if exist "downloads\Pixiv OAuth GUi Setup_latest.exe" (
  copy /y "downloads\Pixiv OAuth GUi Setup_latest.exe" "%RELEASE_DIR%\Pixiv OAuth GUi Setup_v%VER%_%BCODE%.exe" >nul
) else (
  for /f "delims=" %%f in ('dir /b /o:-d "downloads\Pixiv OAuth GUi Setup_v*.exe" 2^>nul') do (
    copy /y "downloads\%%f" "%RELEASE_DIR%\%%f" >nul
    goto :copied_gui_inst
  )
  for /f "delims=" %%f in ('dir /b /o:-d "dist_installer\Pixiv OAuth GUi Setup_v*.exe" 2^>nul') do (
    copy /y "dist_installer\%%f" "%RELEASE_DIR%\%%f" >nul
    goto :copied_gui_inst
  )
)
:copied_gui_inst

if exist "version.json" copy /y "version.json" "%RELEASE_DIR%\version.json" >nul
if exist "README.md" (
  if exist "scripts\clean_readme_for_release.py" (
    python scripts\clean_readme_for_release.py "README.md" "%RELEASE_DIR%\README.md"
  ) else (
    copy /y "README.md" "%RELEASE_DIR%\README.md" >nul
  )
)
if exist "CHANGELOG.md" copy /y "CHANGELOG.md" "%RELEASE_DIR%\CHANGELOG.md" >nul
if exist "SECURITY.md" copy /y "SECURITY.md" "%RELEASE_DIR%\SECURITY.md" >nul
if exist "LICENSE.txt" copy /y "LICENSE.txt" "%RELEASE_DIR%\LICENSE.txt" >nul
if exist "LICENSE" copy /y "LICENSE" "%RELEASE_DIR%\LICENSE" >nul

powershell -NoProfile -Command ^
  "if (Test-Path '%ZIP_NAME%') {Remove-Item -Force '%ZIP_NAME%'}; Compress-Archive -Path '%RELEASE_DIR%\*' -DestinationPath '%ZIP_NAME%'" >nul

echo Release ZIP created:
echo   %ZIP_NAME%
exit /b 0
