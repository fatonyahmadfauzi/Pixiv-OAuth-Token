# Pixiv OAuth

Tool untuk mendapatkan token OAuth Pixiv, tersedia dalam mode:

- CLI (`pixiv_login.py`)
- GUI (`pixiv_login_gui.py`)

## Requirements

- Python 3.11+
- Windows (untuk build `.bat` dan installer Inno Setup)
- Dependency Python pada `requirements.txt`

## Jalankan dari source

```bash
python -m pip install -r requirements.txt
python pixiv_login.py
```

Untuk GUI:

```bash
python pixiv_login_gui.py
```

## Build

### Build semua (CLI + GUI + Installer + ZIP)

```bat
build_all_pro.bat patch
```

Argumen versi:

- `patch`
- `minor`
- `major`
- `none`

Flag opsional:

- `noinst` (skip installer)
- `nosign` (skip signing)
- `nozip` (skip zip)
- `nogui` (skip GUI)
- `nopause` (tanpa pause di akhir)

Contoh:

```bat
build_all_pro.bat patch noinst nosign
```

### Output build utama

- Portable CLI: `dist_portable\Pixiv OAuth CLi (Portable).exe`
- Portable GUI: `dist_gui\Pixiv OAuth GUi (Portable).exe`
- Installer CLI: `dist_installer\Pixiv OAuth CLi Setup_v<version>.exe`
- Installer GUI: `dist_installer\Pixiv OAuth GUi Setup_v<version>.exe`
- Release ZIP: `PixivOAuthRelease_v<version>.zip`
- Folder sinkron otomatis: `downloads/` (portable, setup terbaru, Linux bila ada, dan ZIP release).

## Signing

Konfigurasi ada di `sign_auto.bat`:

- `PFX_PATH`
- `PFX_PASS`
- `TS_URL`

Jika file PFX tidak ada, proses signing akan di-skip.

## Versi

Versi aplikasi disimpan di `version.json`.

## Lisensi

Proyek ini dilisensikan di bawah MIT License. Lihat file `LICENSE`.


## Web Version (Netlify / Vercel)

Project ini sekarang punya versi web responsive + SEO metadata + multi-bahasa:

- `public/index.html`
- `public/assets/style.css` (clean UI + responsive + footer)
- `public/assets/app.js` (PKCE + i18n EN/ID/JP)
- API serverless:
  - Vercel: `api/token.js`
  - Netlify: `netlify/functions/token.js`

### Deploy ke Netlify

1. Push repo ke GitHub.
2. Di Netlify: **Add new site** → **Import from Git**.
3. Build settings (otomatis dari `netlify.toml`):
   - Publish directory: `public`
   - Functions directory: `netlify/functions`
4. Tambahkan Environment Variable:
   - `PIXIV_CLIENT_SECRET` = client secret Pixiv kamu.
   - (opsional kompatibilitas typo lama) `PIXV_CLIENT_SECRET` (tanpa huruf "I" setelah PIX)
5. Deploy, lalu buka URL Netlify.

`netlify.toml` sudah menyiapkan redirect `/api/token` -> `/.netlify/functions/token`.

### Deploy ke Vercel

1. Push repo ke GitHub.
2. Di Vercel: **Add New...** → **Project** → import repo ini.
3. `vercel.json` sudah menyiapkan:
   - Static hosting dari folder `public/`
   - Serverless API di `/api/token`
4. Tambahkan Environment Variable:
   - `PIXIV_CLIENT_SECRET` = client secret Pixiv kamu.
   - (opsional kompatibilitas typo lama) `PIXV_CLIENT_SECRET` (tanpa huruf "I" setelah PIX)
5. Deploy, lalu buka URL Vercel.

> Catatan keamanan: fallback `client_secret` bawaan masih ada untuk kompatibilitas script lama, tetapi untuk production sangat disarankan selalu set `PIXIV_CLIENT_SECRET` di platform deploy.




### Urutan Bahasa (seragam di CLI/GUI/Web)

Default bahasa: `en` (🇬🇧 English).

