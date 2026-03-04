# Tutorial Lengkap: Pakai CDN untuk Gambar Tutorial (Tanpa File Biner di PR)

Dokumen ini menjelaskan cara paling aman dan rapi supaya gambar tutorial tetap tampil, **tanpa commit file PNG ke `public/`**.

## Kenapa pakai CDN?

- PR jadi lebih mudah direview (text-only diff, minim pesan `binary file not supported`).
- Ukuran repo lebih kecil.
- Gambar tetap bisa dimuat dari URL publik.

---

## Opsi CDN yang dipakai saat ini (direkomendasikan)

Website ini sudah diset untuk memuat gambar dari **jsDelivr** yang mengambil file dari folder `tutorial_images/` di GitHub repo ini.

Contoh URL format:

```text
https://cdn.jsdelivr.net/gh/<owner>/<repo>@<branch-or-tag>/tutorial_images/<nama-file>.png
```

Contoh real:

```text
https://cdn.jsdelivr.net/gh/fatonyahmadfauzi/Pixiv-OAuth-Token@master/tutorial_images/step_1.png
```

---

## Langkah 1 — Siapkan file di folder sumber GitHub

Simpan gambar tutorial di root repo folder `tutorial_images/` (bukan `public/tutorial_images/`) dengan nama file konsisten:

1. `step_1.png`
2. `02-continue-login.png`
3. `03-open-console.png`
4. `04-copy-pixiv-url.png`
5. `step_5.png`
6. `result.png`

> Pastikan huruf besar/kecil sama persis karena URL CDN case-sensitive.

---

## Langkah 2 — Upload/push ke GitHub

Commit gambar ke branch yang dipakai CDN (saat ini `master`) lalu push.

```bash
git add tutorial_images/*.png
git commit -m "Add tutorial images for CDN"
git push origin master
```

---

## Langkah 3 — Pakai URL CDN di `public/index.html`

Di bagian tutorial, pakai `src` eksternal seperti ini:

```html
<img src="https://cdn.jsdelivr.net/gh/fatonyahmadfauzi/Pixiv-OAuth-Token@master/tutorial_images/step_1.png" ...>
```

Kalau ganti branch/tag, ubah bagian `@master`.

### Rekomendasi production (lebih stabil)

Jangan pin ke branch (`@master`), tapi pin ke tag/commit, misalnya:

```text
@v1.2.3
```
atau
```text
@<commit-sha>
```

Supaya konten tidak berubah mendadak.

---

## Langkah 4 — Verifikasi cepat

1. Buka langsung URL CDN di browser.
2. Pastikan status `200` dan gambar tampil.
3. Buka website, cek section Tutorial.
4. Cek DevTools Console/Network: tidak ada 404 untuk gambar tutorial.

---

## Langkah 5 — Jika gambar tidak update (cache CDN)

Kadang CDN masih cache versi lama.

Yang bisa dilakukan:

1. Hard refresh browser (`Ctrl+F5`).
2. Ganti URL versi (mis. dari `@master` ke `@commit-sha` terbaru).
3. Tambah query versioning sementara, misalnya `?v=20260302`.

Contoh:

```text
.../step_1.png?v=20260302
```

---

## Fallback lokal (opsional)

Kalau ingin kembali host lokal:

1. Taruh file PNG di `public/tutorial_images/` dengan nama yang sama.
2. Ubah `src` di `public/index.html` dari URL CDN menjadi:

```text
/tutorial_images/<nama-file>
```

Contoh:

```html
<img src="/tutorial_images/step_1.png" ...>
```

---

## Troubleshooting

### 1) 404 di CDN
- Cek nama file dan huruf besar/kecil.
- Cek file benar-benar ada di branch/tag/commit yang dirujuk.
- Coba buka URL raw GitHub untuk memastikan file ada.

### 2) Gambar keblokir kebijakan jaringan
- Beberapa network kantor/sekolah memblokir CDN tertentu.
- Solusi: pakai CDN lain (Cloudflare R2/S3/Cloudinary) atau host lokal.

### 3) Masih muncul error JS `classList` saat gambar gagal
- Pastikan handler `onerror` tidak akses `parentElement` setelah node di-replace tanpa null-check.

