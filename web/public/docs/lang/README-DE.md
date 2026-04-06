# Pixiv OAuth Token

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/fatonyahmadfauzi/Pixiv-OAuth-Token?color=success)](https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest)
[![Github All Releases](https://img.shields.io/github/downloads/fatonyahmadfauzi/Pixiv-OAuth-Token/total.svg?color=blue)](https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Windows Build](https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/actions/workflows/windows-release.yml/badge.svg)](https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/actions/workflows/windows-release.yml)

> 🌐 In anderen Sprachen verfügbar: [English](../../../../README.md) | [Polski](README-PL.md) | [中文](README-ZH.md) | [日本語](README-JP.md) | [Français](README-FR.md) | [Español](README-ES.md) | [Русский](README-RU.md) | [Português](README-PT.md) | [Bahasa Indonesia](README-ID.md) | [한국어](README-KR.md)

---
> 🌐 Verfügbar in anderen Sprachen: [Japanisch](web/public/docs/lang/README-JP.md)

Ein Toolkit zum Generieren von Pixiv OAuth-Tokens in drei Modi:

- CLI (`app/pixiv_login.py`)
- GUI (`app/pixiv_login_gui.py`)
- Web-App (`web/public/` + serverlos API)

## Anforderungen

- Python 3.11+
- Windows (erforderlich für `.bat` Build-Skripte und Inno Setup-Installationsprogramm)
- Python Abhängigkeiten von `app/requirements.txt`

## Von der Quelle ausführen

```bash
cd app
python -m pip install -r requirements.txt
python pixiv_login.py
```

Führen Sie GUI aus:

```bash
cd app
python pixiv_login_gui.py
```

### GUI Funktionen

| Funktion | Beschreibung |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mehrsprachig** | 11 Sprachen – automatisch aus der Konfiguration erkannt, live über Dropdown umschaltbar |
| **⚙ Debug-Konsole** | Schaltfläche in der Kopfzeile oben rechts; öffnet ein dunkles Terminal, das **alle** Ereignisse (Schaltflächenklicks, Sprachänderungen, HTTP-Anfragen, PKCE-Schritte, Zwischenablage, Konfigurationsspeicherungen, Warnungen) in Echtzeit und in der aktuellen Sprache protokolliert |
| **Token-Austausch** | Fügen Sie pixiv:// URL oder Rohcode ein → Austausch gegen Zugriffs- und Aktualisierungstoken |
| **Aktualisierungstoken** | Aktualisierung mit einem Klick mit gespeichertem Refresh_token aus der Konfiguration |
| **Token kopieren** | Access_token/refresh_token sofort in die Zwischenablage kopieren |
| **Tutorial** | In die App integrierte Schritt-für-Schritt-Bildanleitung |

## Bauen

### Alle Artefakte erstellen (CLI + GUI + Installer + ZIP)

```bat
cd scripts
build_all_pro.bat patch
```

Versionsargument:

- `patch`
- `minor`
- `major`
- `none`

Optionale Flags:

- `noinst` (Installationsprogramm überspringen)
- `nosign` (Signatur überspringen)
- `nozip` (zip überspringen)
- `nogui` (GUI überspringen)
- `nopause` (keine Pause am Ende)

Beispiel:

```bat
cd scripts
build_all_pro.bat patch noinst nosign
```

### Hauptausgänge

- Tragbar CLI: `dist_portable\Pixiv OAuth CLi (Portable).exe`
- Tragbar GUI: `dist_gui\Pixiv OAuth GUi (Portable).exe`
- Unified Installer: `dist_installer\PixivLoginSetup_v<version>.exe` (Installiert sowohl CLI als auch GUI)
- Installer CLI: `dist_installer\Pixiv OAuth CLi Setup_v<version>.exe` (Kopie des einheitlichen Installers)
- Installer GUI: `dist_installer\Pixiv OAuth GUi Setup_v<version>.exe` (Kopie des einheitlichen Installers)
- Veröffentlichungs-ZIP: `PixivOAuthRelease_v<version>.zip`
- Automatisch synchronisierter Ordner: `downloads/` (neueste Portable/Setup + Release-ZIP-Datei)

## Unterzeichnung

Bearbeiten Sie `scripts/sign_auto.bat`:

- `PFX_PATH`
- `PFX_PASS`
- `TS_URL`

Wenn die PFX-Datei fehlt, wird das Signieren übersprungen.

## Versionierung

Die Anwendungsversion/Build-Identität wird in `version.json` gespeichert.

- `version`: semantische Version (`X.Y.Z`)
- `build_code`: eindeutige Build-ID

Der standardmäßige Nicht-Release-Fallback ist jetzt `BUILD-UNKNOWN` (anstelle von `REL-LOCAL`), während Release-Bumps Build-Codes im Unix-Stil über `scripts/bump_version.py` generieren:

- `REL-U<unix_ms>`

## Webversion (Vercel)

Eine hochoptimierte, reaktionsfähige Web-App mit dynamischer Mehrsprachenunterstützung (11 Sprachen mit automatischer Erkennung) und umfassenden SEO-Metadaten.

### Wichtige Webfunktionen

- **Umfangreiche Seiten**: Homepage, Downloads, Tutorial, Kontakt, Probleme und PRs, Diskussions-Tracker, Dokumentation Markdown-Viewer und Support/Spenden-Integration.
- **Erweiterte SEO**: Automatisch eingefügte lokalisierte `<meta>`-Tags, umfangreiche JSON-LD-strukturierte Daten (Sitelinks, SoftwareApplication usw.), automatisierte `hreflang`-Generierung, `robots.txt` und `sitemap.xml`.
- **Sicherheit und Leistung**: Automatische JavaScript-Verschleierung (extreme Entstellung), HTML/CSS-Minimierung (über `cd web && node build_minify.js`) und saubere `XSS`-Verhinderung über `escapeHTML`.
- **GitHub API Proxy**: Serverlose Vercel Endpunkte (`/api/github`) Proxy GitHub API-Anfragen unter Verwendung eines persönlichen Zugriffstokens (`GITHUB_PAT`), um öffentliche Ratenbeschränkungen vollständig zu umgehen.

### Bereitstellung auf Vercel

1. Repository nach GitHub verschieben.
2. Vercel → **Neu hinzufügen...** → **Projekt** → dieses Repo importieren.
3. Legen Sie Ihre Umgebungsvariablen in Vercel fest:
- `PIXIV_CLIENT_SECRET`: Ihr Pixiv OAuth-Client-Geheimnis.
- `GITHUB_PAT`: Optional, aber dringend empfohlen (Ihr persönlicher GitHub-Zugriffstoken, um Ratenbeschränkungen bei Repo-Problemen und -Releases zu vermeiden).
4. `vercel.json` konfiguriert bereits:
- URLs bereinigen (`.html` entfernen)
- Statisches Hosting von `public/`
- Serverlose APIs bei `/api/*`
- Integriertes benutzerdefiniertes 404-Seitenrouting
- Caching für die ferne Zukunft über Edge-Cache-Header.
5. Bereitstellen.

> [!IMPORTANT]
> Wenn Sie Änderungen an HTML, CSS oder JS vornehmen, denken Sie daran, vor der Bereitstellung `cd web && node build_minify.js` auszuführen, um den Code automatisch zu verschleiern und Assets zu komprimieren.

> Sicherheitshinweis: Legen Sie für die Produktion immer `PIXIV_CLIENT_SECRET` in Ihren Vercel-Projektumgebungsvariablen fest.

## Anwendung herunterladen (neueste Version)

Basis-URL:

`https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest/download`

Dateien:

- Tragbar GUI: `Pixiv OAuth GUi (Portable).exe`
- Setup GUI: `Pixiv OAuth GUi Setup_v<version>.exe`
- Tragbar CLI: `Pixiv OAuth CLi (Portable).exe`
- Setup CLI: `Pixiv OAuth CLi Setup_v<version>.exe`

### PowerShell (Assets der neuesten Version automatisch erkennen)

```powershell
$api = "https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest"
$assets = (Invoke-RestMethod -Uri $api).assets

function Get-AssetUrl([string]$pattern) {
  ($assets | Where-Object { $_.name -match $pattern } | Select-Object -First 1).browser_download_url
}

$guiPortable = Get-AssetUrl "Pixiv OAuth GUi \(Portable\)"
$cliPortable = Get-AssetUrl "Pixiv OAuth CLi \(Portable\)"
$guiSetup    = Get-AssetUrl "Pixiv OAuth GUi Setup"
$cliSetup    = Get-AssetUrl "Pixiv OAuth CLi Setup"

Invoke-WebRequest $guiPortable -OutFile "Pixiv OAuth GUi (Portable).exe"
Invoke-WebRequest $cliPortable -OutFile "Pixiv OAuth CLi (Portable).exe"
Invoke-WebRequest $guiSetup    -OutFile "Pixiv OAuth GUi Setup.exe"
Invoke-WebRequest $cliSetup    -OutFile "Pixiv OAuth CLi Setup.exe"
```

### PowerShell (feste URLs von `downloads/`)

```powershell
$guiPortable = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/raw/HEAD/downloads/Pixiv%20OAuth%20GUi%20(Portable)_latest.exe"
$cliPortable = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/raw/HEAD/downloads/Pixiv%20OAuth%20CLi%20(Portable)_latest.exe"
$guiSetup    = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/raw/HEAD/downloads/Pixiv%20OAuth%20GUi%20Setup_latest.exe"
$cliSetup    = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/raw/HEAD/downloads/Pixiv%20OAuth%20CLi%20Setup_latest.exe"

Invoke-WebRequest $guiPortable -OutFile "Pixiv OAuth GUi (Portable).exe"
Invoke-WebRequest $cliPortable -OutFile "Pixiv OAuth CLi (Portable).exe"
Invoke-WebRequest $guiSetup    -OutFile "Pixiv OAuth GUi Setup.exe"
Invoke-WebRequest $cliSetup    -OutFile "Pixiv OAuth CLi Setup.exe"
```

Führen Sie dies in **PowerShell** (nicht CMD) aus.

Wenn Sie nur ausführen:

```powershell
$guiPortable = "..."
```

und nichts erscheint, was erwartet wird. Es speichert nur einen Wert in einer Variablen. Der Download beginnt, wenn Sie `Invoke-WebRequest` ausführen.

Nachdem der Download abgeschlossen ist und PowerShell ohne Fehler zu `PS C:\...>` zurückkehrt:

```powershell
Get-ChildItem "Pixiv OAuth GUi (Portable).exe"
Start-Process ".\Pixiv OAuth GUi (Portable).exe"
```

Für den Installer-Build:

```powershell
Invoke-WebRequest $guiSetup -OutFile "Pixiv OAuth GUi Setup.exe"
Start-Process ".\Pixiv OAuth GUi Setup.exe"
```

Wenn die TLS-Richtlinie den Download blockiert:

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```

### CMD (Assets der neuesten Version automatisch erkennen)

```cmd
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi Setup.exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi Setup.exe"
```

## Python installieren

```bash
cd app
python -m pip install -r requirements.txt
```

Oder direkt von GitHub installieren:

```bash
python -m pip install "git+https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token.git"
```

## 🧾 Änderungsprotokoll

Sehen Sie sich alle wichtigen Änderungen für jede Version in der Datei [Änderungsprotokoll](CHANGELOG-DE.md) an.
📦 Sie können Versionshinweise auch direkt auf der [GitHub Releases-Seite](https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases). anzeigen.

### Neueste: v1.0.5 (2026-04-03)

**✨ Hinzugefügt**

- **Internet-Aware GUI Startup** – Intelligente Verbindungsprüfung vor dem Start des GUI, komplett mit Live-Laufzeit-Verbindungsüberwachung.
- **Native GUI-Dokumentationsmodalitäten** – Allgemeine Geschäftsbedingungen, Datenschutzrichtlinien und Änderungsprotokoll werden jetzt direkt in dynamischen Popups angezeigt, anstatt Webweiterleitungen zu erzwingen.
- **Umfassende Terminallokalisierungen** – Der GitHub CLI-Tracker und die rechtlichen Seiten sind jetzt authentisch in alle 11 unterstützten Sprachen übersetzt.

**✨ Geändert und behoben**

- **Automatisierte digitale Code-Signierung** – Alle ausführbaren Dateien bündeln nativ eine selbstsignierte Identität, um Windows SmartScreen zu unterdrücken.
- **Installer Properties Bug** – Ausführbare Setup-Dateien übertragen `1.0.5.0`-Dateiversionen ordnungsgemäß ausschließlich in die Windows PE-Header, anstatt standardmäßig auf Nullen zu setzen.
- **Neu gestaltete CLI-Ästhetik** – Die Ränder der UI-Box wurden entfernt, um eine elegante, linksbündige Terminalanzeige zu ermöglichen.

**🔜 Erscheint im nächsten Update**

- Mobile Web-Unterstützung – die Web-App erhält ein vollständig responsives Layout für mobile Browser.

## Lizenz

MIT License. Siehe `LICENSE`.
