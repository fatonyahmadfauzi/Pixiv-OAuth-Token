@echo off
REM Build Windows .exe using PyInstaller
REM 1) Install Python 3.10+ on Windows
REM 2) pip install -r requirements.txt
REM 3) Run this .bat in the same folder as pixiv_login.py

pyinstaller --onefile --name pixiv_login pixiv_login.py

echo.
echo Build done. Check the dist\ folder for pixiv_login.exe
pause
