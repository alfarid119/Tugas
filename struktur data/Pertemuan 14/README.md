# 🚗 Sistem Antrian FIFO Multi-Loket — Samsat STNK

Aplikasi manajemen antrian pelayanan perpanjangan STNK berbasis **FIFO (First In First Out)** dengan struktur data **Linked List**. Tersedia dalam dua mode: antarmuka web via **Streamlit** dan mode **Console/Terminal**.

---

## 📋 Fitur Utama

- **5 loket pelayanan independen** — setiap loket punya antrian, counter, dan riwayat sendiri
- **Struktur data Linked List** — operasi enqueue/dequeue O(1)
- **Text-to-Speech (TTS)** — pengumuman suara otomatis saat memanggil/mendaftarkan pelanggan
- **Validasi jam pelayanan** — sistem hanya aktif Senin–Jumat, 08:00–16:00 WIB
- **Estimasi waktu tunggu** — dihitung otomatis berdasarkan posisi antrian
- **Riwayat pelayanan** — tercatat lengkap per loket maupun gabungan semua loket
- **Dua mode tampilan** — Web UI (Streamlit) dan Console/Terminal

---

## 🏢 Konfigurasi Loket

| Loket | Kode Antrian | Jenis Layanan                  |
|-------|:------------:|-------------------------------|
| 1     | A001–A999    | Perpanjangan STNK Tahunan     |
| 2     | B001–B999    | Perpanjangan STNK 5 Tahunan   |
| 3     | C001–C999    | Balik Nama Kendaraan          |
| 4     | D001–D999    | Ganti STNK Hilang/Rusak       |
| 5     | E001–E999    | Mutasi Kendaraan              |

---

## 🗂️ Struktur Proyek

```
.
├── app.py              # Antarmuka web (Streamlit)
├── console_app.py      # Mode terminal/console
├── queue_system.py     # Inti logika antrian FIFO & multi-loket
├── tts_helper.py       # Modul Text-to-Speech (gTTS)
├── utils.py            # Fungsi utilitas (validasi, format, jam pelayanan)
└── README.md
```

---

## ⚙️ Instalasi

### Prasyarat

- Python 3.10 atau lebih baru

### 1. Clone / unduh repositori

```bash
git clone <url-repo>
cd <nama-folder>
```

### 2. Install dependensi

```bash
pip install streamlit gtts
```

Opsional untuk memutar audio di console:

```bash
pip install playsound
# atau
pip install pygame
```

---

## 🚀 Cara Menjalankan

### Mode Web (Streamlit)

```bash
streamlit run app.py
```

Buka browser di `http://localhost:8501`

### Mode Console / Terminal

```bash
python console_app.py
```

### Demo / Test Sistem Antrian

```bash
python queue_system.py
```

### Test Utilitas

```bash
python utils.py
```

### Test TTS

```bash
python tts_helper.py
```

---

## 🖥️ Tampilan Aplikasi

### Web UI (Streamlit)

- **Sidebar** — Form pendaftaran antrian baru beserta statistik ringkas (menunggu, aktif, selesai)
- **Kolom Tengah** — Panel kontrol per loket: tombol Panggil & Selesai, daftar tunggu real-time
- **Kolom Kanan** — Riwayat pelayanan per loket (tab) + info jam pelayanan + progress kapasitas harian
- **Audio otomatis** — Pengumuman diputar langsung di browser saat memanggil pelanggan

### Console / Terminal

```
Menu Utama:
  [1]  Daftar Antrian Baru
  [2]  Panggil Pelanggan (pilih loket)
  [3]  Selesaikan Pelayanan (pilih loket)
  [4]  Lihat Semua Antrian
  [5]  Riwayat per Jenis Layanan
  [6]  Statistik
  [0]  Keluar
```

---

## 🔧 Penjelasan Modul

### `queue_system.py`

Inti sistem antrian. Berisi tiga kelas utama:

- **`Node`** — Simpul linked list yang menyimpan data pelanggan
- **`AntrianFIFO`** — Implementasi antrian dengan operasi `enqueue`, `dequeue`, `peek`, dan `lihat_semua`
- **`SistemMultiLoket`** — Orkestrasi 5 loket secara independen, mengelola antrian, status pelayanan, counter nomor, dan riwayat

### `tts_helper.py`

Modul Text-to-Speech menggunakan **gTTS**. Menyediakan fungsi:

- `generate_audio_file()` — membuat file MP3 dari teks
- `speak_text()` — memutar audio (mendukung playsound, pygame, mpg123, ffplay)
- `buat_pesan_panggil()` — template pengumuman pemanggilan
- `buat_pesan_daftar()` — template konfirmasi pendaftaran
- `buat_pesan_selesai()` — template pengumuman selesai dilayani

### `utils.py`

Fungsi-fungsi pembantu:

- `cek_jam_pelayanan()` — validasi hari dan jam aktif
- `get_info_pelayanan()` — info status layanan lengkap
- `format_nomor_antrian()` — format nomor dengan prefix dan zero-padding
- `get_estimasi_waktu()` — hitung estimasi tunggu (default 5 menit/pelanggan)
- `validasi_nomor_polisi()` — validasi format plat nomor Indonesia
- `validasi_nomor_hp()` — validasi format nomor HP Indonesia
- `hitung_durasi_pelayanan()` — hitung durasi dari dua timestamp

---

## 📐 Kompleksitas Algoritma

| Operasi          | Kompleksitas |
|------------------|:------------:|
| Enqueue (masuk)  | O(1)         |
| Dequeue (keluar) | O(1)         |
| Peek (lihat)     | O(1)         |
| Lihat semua      | O(n)         |
| Ukuran antrian   | O(1)         |

---

## ⏰ Jam Pelayanan

| Hari              | Jam                  |
|-------------------|----------------------|
| Senin – Jumat     | 08:00 – 16:00 WIB   |
| Sabtu & Minggu    | Libur                |

Pendaftaran antrian baru hanya dapat dilakukan dalam jam pelayanan aktif.

---

## 🛠️ Teknologi

- **Python 3.10+**
- **Streamlit** — antarmuka web
- **gTTS (Google Text-to-Speech)** — pengumuman suara
- **Linked List** — struktur data antrian FIFO

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan edukasi dan demonstrasi implementasi struktur data antrian FIFO dalam konteks pelayanan publik.
