@echo off
setlocal enabledelayedexpansion

REM ========= SIGNING GUIDE =========
REM Signing reduces warnings, but SmartScreen can still warn until reputation builds.
REM EV certificates usually build SmartScreen trust faster than OV.

REM --- Method A: PFX ---
set PFX_PATH=YOUR_CERT.pfx
set PFX_PASS=YOUR_PASSWORD

REM --- Method B: Cert store thumbprint ---
set THUMBPRINT=

set TS_URL=http://timestamp.digicert.com

set PORTABLE=dist_portable\pixiv_login_plus.exe

for /f "delims=" %%f in ('dir /b /o:-d dist_installer\PixivLoginSetup_v*.exe 2^>nul') do (
  set INSTALLER=dist_installer\%%f
  goto :found
)
:found

if not "%THUMBPRINT%"=="" (
  set SIGNCMD=signtool sign /sha1 "%THUMBPRINT%" /tr "%TS_URL%" /td sha256 /fd sha256
) else (
  set SIGNCMD=signtool sign /f "%PFX_PATH%" /p "%PFX_PASS%" /tr "%TS_URL%" /td sha256 /fd sha256
)

if exist "%PORTABLE%" %SIGNCMD% "%PORTABLE%"
if not "%INSTALLER%"=="" if exist "%INSTALLER%" %SIGNCMD% "%INSTALLER%"

echo Done.
pause
