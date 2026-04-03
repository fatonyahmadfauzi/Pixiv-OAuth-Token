# Pixiv OAuth Token

> 🌐 Available in other languages: [Polski](web/public/docs/lang/README-PL.md) | [中文](web/public/docs/lang/README-ZH.md) | [日本語](web/public/docs/lang/README-JP.md) | [Deutsch](web/public/docs/lang/README-DE.md) | [Français](web/public/docs/lang/README-FR.md) | [Español](web/public/docs/lang/README-ES.md) | [Русский](web/public/docs/lang/README-RU.md) | [Português](web/public/docs/lang/README-PT.md) | [Bahasa Indonesia](web/public/docs/lang/README-ID.md) | [한국어](web/public/docs/lang/README-KR.md)


A toolkit to generate Pixiv OAuth tokens in three modes:

- CLI (`app/pixiv_login.py`)
- GUI (`app/pixiv_login_gui.py`)
- Web app (`web/public/` + serverless API)

## Requirements

- Python 3.11+
- Windows (required for `.bat` build scripts and Inno Setup installer)
- Python dependencies from `app/requirements.txt`

## Run from source

```bash
cd app
python -m pip install -r requirements.txt
python pixiv_login.py
```

Run GUI:

```bash
cd app
python pixiv_login_gui.py
```

### GUI Features

| Feature             | Description                                                                                                                                                                                                       |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Multi-language**  | 11 languages — auto-detected from config, switchable live via dropdown                                                                                                                                            |
| **⚙ Debug Console** | Button in top-right header; opens a dark terminal logging **all** events (button clicks, language changes, HTTP requests, PKCE steps, clipboard, config saves, warnings) in real-time and in the current language |
| **Token Exchange**  | Paste pixiv:// URL or raw code → exchange for access + refresh token                                                                                                                                              |
| **Refresh Token**   | One-click refresh using saved refresh_token from config                                                                                                                                                           |
| **Copy Tokens**     | Copy access_token / refresh_token to clipboard instantly                                                                                                                                                          |
| **Tutorial**        | Step-by-step image guide built into the app                                                                                                                                                                       |

## Build

### Build all artifacts (CLI + GUI + Installer + ZIP)

```bat
cd scripts
build_all_pro.bat patch
```

Version argument:

- `patch`
- `minor`
- `major`
- `none`

Optional flags:

- `noinst` (skip installer)
- `nosign` (skip signing)
- `nozip` (skip zip)
- `nogui` (skip GUI)
- `nopause` (no pause at the end)

Example:

```bat
cd scripts
build_all_pro.bat patch noinst nosign
```

### Main outputs

- Portable CLI: `dist_portable\Pixiv OAuth CLi (Portable).exe`
- Portable GUI: `dist_gui\Pixiv OAuth GUi (Portable).exe`
- Unified Installer: `dist_installer\PixivLoginSetup_v<version>.exe` (Installs both CLI + GUI)
- Installer CLI: `dist_installer\Pixiv OAuth CLi Setup_v<version>.exe` (Copy of unified installer)
- Installer GUI: `dist_installer\Pixiv OAuth GUi Setup_v<version>.exe` (Copy of unified installer)
- Release ZIP: `PixivOAuthRelease_v<version>.zip`
- Auto-synced folder: `downloads/` (latest portable/setup + release ZIP)

## Signing

Edit `scripts/sign_auto.bat`:

- `PFX_PATH`
- `PFX_PASS`
- `TS_URL`

If the PFX file is missing, signing is skipped.

## Versioning

Application version/build identity is stored in `version.json`.

- `version`: semantic version (`X.Y.Z`)
- `build_code`: unique build identifier

Default non-release fallback is now `BUILD-UNKNOWN` (instead of `REL-LOCAL`), while release bumps generate unix-style build codes via `scripts/bump_version.py`:

- `REL-U<unix_ms>`

## Web version (Vercel)

A highly optimized, responsive web app featuring dynamic multi-language support (11 languages with auto-detection) and comprehensive SEO metadata.

### Key Web Features

