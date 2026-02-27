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

Project ini sekarang punya versi web responsive:

- `index.html`
- `web/style.css`
- `web/app.js`
- API serverless:
  - Vercel: `api/token.js`
  - Netlify: `netlify/functions/token.js`

### Deploy ke Netlify

1. Connect repo ke Netlify.
2. Build command: kosongkan (static + functions).
3. Publish directory: `.`
4. Set environment variable (opsional):
   - `PIXIV_CLIENT_SECRET`

`netlify.toml` sudah menyiapkan redirect `/api/token` -> `/.netlify/functions/token`.

### Deploy ke Vercel

1. Import repo ke Vercel.
2. `vercel.json` sudah menyiapkan route API Node di `/api/token`.
3. Set environment variable (opsional):
   - `PIXIV_CLIENT_SECRET`

> Catatan: default fallback `client_secret` tetap ada untuk kompatibilitas script lama, tapi sangat disarankan pakai environment variable di platform deploy.
