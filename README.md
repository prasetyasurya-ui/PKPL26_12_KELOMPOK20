# TokoLaku Auth Module

Modul ini adalah bagian autentikasi untuk skenario E-Commerce Marketplace.
Fokus utama repo saat ini adalah secure authentication flow dan role pengguna sesuai kebutuhan tugas.

## Ringkasan Fitur Saat Ini

- Register, login, logout dengan Django auth.
- Mitigasi brute-force login menggunakan lockout per kombinasi username + IP.
- Session hardening menggunakan rotasi session key dan token sesi unik.
- Least privilege pada akun baru.
- Role e-commerce pada sisi auth:
    - Pembeli
    - Penjual
    - Kurir
- Dashboard auth sederhana yang menampilkan username dan role aktif.

## Struktur Penting

- App auth: folder authentication
- Project config: folder pkpl_project
- Template landing page: folder templates
- Database lokal default: db.sqlite3

## Setup Proyek

Jalankan dari root project.

```bat
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Endpoint Utama

- Landing page: http://127.0.0.1:8000/
- Register: http://127.0.0.1:8000/auth/register/
- Login: http://127.0.0.1:8000/auth/login/
- Dashboard auth: http://127.0.0.1:8000/auth/

## Akun Admin Lokal

Untuk kebutuhan pengujian admin:

```bash
python manage.py createsuperuser
```

## Menjalankan Test

```bash
python manage.py test authentication
```

## Catatan Secure Coding (Yang Sudah Diterapkan)

- Password tidak disimpan plaintext (menggunakan password hasher Django).
- Session fixation mitigation dengan rotasi session key setelah login.
- Token sesi acak tambahan disimpan di server-side session.
- Lockout sementara setelah gagal login berulang.
- Default privilege user baru dibatasi.

## Workflow Git yang Disarankan

1. Tarik update terbaru

```bash
git pull origin <main-branch>
```

2. Buat branch fitur

```bash
git checkout -b feat/<nama-fitur>
```

3. Commit kecil dan jelas

```bash
git add .
git commit -m "feat: tambah <nama-fitur>"
```

4. Push dan buat pull request

## Troubleshooting Cepat

- Jika migrasi gagal karena konflik model:
    - pastikan sudah pull terbaru
    - cek file migration terbaru
    - jalankan ulang migrate
- Jika modul tidak ditemukan:
    - pastikan virtual environment aktif
    - install ulang requirements
- Jika port 8000 dipakai proses lain:

```bash
python manage.py runserver 8001
```
