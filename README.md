# Deskripsi Aplikasi

## Skenario
Aplikasi ini merupakan modul autentikasi pada inisiasi project backend Django.
Fokus implementasi adalah alur register-login-logout dengan keamanan sesi yang memadai, pembatasan percobaan login, dan kontrol hak akses pengguna baru.

## Fitur
- Inisiasi project Django dengan struktur app authentication.
- Database SQLite sebagai penyimpanan data lokal.
- Register pengguna menggunakan `UserCreationForm` Django.
- Login dan Logout menggunakan sistem autentikasi bawaan Django.
- Lockout login setelah maksimal 5 kali kegagalan dari kombinasi username dan alamat IP.
- Manajemen sesi aman dengan rotasi session key dan token sesi unik di server.
- Penerapan least privilege: user baru otomatis non-staff, non-superuser, dan masuk grup default `user`.

## Stack
- Python 3.x
- Django 6.x
- SQLite

# Mitigasi Broken Authentication

## Ringkasan CWE Terkait
- CWE-287: Improper Authentication
- CWE-307: Improper Restriction of Excessive Authentication Attempts
- CWE-384: Session Fixation
- CWE-522: Insufficiently Protected Credentials

## Implementasi Mitigasi
- Password disimpan dengan password hasher default Django (`PBKDF2PasswordHasher`) sehingga tidak ada penyimpanan plaintext.
- Django juga mendukung hasher tambahan seperti bcrypt melalui konfigurasi `PASSWORD_HASHERS`.
- Setelah login berhasil, session key dirotasi melalui `request.session.cycle_key()`.
- Token sesi unik tambahan disimpan per sesi (`request.session['session_token'] = uuid.uuid4().hex`).
- Rate limiting/lockout: jika gagal login 5 kali, akun sementara dikunci selama 15 menit.
- Least privilege: akun register baru dipaksa `is_staff=False` dan `is_superuser=False`.

## Snippet Vulnerable vs Secure

### Contoh Vulnerable 1 (password plaintext)
```python
# Buruk: membandingkan password plaintext
if request.POST['password'] == user.password:
    request.session['user_id'] = user.id
```

### Contoh Secure 1 (hash verification + session hardening)
```python
form = AuthenticationForm(request, data=request.POST)
if form.is_valid():
    user = form.get_user()
    login(request, user)                   # verifikasi password hash Django
    request.session.cycle_key()            # cegah session fixation
    request.session['session_token'] = uuid.uuid4().hex
```

### Contoh Vulnerable 2 (tanpa lockout brute-force)
```python
# Buruk: tidak ada pembatasan percobaan login
if not form.is_valid():
    return render(request, 'login.html', {'form': form})
```

### Contoh Secure 2 (lockout 5x gagal)
```python
if attempt.failed_attempts >= 5:
    attempt.locked_until = timezone.now() + timedelta(minutes=15)
    attempt.failed_attempts = 0
    attempt.save(update_fields=['failed_attempts', 'locked_until', 'last_attempt_at'])
```

# Cara Menjalankan

```bash
python manage.py migrate
python manage.py runserver
```

Akses:
- Register: `/auth/register/`
- Login: `/auth/login/`
- Home (setelah login): `/auth/`
