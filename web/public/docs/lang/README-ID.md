# Pixiv OAuth Token


> 🌐 Tersedia dalam bahasa lain: [English](../../../../README.md) | [Polski](README-PL.md) | [中文](README-ZH.md) | [日本語](README-JP.md) | [Deutsch](README-DE.md) | [Français](README-FR.md) | [Español](README-ES.md) | [Русский](README-RU.md) | [Português](README-PT.md) | [한국어](README-KR.md)

---

Toolkit untuk menghasilkan token Pixiv OAuth dalam tiga mode:

- CLI (`app/pixiv_login.py`)
- GUI (`app/pixiv_login_gui.py`)
- Aplikasi web (`web/public/` + tanpa server API)

## Persyaratan

- Python 3.11+
- Windows (diperlukan untuk skrip build `.bat` dan penginstal Inno Setup)
- Python ketergantungan dari `app/requirements.txt`

## Jalankan dari sumber

```bash
cd app
python -m pip install -r requirements.txt
python pixiv_login.py
```

Jalankan GUI:

```bash
cd app
python pixiv_login_gui.py
```

### GUI Fitur

| Fitur | Deskripsi |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Multi-bahasa** | 11 bahasa — terdeteksi otomatis dari konfigurasi, dapat dialihkan langsung melalui dropdown |
| **⚙ Konsol Debug** | Tombol di header kanan atas; membuka terminal gelap yang mencatat **semua** peristiwa (klik tombol, perubahan bahasa, permintaan HTTP, langkah PKCE, papan klip, penyimpanan konfigurasi, peringatan) secara real-time dan dalam bahasa saat ini |
| **Penukaran Token** | Tempel URL pixiv:// atau kode mentah → tukarkan dengan akses + token penyegaran |
| **Segarkan Token** | Penyegaran sekali klik menggunakan refresh_token yang disimpan dari config |
| **Salin Token** | Salin access_token / refresh_token ke clipboard secara instan |
| **Tutorial** | Panduan gambar langkah demi langkah yang ada di dalam aplikasi |

## Membangun

### Bangun semua artefak (CLI + GUI + Pemasang + ZIP)

```bat
cd scripts
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
cd scripts
build_all_pro.bat patch noinst nosign
```

### Keluaran utama

- Portabel CLI: `dist_portable\Pixiv OAuth CLi (Portable).exe`
- Portabel GUI: `dist_gui\Pixiv OAuth GUi (Portable).exe`
- Penginstal Terpadu: `dist_installer\PixivLoginSetup_v<version>.exe` (Menginstal CLI + GUI)
- Pemasang CLI: `dist_installer\Pixiv OAuth CLi Setup_v<version>.exe` (Salinan pemasang terpadu)
- Pemasang GUI: `dist_installer\Pixiv OAuth GUi Setup_v<version>.exe` (Salinan pemasang terpadu)
- Rilis ZIP: `PixivOAuthRelease_v<version>.zip`
- Folder yang disinkronkan otomatis: `downloads/` (portabel/pengaturan terbaru + rilis ZIP)

## Penandatanganan

Sunting `scripts/sign_auto.bat`:

- `PFX_PATH`
- `PFX_PASS`
- `TS_URL`

Jika file PFX hilang, penandatanganan dilewati.

## Pembuatan Versi

Versi aplikasi/identitas build disimpan di `version.json`.

- `version`: versi semantik (`X.Y.Z`)
- `build_code`: pengidentifikasi bangunan unik

Penggantian non-rilis default sekarang adalah `BUILD-UNKNOWN` (bukan `REL-LOCAL`), sedangkan rilis bump menghasilkan kode build gaya unix melalui `scripts/bump_version.py`:

- `REL-U<unix_ms>`

## Versi web (Vercel)

Aplikasi web responsif dan sangat optimal yang menampilkan dukungan multibahasa dinamis (11 bahasa dengan deteksi otomatis) dan metadata SEO komprehensif.

### Fitur Web Utama

