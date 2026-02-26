#define MyAppName "Pixiv Login CLI"
#define MyAppVersion "1.0.4"
#define MyAppPublisher "Faton Dev"
#define MyAppURL "https://example.com"
#define MyAppExeName "pixiv_login_plus.exe"

[Setup]
AppId={{A8D1A0C4-7A8A-4A8A-9F1E-33C0E6E6F9A1}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName=Pixiv Login CLI
DisableProgramGroupPage=yes
OutputDir=dist_installer
OutputBaseFilename=PixivLoginSetup_v{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern

SetupIconFile=pixiv_login_pro.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "dist_portable\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
