# Pixiv OAuth Token


> 🌐 Tersedia dalam bahasa lain: [English](../../README.md) | [Polski](README-PL.md) | [中文](README-ZH.md) | [日本語](README-JP.md) | [Deutsch](README-DE.md) | [Français](README-FR.md) | [Español](README-ES.md) | [Русский](README-RU.md) | [Português](README-PT.md) | [한국어](README-KR.md)

---
Toolkit untuk menghasilkan token Pixiv OAuth dalam tiga mode:

- CLI (`pixiv_login.py`)
- GUI (`pixiv_login_gui.py`)
- Aplikasi web (`public/` + API tanpa server)

## Persyaratan

- Python 3.11+
- Windows (diperlukan untuk skrip build `.bat` dan penginstal Inno Setup)
- Ketergantungan Python dari `requirements.txt`

## Jalankan dari sumber

```bash
python -m pip install -r requirements.txt
python pixiv_login.py
```

Jalankan GUI:

```bash
python pixiv_login_gui.py
```

## Membangun

### Bangun semua artefak (CLI + GUI + Installer + ZIP)

```bat
build_all_pro.bat patch
```

Argumen versi:

- `patch`
- `minor`
- `major`
- `none`

Bendera opsional:

- `noinst` (lewati penginstal)
- `nosign` (lewati penandatanganan)
- `nozip` (lewati zip)
- `nogui` (lewati GUI)
- `nopause` (tidak ada jeda di akhir)

Contoh:

```bat
build_all_pro.bat patch noinst nosign
```

### Keluaran utama

- CLI portabel: `dist_portable\Pixiv OAuth CLi (Portable).exe`
- GUI portabel: `dist_gui\Pixiv OAuth GUi (Portable).exe`
- CLI Pemasang: `dist_installer\Pixiv OAuth CLi Setup_v<version>.exe`
- GUI Pemasang: `dist_installer\Pixiv OAuth GUi Setup_v<version>.exe`
- Rilis ZIP: `PixivOAuthRelease_v<version>.zip`
- Folder yang disinkronkan otomatis: `downloads/` (portabel/pengaturan terbaru + rilis ZIP)

## Penandatanganan

Sunting `sign_auto.bat`:

- `PFX_PATH`
- `PFX_PASS`
- `TS_URL`

Jika file PFX hilang, penandatanganan dilewati.

## Pembuatan Versi

Versi aplikasi disimpan di `version.json`.

## Versi web (Vercel)

Aplikasi web responsif dan sangat optimal yang menampilkan dukungan multibahasa dinamis (11 bahasa dengan deteksi otomatis) dan metadata SEO komprehensif.

### Fitur Web Utama
- **Halaman Luas**: Beranda, Unduhan, Tutorial, Kontak, Masalah & Humas, Pelacak Diskusi, penampil Penurunan Harga Dokumentasi, dan integrasi Dukungan/Sumbangan.
- **SEO Tingkat Lanjut**: Tag `<meta>` lokal yang dimasukkan secara otomatis, data terstruktur JSON-LD yang ekstensif (Tautan Situs, Aplikasi Perangkat Lunak, dll.), pembuatan `hreflang` otomatis, `robots.txt`, dan `sitemap.xml`.
- **Keamanan & Performa**: Kebingungan JavaScript otomatis (pengrusakan ekstrem), minifikasi HTML/CSS (melalui `node build_minify.js`), dan pencegahan `XSS` bersih melalui `escapeHTML`.
- **Proksi API GitHub**: Proksi titik akhir Vercel tanpa server (`/api/github`) meminta API GitHub menggunakan Token Akses Pribadi (`GITHUB_PAT`) untuk sepenuhnya melewati batas tarif publik.

### Terapkan ke Vercel

1. Dorong repositori ke GitHub.
2. Vercel → **Tambahkan Baru...** → **Proyek** → impor repo ini.
3. Atur Variabel Lingkungan Anda di Vercel:
- `PIXIV_CLIENT_SECRET`: Rahasia klien Pixiv OAuth Anda.
- `GITHUB_PAT`: Opsional tetapi sangat disarankan (Token Akses Pribadi GitHub Anda untuk menghindari batasan nilai pada masalah & rilis repo).
4. `vercel.json` sudah mengkonfigurasi:
- URL bersih (menghapus `.html`)
- Hosting statis dari `public/`
- API Tanpa Server di `/api/*`
- Perutean halaman 404 Kustom bawaan
- Caching masa depan melalui header Edge Cache.
5. Terapkan.

> [!PENTING]
> Jika Anda membuat perubahan pada HTML, CSS, atau JS, ingatlah untuk menjalankan `node build_minify.js` sebelum menerapkan untuk mengaburkan kode secara otomatis dan mengompresi aset.

> Catatan keamanan: untuk produksi, selalu setel `PIXIV_CLIENT_SECRET` di variabel lingkungan proyek Vercel Anda.

## Unduh aplikasi (rilis terbaru)

URL Dasar:

`https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest/download`

File:

- GUI portabel: `Pixiv OAuth GUi (Portable).exe`
- Pengaturan GUI: `Pixiv OAuth GUi Setup_v<version>.exe`
- CLI portabel: `Pixiv OAuth CLi (Portable).exe`
- Pengaturan CLI: `Pixiv OAuth CLi Setup_v<version>.exe`

### PowerShell (deteksi otomatis aset rilis terbaru)

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

### PowerShell (URL tetap dari `downloads/`)

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

Jalankan ini di **PowerShell** (bukan CMD).

Jika Anda hanya menjalankan:

```powershell
$guiPortable = "..."
```

dan tidak ada yang muncul, itu yang diharapkan. Itu hanya menyimpan nilai dalam variabel. Pengunduhan dimulai saat Anda menjalankan `Invoke-WebRequest`.

Setelah pengunduhan selesai dan PowerShell kembali ke `PS C:\...>` tanpa kesalahan:

```powershell
Get-ChildItem "Pixiv OAuth GUi (Portable).exe"
Start-Process ".\Pixiv OAuth GUi (Portable).exe"
```

Untuk pembuatan penginstal:

```powershell
Invoke-WebRequest $guiSetup -OutFile "Pixiv OAuth GUi Setup.exe"
Start-Process ".\Pixiv OAuth GUi Setup.exe"
```

Jika kebijakan TLS memblokir pengunduhan:

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```

### CMD (deteksi otomatis aset rilis terbaru)

```cmd
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi Setup.exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi Setup.exe"
```

## Pemasangan piton

```bash
python -m pip install -r requirements.txt
```

Atau instal langsung dari GitHub:

```bash
python -m pip install "git+https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token.git"
```

## Lisensi

MIT License. Lihat `LICENSE`.