- **Halaman Luas**: Beranda, Unduhan, Tutorial, Kontak, Masalah & Humas, Pelacak Diskusi, Penampil Dokumentasi Markdown, dan integrasi Dukungan/Sumbang.
- **SEO Tingkat Lanjut**: Tag `<meta>` lokal yang dimasukkan secara otomatis, data terstruktur JSON-LD yang ekstensif (Tautan Situs, Aplikasi Perangkat Lunak, dll.), pembuatan `hreflang` otomatis, `robots.txt`, dan `sitemap.xml`.
- **Keamanan & Performa**: Kebingungan JavaScript otomatis (pengrusakan ekstrem), minifikasi HTML/CSS (melalui `cd web && node build_minify.js`), dan pencegahan `XSS` bersih melalui `escapeHTML`.
- **GitHub API Proxy**: Permintaan proxy GitHub API titik akhir Vercel tanpa server (`/api/github`) menggunakan Token Akses Pribadi (`GITHUB_PAT`) untuk sepenuhnya melewati batas tarif publik.

### Terapkan ke Vercel

1. Dorong repositori ke GitHub.
2. Vercel → **Tambahkan Baru...** → **Proyek** → impor repo ini.
3. Tetapkan Variabel Lingkungan Anda di Vercel:
- `PIXIV_CLIENT_SECRET`: Rahasia klien Pixiv OAuth Anda.
- `GITHUB_PAT`: Opsional tetapi sangat disarankan (Token Akses Pribadi GitHub Anda untuk menghindari batasan nilai pada masalah & rilis repo).
4. `vercel.json` sudah mengkonfigurasi:
- URL bersih (menghapus `.html`)
- Hosting statis dari `public/`
- APIs tanpa server di `/api/*`
- Perutean halaman 404 Kustom bawaan
- Caching masa depan melalui header Edge Cache.
5. Terapkan.

> [!PENTING]
> Jika Anda membuat perubahan pada HTML, CSS, atau JS, ingatlah untuk menjalankan `cd web && node build_minify.js` sebelum menerapkan untuk mengaburkan kode secara otomatis dan mengompresi aset.

> Catatan keamanan: untuk produksi, selalu setel `PIXIV_CLIENT_SECRET` di variabel lingkungan proyek Vercel Anda.

## Unduh aplikasi (rilis terbaru)

URL Dasar:

`https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest/download`

File:

- Portabel GUI: `Pixiv OAuth GUi (Portable).exe`
- Pengaturan GUI: `Pixiv OAuth GUi Setup_v<version>.exe`
- Portabel CLI: `Pixiv OAuth CLi (Portable).exe`
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

## Python pasang

```bash
cd app
python -m pip install -r requirements.txt
```

Atau instal langsung dari GitHub:

```bash
python -m pip install "git+https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token.git"
```

## 🧾 Catatan Perubahan

Lihat semua perubahan penting untuk setiap versi di file [log perubahan](CHANGELOG-ID.md).
📦 Anda juga dapat melihat catatan rilis langsung di [GitHub halaman Rilis](https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases).

### Terbaru: v1.0.5 (2026-04-03)

**✨ Ditambahkan**

- **Permulaan GUI Sadar Internet** — Pemeriksaan pra-penerbangan koneksi cerdas sebelum mem-boot GUI, lengkap dengan pemantauan koneksi runtime langsung.
- **Modal Dokumentasi GUI Asli** — Syarat & Ketentuan, Kebijakan Privasi, dan Changelog kini disajikan dalam popup dinamis secara langsung daripada memaksa pengalihan web.
- **Lokalisasi Terminal Komprehensif** — Pelacak GitHub CLI dan halaman resmi kini diterjemahkan secara autentik dalam 11 bahasa yang didukung.

**✨ Diubah & Diperbaiki**

- **Penandatanganan Kode Digital Otomatis** — Semua executable secara bawaan menggabungkan identitas yang ditandatangani sendiri untuk menyembunyikan Windows SmartScreen.
- **Bug Properti Penginstal** — Setup executable dengan benar menyiarkan Versi File `1.0.5.0` secara ketat ke dalam header Windows PE alih-alih menetapkan default ke nol.
- **Didesain ulang CLI Estetika** — Batas kotak UI dihilangkan untuk tampilan terminal rata kiri yang ramping.

**🔜 Akan hadir pada pembaruan berikutnya**

- Dukungan web seluler — aplikasi web akan mendapatkan tata letak responsif penuh untuk browser seluler.

## Lisensi

MIT License. Lihat `LICENSE`.
