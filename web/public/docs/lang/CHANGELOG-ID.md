# log perubahan

All notable changes to the "Pixiv OAuth Token" toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


---
## [1.0.3] - 2026-03-26 
### ✨ Berubah
- Mengganti label build lokal default dari `REL-LOCAL` menjadi `BUILD-UNKNOWN` di seluruh runtime/versi perkakas dan manifes yang dihasilkan.
- GUI kini menyertakan tindakan menu atas **Changelog** dan dropdown **Version** dengan entri pemeriksaan versi eksplisit.
- Menambahkan pemeriksaan versi startup otomatis di GUI dengan tindakan popup pembaruan (**Perbarui** / **Nanti**), ditambah penanganan aliran pembaruan untuk pengaturan beku/distribusi portabel.
- Memperbarui pembuatan kode build ke gaya unix `REL-U<unix_ms>` pada versi bump (`patch/minor/major`).

## [1.0.2] - 2026-03-23 
### ✨ Ditambahkan
- **Konsol Debug (GUI)**
Tombol `⚙ Debug` khusus di sudut kanan atas header GUI membuka konsol terminal bertema gelap yang mencatat setiap peristiwa aplikasi secara real-time. Peristiwa yang ditangkap meliputi: permulaan aplikasi, perubahan bahasa, semua klik tombol (Buka Login, Token Pertukaran, Token Penyegaran, Salin token akses/penyegaran, Tutorial), status permintaan HTTP (pengiriman/berhasil/gagal), langkah alur PKCE, operasi papan klip, penulisan konfigurasi, dan peringatan. Semua pesan debug sepenuhnya dilokalkan dalam 11 bahasa yang didukung. Konsol ini mendukung streaming langsung pesan baru saat terbuka, pra-pengisian log historis dari awal sesi, tombol **Salin Semua**, dan tombol **Hapus**.

## [1.0.1] - 2026-03-22
### ✨ Ditambahkan
- **Pembersih README Cerdas untuk Rilis**
Secara otomatis menghapus bagian bahasa pelokalan dari file `` saat mengkompilasi `.zip` yang dapat didistribusikan, menggantikan tautan internal dengan tautan GitHub absolut.
- **Dukungan Pemasang Ganda Terpadu**
Skrip pembuat InnoSetup sekarang menghasilkan penginstal terpadu yang meminta pengguna akhir untuk menginstal CLI mandiri atau GUI grafis secara opsional.

### 🐞 Diperbaiki
- **Resolusi Jalur Pembuatan Penginstal**
Memperbaiki masalah ketidakcocokan jalur kritis di `make_installer_iss_dual.py` di mana `iscc` gagal menemukan `app\pixiv_oauth.ico` dengan membuat file build langsung dalam direktori `scripts\` yang dikonfigurasi.

## [1.0.0] - 2026-03-21
### ✨ Ditambahkan
- Distribusi awal yang dapat dieksekusi mandiri (`.exe`) dikompilasi untuk mode GUI dan CLI.
- Integrasi tanpa server awal yang dioptimalkan disinkronkan ke Vercel dengan deteksi bahasa otomatis.
- Pass kebingungan JavaScript ekstrem ditambahkan untuk titik akhir web.
