# Mini SIMRS Klinik

Aplikasi web sederhana untuk mengelola data pasien dan riwayat kunjungan klinik. Dibuat sebagai latihan dasar sistem informasi rumah sakit (SIMRS) dengan Python, Flask, dan MySQL.

## Fitur

- Menampilkan daftar pasien
- Menambah pasien baru lewat form
- Mencari pasien berdasarkan nama atau nomor rekam medis
- Mengubah dan menghapus data pasien (dengan konfirmasi sebelum hapus)
- Menampilkan riwayat kunjungan lengkap dengan nama pasien dan dokter (menggabungkan 3 tabel dengan `JOIN`)
- Penghapusan pasien yang masih punya data kunjungan ditolak oleh database (Foreign Key), lalu aplikasi menampilkan pesan yang jelas

## Teknologi

- Python 3
- Flask
- MySQL 8
- mysql-connector-python
- python-dotenv (menyimpan konfigurasi database di file `.env`)

## Struktur Database

Database `klinik` terdiri dari 3 tabel:

- `pasien` (id_pasien, nama, tanggal_lahir, no_bpjs, no_rekam_medis)
- `dokter` (id_dokter, nama_dokter, spesialisasi)
- `kunjungan` (id_kunjungan, id_pasien, id_dokter, tanggal_kunjungan, diagnosa, obat, dosis)

Tabel `kunjungan` terhubung ke `pasien` dan `dokter` lewat Foreign Key. Struktur lengkapnya ada di file `schema.sql`.

## Cara Menjalankan

1. Clone repo ini, lalu masuk ke foldernya.
2. Buat database dengan menjalankan isi file `schema.sql` di MySQL Workbench. File ini hanya berisi struktur tabel, tanpa data.
3. Salin file `.env.example` menjadi `.env`, lalu isi password MySQL kamu:
```
   copy .env.example .env
```
4. Pasang library yang dibutuhkan:
```
   pip install flask mysql-connector-python python-dotenv
```
5. Jalankan aplikasi:
```
   python app.py
```
6. Buka `http://127.0.0.1:5000` di browser.

Tabel masih kosong saat pertama dijalankan. Tambahkan pasien lewat form di halaman utama. Data kunjungan dan dokter saat ini ditambahkan lewat MySQL Workbench.

## Rencana Pengembangan

- Form tambah kunjungan (pilih pasien dan dokter dari dropdown)
- Login dengan 2 peran: staf pendaftaran dan staf medis
- Fitur backup database otomatis

## Catatan

Semua data pada project ini adalah data contoh (fiktif) untuk keperluan belajar.