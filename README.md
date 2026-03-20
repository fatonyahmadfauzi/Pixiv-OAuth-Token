# Pixiv OAuth Token

> 🌐 Available in other languages: [Polski](docs/lang/README-PL.md) | [中文](docs/lang/README-ZH.md) | [日本語](docs/lang/README-JP.md) | [Deutsch](docs/lang/README-DE.md) | [Français](docs/lang/README-FR.md) | [Español](docs/lang/README-ES.md) | [Русский](docs/lang/README-RU.md) | [Português](docs/lang/README-PT.md) | [Bahasa Indonesia](docs/lang/README-ID.md) | [한국어](docs/lang/README-KR.md)


A toolkit to generate Pixiv OAuth tokens in three modes:

- CLI (`pixiv_login.py`)
- GUI (`pixiv_login_gui.py`)
- Web app (`public/` + serverless API)

## Requirements

- Python 3.11+
- Windows (required for `.bat` build scripts and Inno Setup installer)
- Python dependencies from `requirements.txt`

## Run from source

```bash
python -m pip install -r requirements.txt
python pixiv_login.py
```

Run GUI:

```bash
python pixiv_login_gui.py
```

## Build

### Build all artifacts (CLI + GUI + Installer + ZIP)

```bat
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
build_all_pro.bat patch noinst nosign
```

### Main outputs

- Portable CLI: `dist_portable\Pixiv OAuth CLi (Portable).exe`
- Portable GUI: `dist_gui\Pixiv OAuth GUi (Portable).exe`
- Installer CLI: `dist_installer\Pixiv OAuth CLi Setup_v<version>.exe`
- Installer GUI: `dist_installer\Pixiv OAuth GUi Setup_v<version>.exe`
- Release ZIP: `PixivOAuthRelease_v<version>.zip`
- Auto-synced folder: `downloads/` (latest portable/setup + release ZIP)

## Signing

Edit `sign_auto.bat`:

- `PFX_PATH`
- `PFX_PASS`
- `TS_URL`

If the PFX file is missing, signing is skipped.

## Versioning

Application version is stored in `version.json`.

## Web version (Vercel)

A highly optimized, responsive web app featuring dynamic multi-language support (11 languages with auto-detection) and comprehensive SEO metadata.

### Key Web Features
- **Extensive Pages**: Homepage, Downloads, Tutorial, Contact, Issues & PRs, Discussions Tracker, Documentation Markdown viewer, and Support/Donate integration.
- **Advanced SEO**: Auto-injected localized `<meta>` tags, extensive JSON-LD structured data (Sitelinks, SoftwareApplication, etc.), automated `hreflang` generation, `robots.txt`, and `sitemap.xml`.
- **Security & Performance**: Automatic JavaScript obfuscation (extreme mangling), HTML/CSS minification (via `node build_minify.js`), and clean `XSS` prevention via `escapeHTML`.
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
> If you make changes to HTML, CSS, or JS, remember to run `node build_minify.js` before deploying to automatically obfuscate the code and compress assets.

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
python -m pip install -r requirements.txt
```

Or install directly from GitHub:

```bash
python -m pip install "git+https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token.git"
```

## License

MIT License. See `LICENSE`.
