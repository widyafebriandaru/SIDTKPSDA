# TKPSDA WS Seputih Sekampung — Monitoring Tindak Lanjut Rekomendasi

Backend CRUD (FastAPI + PostgreSQL + Docker) untuk data monitoring tindak lanjut
rekomendasi TKPSDA. Frontend belum dibuat — tahap ini fokus ke backend + database dulu.

## Struktur Project

```
tkpsda-app/
├── docker-compose.yml       # Orkestrasi: postgres, pgadmin, backend
├── .env                     # Variabel environment (JANGAN di-commit ke git)
├── .env.example             # Contoh/template .env
├── .gitignore
├── README.md
└── backend/
    ├── Dockerfile
    ├── requirements.txt
    ├── main.py               # Entry point FastAPI
    ├── seed.py                # Script isi data contoh
    ├── alembic.ini
    ├── alembic/
    │   ├── env.py
    │   ├── script.py.mako
    │   └── versions/
    │       └── 0001_initial.py   # Migration awal: buat semua tabel
    └── app/
        ├── config.py          # Baca env var (DATABASE_URL, CORS_ORIGINS)
        ├── database.py        # Setup SQLAlchemy engine/session
        ├── models/            # Definisi tabel (SQLAlchemy ORM)
        │   ├── instansi.py
        │   ├── tusi.py
        │   ├── rekomendasi.py
        │   ├── tindak_lanjut.py
        │   └── program_kerja.py
        ├── schemas/            # Skema request/response (Pydantic)
        │   └── ... (satu file per resource)
        ├── crud/               # Logika query ke database
        │   ├── base.py         # CRUD generik (dipakai semua resource)
        │   └── ... (satu file per resource)
        └── routers/            # Endpoint HTTP (FastAPI)
            └── ... (satu file per resource)
```

## Skema Database (ringkas)

- **instansi** — daftar dinas/lembaga (BBWS, Dinas PSDA, BMKG, dst)
- **tusi** — daftar Tugas dan Fungsi (SIH3, RAAT, ISU STRATEGIS, dst)
- **rekomendasi** — data induk rekomendasi hasil sidang (judul sidang, nomor rekomendasi, isi, dll)
- **tindak_lanjut** — status tindak lanjut tiap rekomendasi PER instansi (satu rekomendasi
  bisa ditindaklanjuti banyak instansi, masing-masing dengan status sendiri)
- **program_kerja** — rencana & progres kerja tahunan (dari sheet "Program Kerja dan Progres SS")

Sheet-sheet rekap di Excel (Rekap Per Instansi, Rekap Per Tusi, dll) **sengaja tidak dibuat
sebagai tabel** — nanti itu akan jadi VIEW / query SQL yang dihitung otomatis dari data di atas,
supaya angkanya selalu konsisten dan tidak perlu di-update manual.

## Cara Menjalankan

### 1. Siapkan file environment

```bash
cp .env.example .env
```

Buka `.env`, ganti `POSTGRES_PASSWORD` dan `PGADMIN_DEFAULT_PASSWORD` dengan password sendiri
(terutama kalau nanti di-deploy, jangan pakai nilai default).

### 2. Jalankan semua service

```bash
docker compose up -d --build
```

Ini akan:
- Menyalakan PostgreSQL di port `5432`
- Menyalakan pgAdmin di `http://localhost:5050`
- Build & menyalakan backend FastAPI di `http://localhost:8010`
- **Otomatis menjalankan migration** (`alembic upgrade head`) sebelum server backend start
  — jadi begitu container backend hidup, semua tabel sudah otomatis terbentuk.

Cek log kalau mau memastikan migration jalan lancar:
```bash
docker compose logs -f backend
```

### 3. Cek API sudah jalan

Buka `http://localhost:8010/docs` — dokumentasi interaktif (Swagger UI) otomatis dari FastAPI.
Semua endpoint CRUD bisa langsung dicoba dari sini tanpa perlu Postman.

### 4. Isi data contoh (opsional, untuk uji coba)

```bash
docker compose exec backend python seed.py
```

Ini akan mengisi beberapa baris contoh (3 instansi, 3 tusi, 3 rekomendasi, 3 tindak lanjut,
1 program kerja) supaya kamu bisa langsung lihat & coba endpoint GET/PUT/DELETE-nya.

### 5. Akses pgAdmin (opsional, untuk lihat isi database via GUI)

Buka `http://localhost:5050`, login pakai `PGADMIN_DEFAULT_EMAIL` / `PGADMIN_DEFAULT_PASSWORD`
dari `.env`. Lalu tambahkan server baru dengan koneksi:
- Host: `postgres` (nama service di docker-compose, BUKAN `localhost`)
- Port: `5432`
- Username/Password: sesuai `POSTGRES_USER` / `POSTGRES_PASSWORD` di `.env`

## Endpoint yang tersedia

Semua resource (`instansi`, `tusi`, `rekomendasi`, `tindak-lanjut`, `program-kerja`) punya
pola endpoint yang sama:

| Method | Path | Keterangan |
|---|---|---|
| GET | `/api/{resource}` | List semua data (support `?skip=&limit=`) |
| GET | `/api/{resource}/{id}` | Detail satu data |
| POST | `/api/{resource}` | Tambah data baru |
| PUT | `/api/{resource}/{id}` | Update data |
| DELETE | `/api/{resource}/{id}` | Hapus data |

Contoh filter tambahan:
- `GET /api/rekomendasi?tahun=2025&tusi_id=1`
- `GET /api/tindak-lanjut?status_pelaksanaan=terlaksana&instansi_id=1`

## Perintah Alembic yang berguna

```bash
# Bikin migration baru setelah ubah model (misal tambah kolom)
docker compose exec backend alembic revision --autogenerate -m "deskripsi perubahan"

# Jalankan migration terbaru
docker compose exec backend alembic upgrade head

# Rollback satu migration
docker compose exec backend alembic downgrade -1
```

## Menghentikan / reset

```bash
# Stop semua service (data tetap tersimpan)
docker compose down

# Stop + hapus semua data (reset total dari nol)
docker compose down -v
```

## Rencana selanjutnya

- [ ] Frontend (Vite + React/Vue) untuk tampilan CRUD
- [ ] Import data asli dari Excel ke database (setelah struktur difinalkan)
- [ ] VIEW/endpoint rekap (per instansi, per tusi, per tahun) — pengganti sheet rekap Excel
- [ ] Fitur AI chat (Text-to-SQL) di atas database ini
