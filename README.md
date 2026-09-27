# Faceswap App — Tahap 1

Tahap ini berisi: project setup, model dasar, autentikasi, verifikasi OTP via email,
dan halaman Syarat & Ketentuan (ToS).

**Belum termasuk di tahap ini (sengaja):** endpoint generate/face-swap. Ini akan
ditambahkan di Tahap 2, bersamaan dengan pemeriksaan NSFW yang wajib aktif sejak
awal endpoint itu dibuat.

## Menjalankan lokal (kalau nanti punya akses ke komputer/Colab/Cloud IDE)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env: isi SECRET_KEY, DATABASE_URL, kredensial email, dll

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Buka `http://127.0.0.1:8000/accounts/register/` untuk coba alur daftar.
Buka `http://127.0.0.1:8000/admin/` untuk tambah versi ToS pertama
(model `TosVersion`, set `is_active=True`) — wajib diisi sebelum user bisa
menyetujui ToS saat daftar.

## Deploy tanpa laptop (Railway/Render, lewat browser HP)

1. Upload seluruh folder ini ke repository GitHub (lewat web GitHub, drag & drop file).
2. Buat akun di [Railway](https://railway.app) atau [Render](https://render.com) lewat browser.
3. Pilih "Deploy from GitHub repo", hubungkan ke repo yang tadi dibuat.
4. Di dashboard hosting, isi environment variables sesuai `.env.example`
   (`SECRET_KEY`, `DATABASE_URL` — biasanya disediakan otomatis kalau kamu
   tambah addon PostgreSQL di Railway/Render, `EMAIL_HOST`, dll).
5. Railway/Render otomatis mendeteksi `Procfile` dan menjalankan migrasi + server.
6. Setelah deploy sukses, buat superuser lewat fitur "Shell"/"Console" yang
   disediakan dashboard Railway/Render (berbasis web, tidak perlu laptop):
   ```
   python manage.py createsuperuser
   ```
7. Login ke `/admin/` dari domain yang diberikan Railway/Render, tambahkan
   versi ToS pertama.

## Struktur project

```
config/       -> settings, root urls
accounts/     -> User custom, OTP email, register/login/verify
core/         -> ToS, halaman beranda (placeholder Tahap 1)
templates/    -> base.html
```

## Tahap berikutnya (Tahap 2)

- App `moderation`: validator wajib (jumlah wajah, NSFW, ukuran file) — menyatu
  langsung di pipeline generate, bukan modul opsional yang bisa dimatikan lewat toggle.
- App `generate`: model `GenerateHistory`, endpoint upload source/target, Celery task.
- App `reports`: model `Report`, fitur lapor dari user.
- Dashboard admin: statistik & filter riwayat generate.
