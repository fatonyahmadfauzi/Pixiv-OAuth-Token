# Pixiv OAuth Token


> 🌐 Dostępne w innych językach: [English](../../README.md) | [中文](README-ZH.md) | [日本語](README-JP.md) | [Deutsch](README-DE.md) | [Français](README-FR.md) | [Español](README-ES.md) | [Русский](README-RU.md) | [Português](README-PT.md) | [Bahasa Indonesia](README-ID.md) | [한국어](README-KR.md)

---
Zestaw narzędzi do generowania tokenów Pixiv OAuth w trzech trybach:

- Interfejs wiersza polecenia (`pixiv_login.py`)
- GUI (`pixiv_login_gui.py`)
- Aplikacja internetowa (`public/` + bezserwerowe API)

## Wymagania

- Python 3.11+
- Windows (wymagany dla skryptów kompilacji `.bat` i instalatora Inno Setup)
- Zależności Pythona od `requirements.txt`

## Uruchom ze źródła

```bash
python -m pip install -r requirements.txt
python pixiv_login.py
```

Uruchom interfejs graficzny:

```bash
python pixiv_login_gui.py
```

## Zbudować

### Zbuduj wszystkie artefakty (CLI + GUI + Instalator + ZIP)

```bat
build_all_pro.bat patch
```

Argument wersji:

- `patch`
- `minor`
- `major`
- `none`

Opcjonalne flagi:

- `noinst` (pomiń instalację)
- `nosign` (pomiń podpisywanie)
- `nozip` (pomiń zip)
- `nogui` (pomiń GUI)
- `nopause` (bez pauzy na końcu)

Przykład:

```bat
build_all_pro.bat patch noinst nosign
```

### Główne wyjścia

- Przenośny CLI: `dist_portable\Pixiv OAuth CLi (Portable).exe`
- Przenośny graficzny interfejs użytkownika: `dist_gui\Pixiv OAuth GUi (Portable).exe`
- Instalator CLI: `dist_installer\Pixiv OAuth CLi Setup_v<version>.exe`
- GUI instalatora: `dist_installer\Pixiv OAuth GUi Setup_v<version>.exe`
- Zwolnij kod pocztowy: `PixivOAuthRelease_v<version>.zip`
- Folder automatycznie synchronizowany: `downloads/` (najnowsza wersja przenośna/konfiguracja + wersja ZIP)

## Podpisywanie

Edytuj `sign_auto.bat`:

- `PFX_PATH`
- `PFX_PASS`
- `TS_URL`

Jeśli brakuje pliku PFX, podpisywanie jest pomijane.

## Wersja

Wersja aplikacji jest przechowywana w `version.json`.

## Wersja internetowa (Vercel)

Wysoce zoptymalizowana, responsywna aplikacja internetowa z dynamiczną obsługą wielu języków (11 języków z automatycznym wykrywaniem) i kompleksowymi metadanymi SEO.

### Kluczowe funkcje internetowe
- **Rozbudowane strony**: strona główna, pliki do pobrania, samouczek, kontakt, problemy i PR, narzędzie do śledzenia dyskusji, przeglądarka dokumentacji Markdown oraz integracja wsparcia/darowizn.
- **Zaawansowane SEO**: automatycznie wstrzykiwane zlokalizowane tagi `<meta>`, obszerne dane strukturalne JSON-LD (linki do podstron, aplikacje programowe itp.), automatyczne generowanie `hreflang`, `robots.txt` i `sitemap.xml`.
- **Bezpieczeństwo i wydajność**: Automatyczne zaciemnianie kodu JavaScript (ekstremalne zniekształcanie), minifikacja HTML/CSS (przez `node build_minify.js`) i czyste zapobieganie `XSS` poprzez `escapeHTML`.
- **GitHub API Proxy**: bezserwerowe punkty końcowe Vercel (`/api/github`) żądania proxy GitHub API korzystające z tokenu dostępu osobistego (`GITHUB_PAT`) w celu całkowitego ominięcia publicznych limitów szybkości.

### Wdróż w Vercel

1. Prześlij repozytorium do GitHuba.
2. Vercel → **Dodaj nowy...** → **Projekt** → zaimportuj to repozytorium.
3. Ustaw zmienne środowiskowe w Vercel:
- `PIXIV_CLIENT_SECRET`: Twój sekret klienta Pixiv OAuth.
- `GITHUB_PAT`: Opcjonalny, ale wysoce zalecany (Twój osobisty token dostępu GitHub, aby uniknąć ograniczeń szybkości w przypadku problemów i wydań repo).
4. `vercel.json` już konfiguruje:
- Wyczyść adresy URL (usuwanie `.html`)
- Hosting statyczny od `public/`
- Bezserwerowe interfejsy API w `/api/*`
- Wbudowane niestandardowe routing stron 404
- Buforowanie dalekiej przyszłości poprzez nagłówki Edge Cache.
5. Wdróż.

> [!WAŻNE]
> Jeśli wprowadzasz zmiany w HTML, CSS lub JS, pamiętaj o uruchomieniu `node build_minify.js` przed wdrożeniem, aby automatycznie zaciemnić kod i skompresować zasoby.

> Uwaga dotycząca bezpieczeństwa: w przypadku produkcji zawsze ustawiaj `PIXIV_CLIENT_SECRET` w zmiennych środowiskowych projektu Vercel.

## Pobierz aplikację (najnowsza wersja)

Bazowy adres URL:

`https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest/download`

Akta:

- Przenośny graficzny interfejs użytkownika: `Pixiv OAuth GUi (Portable).exe`
- Skonfiguruj GUI: `Pixiv OAuth GUi Setup_v<version>.exe`
- Przenośny CLI: `Pixiv OAuth CLi (Portable).exe`
- Skonfiguruj CLI: `Pixiv OAuth CLi Setup_v<version>.exe`

### PowerShell (automatycznie wykrywa zasoby najnowszej wersji)

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

### PowerShell (stałe adresy URL z `downloads/`)

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

Uruchom to w **PowerShell** (nie CMD).

Jeśli uruchamiasz tylko:

```powershell
$guiPortable = "..."
```

i nic się nie pojawia, tego można się spodziewać. Przechowuje tylko wartość w zmiennej. Pobieranie rozpoczyna się po uruchomieniu `Invoke-WebRequest`.

Po zakończeniu pobierania i PowerShell powróci do `PS C:\...>` bez błędu:

```powershell
Get-ChildItem "Pixiv OAuth GUi (Portable).exe"
Start-Process ".\Pixiv OAuth GUi (Portable).exe"
```

W przypadku kompilacji instalatora:

```powershell
Invoke-WebRequest $guiSetup -OutFile "Pixiv OAuth GUi Setup.exe"
Start-Process ".\Pixiv OAuth GUi Setup.exe"
```

Jeśli zasady TLS blokują pobieranie:

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```

### CMD (automatycznie wykrywa najnowsze zasoby wersji)

```cmd
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi Setup.exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi Setup.exe"
```

## Instalacja Pythona

```bash
python -m pip install -r requirements.txt
```

Lub zainstaluj bezpośrednio z GitHub:

```bash
python -m pip install "git+https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token.git"
```

## Licencja

MIT License. Zobacz `LICENSE`.
