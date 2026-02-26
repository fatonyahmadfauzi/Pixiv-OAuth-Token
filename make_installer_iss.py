#!/usr/bin/env python
import json, os

ROOT = os.path.dirname(__file__)
VERSION_FILE = os.path.join(ROOT, "version.json")
OUT_ISS = os.path.join(ROOT, "pixiv_login_installer.iss")

# Customize these:
APP_NAME = "Pixiv Login CLI"
PUBLISHER = "Faton Dev"
APP_EXE_NAME = "pixiv_login_plus.exe"
APP_URL = "https://example.com"  # optional
DEFAULT_GROUP = "Pixiv Login CLI"
APP_ID_GUID = "A8D1A0C4-7A8A-4A8A-9F1E-33C0E6E6F9A1"

def main():
    with open(VERSION_FILE, "r", encoding="utf-8") as f:
        version = json.load(f)["version"]

    iss = f"""#define MyAppName \"{APP_NAME}\"
#define MyAppVersion \"{version}\"
#define MyAppPublisher \"{PUBLISHER}\"
#define MyAppURL \"{APP_URL}\"
#define MyAppExeName \"{APP_EXE_NAME}\"

[Setup]
AppId={{{{{APP_ID_GUID}}}}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
AppPublisherURL={{#MyAppURL}}
AppSupportURL={{#MyAppURL}}
AppUpdatesURL={{#MyAppURL}}
DefaultDirName={{autopf}}\\{{#MyAppName}}
DefaultGroupName={DEFAULT_GROUP}
DisableProgramGroupPage=yes
OutputDir=dist_installer
OutputBaseFilename=PixivLoginSetup_v{{#MyAppVersion}}
Compression=lzma
SolidCompression=yes
WizardStyle=modern

SetupIconFile=pixiv_login_pro.ico
UninstallDisplayIcon={{app}}\\{{#MyAppExeName}}

[Languages]
Name: \"english\"; MessagesFile: \"compiler:Default.isl\"

[Tasks]
Name: \"desktopicon\"; Description: \"Create a &desktop shortcut\"; GroupDescription: \"Additional icons:\"; Flags: unchecked

[Files]
Source: \"dist_portable\\{{#MyAppExeName}}\"; DestDir: \"{{app}}\"; Flags: ignoreversion

[Icons]
Name: \"{{group}}\\{{#MyAppName}}\"; Filename: \"{{app}}\\{{#MyAppExeName}}\"
Name: \"{{commondesktop}}\\{{#MyAppName}}\"; Filename: \"{{app}}\\{{#MyAppExeName}}\"; Tasks: desktopicon

[Run]
Filename: \"{{app}}\\{{#MyAppExeName}}\"; Description: \"Launch {{#MyAppName}}\"; Flags: nowait postinstall skipifsilent
"""

    with open(OUT_ISS, "w", encoding="utf-8") as f:
        f.write(iss)

    print(f"Wrote {OUT_ISS} (version {version})")

if __name__ == "__main__":
    main()
