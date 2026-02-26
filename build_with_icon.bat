@echo off
pip install -r requirements.txt
pyinstaller --onefile ^
  --icon=pixiv_login.ico ^
  --version-file=version_info.txt ^
  pixiv_login_plus.py
pause
