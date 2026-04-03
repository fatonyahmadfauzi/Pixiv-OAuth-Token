# log perubahan

All notable changes to the "Pixiv OAuth Token" toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🔜 Coming Soon

- **Mobile Web Support** — The web app currently only supports desktop browsers. Upcoming update will bring full responsive mobile support, allowing users to generate Pixiv OAuth tokens directly from mobile devices without needing the desktop app.


---

## [1.0.5] - 2026-04-03

### ✨ Ditambahkan

- **Permulaan GUI Sadar Internet**
Sebelum meluncurkan jendela GUI utama, layar splash `NetLoadingScreen` yang cerdas sekarang melakukan pemeriksaan konektivitas internet sebelum penerbangan. Jika tidak ada koneksi yang ditemukan, maka koneksi akan dicoba lagi dengan aman di latar belakang hingga tersambung. Selain itu, monitor runtime yang aktif akan menampilkan peringatan yang kembali ke layar pemuatan jika koneksi terputus di tengah jalan selama penggunaan.
- **Modal Dokumentasi GUI Asli**
Mengganti pengalihan browser eksternal untuk dokumentasi penting. **Changelog**, **Syarat & Ketentuan**, dan **Kebijakan Privasi** kini ditampilkan di dalam jendela dialog `tkinter` yang asli, dinamis, dan bersih (diambil secara asinkron langsung dari repo GitHub).
- **Lokalisasi Terminal Komprehensif**
Antarmuka GitHub CLI yang interaktif (Navigasi masalah) dan semua tata letak Hukum/Dukungan berbasis terminal kini dilokalkan secara autentik dalam 11 bahasa yang didukung.

### ✨ Berubah

- **Didesain ulang CLI Estetika**
Menghapus batas kotak dekoratif lama untuk tampilan terminal yang jauh lebih bersih, modern, dan rata kiri.
- **Penandatanganan Kode Digital Otomatis**
Meningkatkan pipa `sign_auto.bat` secara signifikan. Skrip sekarang secara otomatis menemukan `signtool.exe` jauh di dalam SDK Windows, dengan mudah menerapkan sertifikat yang ditandatangani sendiri di semua build yang dihasilkan secara bersamaan (termasuk pengaturan Penginstal dan alias Unduh `_latest`) untuk menyembunyikan tanda dasar 'Penerbit Tidak Dikenal' SmartScreen.

### 🐞 Diperbaiki

- **Bug Properti Pemasang**
Memperbaiki anomali saat Penginstal `Setup.exe` menampilkan `0.0.0.0` di Properti Windows. Pembuat sekarang memasukkan dengan benar header PE `VersionInfoVersion` yang ketat selama kompilasi untuk mencerminkan nomor rilis yang sama persis (e.g., 1.0.5.0) segera setelah rendering.

---

## [1.0.4] - 2026-03-29

### 🐞 Diperbaiki

- **Portable CLI/GUI — Pengembalian versi setelah pembaruan**: `VERSION_FILE` dan `CONFIG_FILE` diselesaikan menggunakan `Path(__file__)`, yang dalam mode beku (PyInstaller onefile) menunjuk ke direktori `_MEIPASS` sementara — direktori yang dimusnahkan saat aplikasi ditutup. Kedua file sekarang diselesaikan menggunakan `_app_dir()` / `app_dir()` yang dengan benar mengembalikan folder yang berisi `.exe` sebenarnya, memastikan identitas versi tetap ada saat restart.
- **CLI — Perbarui timpa temp `.py` alih-alih exe**: Saat dijalankan sebagai executable yang dibekukan, `_self_update()` menimpa `.py` yang diekstraksi di dalam direktori sementara alih-alih mengganti `.exe` yang sebenarnya. Fungsi tersebut sekarang mendeteksi `is_frozen` dan mengunduh executable baru secara langsung, menggantikannya melalui skrip pembaru `.bat` (mekanisme yang sama seperti GUI).

### ✨ Ditambahkan

- **Pembaruan otomatis yang sadar arsitektur (CLI + GUI)**: Alur pembaruan portabel dan pengaturan kini mendeteksi arsitektur executable yang sedang berjalan (`x64`, `x86`, `ARM64`, atau generik) dari nama filenya dan mengunduh varian yang sama persis dari folder `downloads/`, sehingga mencegah ketidakcocokan arsitektur yang tidak disengaja selama pembaruan.
- **alur pembaruan penginstal pengaturan CLI**: CLI sekarang mencerminkan perilaku GUI untuk instalasi pengaturan — saat dijalankan dari `Program Files`, ia mengunduh penginstal pengaturan `.exe` terbaru dan menjalankannya secara diam-diam (`/VERYSILENT /NORESTART`) alih-alih mencoba pertukaran biner di tempat.

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
Skrip pembuat InnoSetup sekarang menghasilkan penginstal terpadu yang meminta pengguna akhir untuk menginstal CLI mandiri atau GUI grafis.

### 🐞 Diperbaiki

- **Resolusi Jalur Pembuatan Penginstal**
Memperbaiki masalah ketidakcocokan jalur kritis di `make_installer_iss_dual.py` di mana `iscc` gagal menemukan `app\pixiv_oauth.ico` dengan membuat file build langsung dalam direktori `scripts\` yang dikonfigurasi.

## [1.0.0] - 2026-03-21

### ✨ Ditambahkan

- Distribusi awal yang dapat dieksekusi mandiri (`.exe`) dikompilasi untuk mode GUI dan CLI.
- Integrasi tanpa server awal yang dioptimalkan disinkronkan ke Vercel dengan deteksi bahasa otomatis.
- Pass kebingungan JavaScript ekstrem ditambahkan untuk titik akhir web.
