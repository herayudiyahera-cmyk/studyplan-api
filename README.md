
# StudyPlan API

Backend REST API untuk mengelola target dan progres belajar mahasiswa menggunakan Python dan FastAPI.

## Fitur
- Menambahkan target belajar.
- Melihat seluruh target dan detail target.
- Mengubah informasi target.
- Mengubah status belajar.
- Menghapus target.
- Validasi deadline dan input.

## Teknologi
- Python
- FastAPI
- Uvicorn
- Pytest
- HTTPX

## Instalasi

```bash
python -m venv .venv
```

Aktifkan virtual environment sesuai sistem operasi, lalu jalankan:

```bash
python -m pip install -r requirements.txt
```

## Menjalankan API

```bash
python -m uvicorn app.main:app --reload
```

Dokumentasi API tersedia di:
http://127.0.0.1:8000/docs

## Menjalankan Pengujian

```bash
python -m pytest -v
```

## Struktur Arsitektur

- `models`: representasi data.
- `schemas`: validasi request dan response.
- `repositories`: abstraksi dan implementasi penyimpanan.
- `services`: logika bisnis.
- `routers`: endpoint REST API.
- `tests`: pengujian service dan API.

## Penyimpanan Data

Versi saat ini menggunakan penyimpanan di memori.
Data akan hilang ketika server dimulai ulang.