- **Extensive Pages**: Homepage, Downloads, Tutorial, Contact, Issues & PRs, Discussions Tracker, Documentation Markdown viewer, and Support/Donate integration.
- **Advanced SEO**: Auto-injected localized `<meta>` tags, extensive JSON-LD structured data (Sitelinks, SoftwareApplication, etc.), automated `hreflang` generation, `robots.txt`, and `sitemap.xml`.
- **Security & Performance**: Automatic JavaScript obfuscation (extreme mangling), HTML/CSS minification (via `cd web && node build_minify.js`), and clean `XSS` prevention via `escapeHTML`.
- **GitHub API Proxy**: Serverless Vercel endpoints (`/api/github`) proxy GitHub API requests using a Personal Access Token (`GITHUB_PAT`) to completely bypass public rate limits.

### Deploy to Vercel

1. Push repository to GitHub.
2. Vercel → **Add New...** → **Project** → import this repo.
3. Set your Environment Variables in Vercel:
   - `PIXIV_CLIENT_SECRET`: Your Pixiv OAuth client secret.
   - `GITHUB_PAT`: Optional but highly recommended (Your GitHub Personal Access Token to avoid rate limits on repo issues & releases).
4. `vercel.json` already configures:
   - Clean URLs (stripping `.html`)
   - Static hosting from `public/`
   - Serverless APIs at `/api/*`
   - Built-in Custom 404 page routing
   - Far-future caching via Edge Cache headers.
5. Deploy.

> [!IMPORTANT]
> If you make changes to HTML, CSS, or JS, remember to run `cd web && node build_minify.js` before deploying to automatically obfuscate the code and compress assets.

> Security note: for production, always set `PIXIV_CLIENT_SECRET` in your Vercel project environment variables.

## Download application (latest release)

Base URL:

`https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest/download`

Files:

- Portable GUI: `Pixiv OAuth GUi (Portable).exe`
- Setup GUI: `Pixiv OAuth GUi Setup_v<version>.exe`
- Portable CLI: `Pixiv OAuth CLi (Portable).exe`
- Setup CLI: `Pixiv OAuth CLi Setup_v<version>.exe`

### PowerShell (auto-detect latest release assets)

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

### PowerShell (fixed URLs from `downloads/`)

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

Run this in **PowerShell** (not CMD).

If you only run:

```powershell
$guiPortable = "..."
```

and nothing appears, that is expected. It only stores a value in a variable. Download starts when you run `Invoke-WebRequest`.

After download finishes and PowerShell returns to `PS C:\...>` with no error:

```powershell
Get-ChildItem "Pixiv OAuth GUi (Portable).exe"
Start-Process ".\Pixiv OAuth GUi (Portable).exe"
```

For installer build:

```powershell
Invoke-WebRequest $guiSetup -OutFile "Pixiv OAuth GUi Setup.exe"
Start-Process ".\Pixiv OAuth GUi Setup.exe"
```

If TLS policy blocks download:

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```

### CMD (auto-detect latest release assets)

```cmd
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi Setup.exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi Setup.exe"
```

## Python install

```bash
cd app
python -m pip install -r requirements.txt
```

Or install directly from GitHub:

```bash
python -m pip install "git+https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token.git"
```

## 🧾 Changelog

See all notable changes for each version in the [CHANGELOG.md](CHANGELOG.md) file.  
📦 You can also view release notes directly on the [GitHub Releases page](https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases).

### Latest: v1.0.5 (2026-04-03)

**✨ Added**

- **Internet-Aware GUI Startup** — Smart connection pre-flight check before booting the GUI, complete with live runtime connection monitoring.
- **Native GUI Documentation Modals** — Terms & Conditions, Privacy Policy, and Changelog are now presented in dynamic popups directly rather than forcing web redirects.
- **Comprehensive Terminal Localizations** — The GitHub CLI tracker and legal pages are now authentically translated across all 11 supported languages.

**✨ Changed & Fixed**

- **Automated Digital Code Signing** — All executables natively bundle self-signed identity to suppress Windows SmartScreen.
- **Installer Properties Bug** — Setup executables properly broadcast `1.0.5.0` File Versions strictly into the Windows PE headers instead of defaulting to zeros.
- **Redesigned CLI Aesthetics** — UI box borders were eradicated for a sleek left-aligned terminal display.

**🔜 Coming in next update**

- Mobile web support — the web app will gain full responsive layout for mobile browsers.

## License

MIT License. See `LICENSE`.