Urutan bahasa:
`🇬🇧 English, 🇵🇱 Polski, 🇨🇳 中文, 🇯🇵 日本語, 🇩🇪 Deutsch, 🇫🇷 Français, 🇪🇸 Español, 🇷🇺 Русский, 🇵🇹 Português, 🇮🇩 Indonesia, 🇰🇷 한국어`

## Struktur Folder (Ringkas)

```
public/
  index.html
  assets/
    app.js
    style.css
api/
  token.js
  _oauthProxy.js
netlify/functions/
  token.js
```


## Kenapa muncul error `API endpoint not found (404)`?

Error ini muncul karena web mencoba request ke endpoint backend (`/api/token` atau `/.netlify/functions/token`) tapi endpoint serverless belum aktif/ter-route.

Penyebab paling umum:
- Belum deploy ke Vercel/Netlify (masih buka file HTML langsung).
- Konfigurasi deploy belum sesuai (`public` untuk static, function untuk backend).
- Endpoint API belum ikut terdeploy.

Solusi cepat:
1. Deploy ke Vercel/Netlify sesuai panduan di bawah.
2. Pastikan endpoint bisa diakses:
   - Vercel: `https://<domain>/api/token`
   - Netlify: `https://<domain>/.netlify/functions/token`
3. Set environment variable `PIXIV_CLIENT_SECRET` (atau alias kompatibel typo: `PIXV_CLIENT_SECRET`).

## Download Aplikasi (Release)

Base release URL (ganti jika repo/fork berbeda):

`https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest/download`

File download:
- Portable GUI: `Pixiv OAuth GUi (Portable).exe`
- Setup GUI: `Pixiv OAuth GUi Setup_v<version>.exe`
- Portable CLI: `Pixiv OAuth CLi (Portable).exe`
- Setup CLI: `Pixiv OAuth CLi Setup_v<version>.exe`
- Linux build: `pixiv_login_plus_linux` (jika disertakan di release)

### PowerShell (langsung download, otomatis versi terbaru)

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
$linux       = Get-AssetUrl "pixiv_login_plus_linux"

Invoke-WebRequest $guiPortable -OutFile "Pixiv OAuth GUi (Portable).exe"
Invoke-WebRequest $cliPortable -OutFile "Pixiv OAuth CLi (Portable).exe"
Invoke-WebRequest $guiSetup    -OutFile "Pixiv OAuth GUi Setup.exe"
Invoke-WebRequest $cliSetup    -OutFile "Pixiv OAuth CLi Setup.exe"
if ($linux) { Invoke-WebRequest $linux -OutFile "pixiv_login_plus_linux" }
```

### CMD (langsung download, otomatis versi terbaru)

```cmd
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi Setup.exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi Setup.exe"
```

### Python package / source install


```bash
python -m pip install -r requirements.txt
```

Atau install langsung dari GitHub:

```bash
python -m pip install "git+https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token.git"
```


### Catatan khusus error Vercel `Deploying outputs... Error: API endpoint not found (404)`

Biasanya ini terjadi karena routing lama `builds/routes` tidak memetakan `api/token.js` dengan benar, atau env var salah ketik.

Checklist perbaikan:
1. Gunakan `vercel.json` berbasis `rewrites` (tanpa `builds`) seperti di repo ini.
2. Pastikan file endpoint ada: `api/token.js`.
3. Pastikan env var benar: `PIXIV_CLIENT_SECRET` (jika terlanjur typo, gunakan alias `PIXV_CLIENT_SECRET`).
4. Redeploy dari commit terbaru.


## Tombol Download di Web

Halaman web sekarang menyediakan tombol download langsung untuk:
- Pixiv OAuth CLi Setup
- Pixiv OAuth CLi (Portable)
- Pixiv OAuth GUi Setup
- Pixiv OAuth GUi (Portable)
- Pixiv OAuth Linux

Sumber download menggunakan URL:
`https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest/download`

Jika ingin menyimpan binary langsung di repo, gunakan folder `downloads/` (sudah tidak di-ignore).
