"""
╔══════════════════════════════════════════════════════════════════════╗
║         BACKEND — Sistem Antrian STNK Samsat                       ║
║         FastAPI + Logika FIFO Multi-Loket + TTS (gTTS)             ║
╚══════════════════════════════════════════════════════════════════════╝

Jalankan:
    pip install fastapi uvicorn gtts
    python -m uvicorn backend:app --reload --port 8000
"""

# ╔══════════════════════════════════════════════════════════════════════╗
# ║                     BAGIAN 1 — ALFA                                ║
# ║  Meliputi: Import library, konfigurasi aplikasi, konfigurasi       ║
# ║  loket & layanan, konstanta jam operasional, serta struktur        ║
# ║  data antrian (Node, AntrianFIFO) sebagai inti logika FIFO.        ║
# ╚══════════════════════════════════════════════════════════════════════╝

import os
import re
import tempfile
from datetime import datetime, time
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="Antrian STNK Samsat", version="3.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ─── Konfigurasi (sama persis dengan queue_system.py & utils.py asli) ─────────

LOKET_MAP = {
    "Perpanjangan STNK Tahunan":   1,
    "Perpanjangan STNK 5 Tahunan": 2,
    "Balik Nama Kendaraan":        3,
    "Ganti STNK Hilang/Rusak":     4,
    "Mutasi Kendaraan":            5,
}
PREFIX_MAP     = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E"}
DAFTAR_LAYANAN = list(LOKET_MAP.keys())
NAMA_LOKET     = {i: k for k, i in LOKET_MAP.items()}

JAM_BUKA   = time(8, 0)
JAM_TUTUP  = time(16, 0)
HARI_AKTIF = {0, 1, 2, 3, 4}
NAMA_HARI  = {0:"Senin",1:"Selasa",2:"Rabu",3:"Kamis",4:"Jumat",5:"Sabtu",6:"Minggu"}

AUDIO_DIR = tempfile.gettempdir()

# ─── Struktur Data FIFO (sama persis dengan queue_system.py asli) ─────────────

class Node:
    def __init__(self, data: dict):
        self.data = data
        self.next: Optional["Node"] = None


class AntrianFIFO:
    def __init__(self):
        self._depan: Optional[Node] = None
        self._belakang: Optional[Node] = None
        self._jumlah = 0

    def enqueue(self, data: dict):
        node = Node(data)
        if self._depan is None:
            self._depan = self._belakang = node
        else:
            self._belakang.next = node
            self._belakang = node
        self._jumlah += 1

    def dequeue(self) -> Optional[dict]:
        if self._depan is None:
            return None
        data = self._depan.data
        self._depan = self._depan.next
        if self._depan is None:
            self._belakang = None
        self._jumlah -= 1
        return data

    def peek(self) -> Optional[dict]:
        return self._depan.data if self._depan else None

    def lihat_semua(self) -> list:
        hasil, node = [], self._depan
        while node:
            hasil.append(node.data)
            node = node.next
        return hasil

    def kosong(self) -> bool:
        return self._jumlah == 0

    def ukuran(self) -> int:
        return self._jumlah

    def clear(self):
        self._depan = self._belakang = None
        self._jumlah = 0

# ╔══════════════════════════════════════════════════════════════════════╗
# ║                     BAGIAN 2 — PASYA                                ║
# ║  Meliputi: Kelas SistemMultiLoket (manajemen 5 loket sekaligus),    ║
# ║  singleton sistem, serta semua fungsi helper/utilitas seperti       ║
# ║  pengecekan jam, estimasi waktu, dan pembuatan pesan TTS audio.     ║
# ╚══════════════════════════════════════════════════════════════════════╝

class SistemMultiLoket:
    def __init__(self):
        self.antrian         = {l: AntrianFIFO() for l in range(1, 6)}
        self.sedang_dilayani = {l: None for l in range(1, 6)}
        self.counter         = {l: 1 for l in range(1, 6)}
        self.riwayat         = {l: [] for l in range(1, 6)}

    def buat_nomor(self, loket: int) -> str:
        nomor = f"{PREFIX_MAP[loket]}{self.counter[loket]:03d}"
        self.counter[loket] += 1
        return nomor

    def daftar(self, data: dict) -> str:
        loket = LOKET_MAP.get(data.get("jenis_layanan", "Perpanjangan STNK Tahunan"), 1)
        nomor = self.buat_nomor(loket)
        data.update({"nomor": nomor, "loket": loket})
        self.antrian[loket].enqueue(data)
        return nomor

    def panggil(self, loket: int) -> Optional[dict]:
        if self.sedang_dilayani[loket] or self.antrian[loket].kosong():
            return None
        pelanggan = self.antrian[loket].dequeue()
        self.sedang_dilayani[loket] = pelanggan
        return pelanggan

    def selesai(self, loket: int) -> Optional[dict]:
        if not self.sedang_dilayani[loket]:
            return None
        data = self.sedang_dilayani[loket]
        data["waktu_selesai"] = datetime.now().strftime("%H:%M:%S")
        self.riwayat[loket].append(data)
        self.sedang_dilayani[loket] = None
        return data

    def reset(self):
        for l in range(1, 6):
            self.antrian[l].clear()
            self.sedang_dilayani[l] = None
            self.counter[l] = 1
            self.riwayat[l] = []

    def total_menunggu(self): return sum(self.antrian[l].ukuran() for l in range(1, 6))
    def total_selesai(self):  return sum(len(self.riwayat[l]) for l in range(1, 6))
    def total_aktif(self):    return sum(1 for l in range(1, 6) if self.sedang_dilayani[l])

    def semua_riwayat(self):
        hasil = []
        for l in range(1, 6):
            hasil.extend(self.riwayat[l])
        hasil.sort(key=lambda x: x.get("waktu_selesai", ""), reverse=True)
        return hasil


# ─── Singleton ────────────────────────────────────────────────────────────────
sistem = SistemMultiLoket()

# ─── Helpers (sama persis dengan utils.py & tts_helper.py asli) ───────────────

def cek_jam_pelayanan() -> tuple:
    return True, "Pelayanan sedang berjalan"

def get_info_pelayanan() -> dict:
    aktif, pesan = cek_jam_pelayanan()
    now = datetime.now()
    return {
        "aktif": aktif,
        "jam_buka": "08:00",
        "jam_tutup": "16:00",
        "hari_ini": NAMA_HARI.get(now.weekday(), ""),
        "tanggal": now.strftime("%d %B %Y"),
        "pesan": pesan,
        "hari_aktif_list": "Senin – Jumat",
    }

def get_estimasi_waktu(posisi: int, menit_per_pelanggan: int = 5) -> int:
    return posisi * menit_per_pelanggan

def buat_pesan_panggil(nomor, nama, loket):
    return (f"Perhatian. Nomor antrian {nomor}, atas nama {nama}, "
            f"dimohon segera menuju loket {loket}. Terima kasih.")

def buat_pesan_daftar(nomor, nama, estimasi_menit, loket):
    return (f"Selamat datang, {nama}. Nomor antrian Anda adalah {nomor}, "
            f"untuk loket {loket}. Estimasi waktu tunggu sekitar {estimasi_menit} menit. "
            f"Mohon menunggu di ruang tunggu yang telah disediakan.")

def buat_pesan_selesai(nama, loket):
    return (f"Pelayanan atas nama {nama} di loket {loket} telah selesai. "
            f"Terima kasih telah menggunakan layanan Samsat. Semoga harimu menyenangkan.")

def generate_audio_file(teks: str, nama_file: str) -> Optional[str]:
    try:
        from gtts import gTTS
        import time as _time
        nama_bersih = "".join(c for c in nama_file if c.isalnum() or c in "_-")
        path = os.path.join(AUDIO_DIR, f"{nama_bersih}.mp3")
        gTTS(text=teks, lang="id", slow=False).save(path)
        _time.sleep(0.5)
        return path
    except Exception as e:
        print(f"[TTS] Gagal: {e}")
        return None

# ─── Pydantic Models ──────────────────────────────────────────────────────────

class DaftarRequest(BaseModel):
    nama: str
    no_polisi: str
    jenis_layanan: str
    no_hp: str = "-"

# ╔══════════════════════════════════════════════════════════════════════╗
# ║                     BAGIAN 3 — LEVI                                ║
# ║  Meliputi: Semua endpoint API FastAPI — GET /info, GET /state,     ║
# ║  POST /daftar, POST /panggil, POST /selesai, POST /reset,          ║
# ║  GET /audio, dan GET /layanan. Inilah antarmuka utama yang         ║
# ║  diakses oleh frontend untuk menjalankan sistem antrian.           ║
# ╚══════════════════════════════════════════════════════════════════════╝

@app.get("/info")
def get_info():
    """Info status & jam pelayanan (sama dengan get_info_pelayanan)."""
    info = get_info_pelayanan()
    now  = datetime.now()
    info["jam"]     = now.strftime("%H:%M")
    info["tanggal"] = now.strftime("%d %B %Y")
    info["hari_ini"] = NAMA_HARI.get(now.weekday(), "")
    return info

@app.get("/state")
def get_state():
    """State lengkap semua loket + antrian + statistik."""
    aktif, pesan = cek_jam_pelayanan()
    loket_data = {}
    for l in range(1, 6):
        loket_data[l] = {
            "sedang_dilayani": sistem.sedang_dilayani[l],
            "antrian":         sistem.antrian[l].lihat_semua(),
            "jumlah_antrian":  sistem.antrian[l].ukuran(),
            "berikutnya":      sistem.antrian[l].peek(),
            "riwayat":         sistem.riwayat[l],
        }
    return {
        "aktif":   aktif,
        "pesan":   pesan,
        "loket":   loket_data,
        "statistik": {
            "menunggu": sistem.total_menunggu(),
            "aktif":    sistem.total_aktif(),
            "selesai":  sistem.total_selesai(),
        },
        "semua_riwayat": sistem.semua_riwayat(),
        "timestamp": datetime.now().strftime("%H:%M:%S"),
    }

@app.post("/daftar")
def daftar(req: DaftarRequest):
    aktif, pesan = cek_jam_pelayanan()
    if not aktif:
        raise HTTPException(400, pesan)
    if not req.nama.strip():
        raise HTTPException(400, "Nama tidak boleh kosong")
    if not req.no_polisi.strip():
        raise HTTPException(400, "Nomor polisi tidak boleh kosong")
    if req.jenis_layanan not in LOKET_MAP:
        raise HTTPException(400, "Jenis layanan tidak valid")

    now = datetime.now()
    data = {
        "nama":          req.nama.strip().title(),
        "no_polisi":     req.no_polisi.strip().upper(),
        "jenis_layanan": req.jenis_layanan,
        "no_hp":         req.no_hp.strip() or "-",
        "waktu_daftar":  now.strftime("%H:%M:%S"),
        "tanggal":       now.strftime("%d/%m/%Y"),
    }
    nomor    = sistem.daftar(data)
    loket    = LOKET_MAP[req.jenis_layanan]
    estimasi = get_estimasi_waktu(sistem.antrian[loket].ukuran())

    audio_key = None
    teks_tts  = buat_pesan_daftar(nomor, data["nama"], estimasi, loket)
    path      = generate_audio_file(teks_tts, f"daftar_{nomor}")
    if path:
        audio_key = f"daftar_{nomor}"

    return {
        "nomor":    nomor,
        "loket":    loket,
        "estimasi": estimasi,
        "audio":    audio_key,
        "pesan":    f"Berhasil! Nomor antrian: {nomor} — Loket {loket}",
    }

@app.post("/panggil/{loket}")
def panggil(loket: int):
    if loket not in range(1, 6):
        raise HTTPException(400, "Loket tidak valid")
    pelanggan = sistem.panggil(loket)
    if not pelanggan:
        raise HTTPException(400, "Tidak dapat memanggil: loket sedang aktif atau antrian kosong")

    audio_key = None
    teks_tts  = buat_pesan_panggil(pelanggan["nomor"], pelanggan["nama"], loket)
    path      = generate_audio_file(teks_tts, f"panggil_{pelanggan['nomor']}")
    if path:
        audio_key = f"panggil_{pelanggan['nomor']}"

    return {"pelanggan": pelanggan, "audio": audio_key}

@app.post("/selesai/{loket}")
def selesai(loket: int):
    if loket not in range(1, 6):
        raise HTTPException(400, "Loket tidak valid")
    hasil = sistem.selesai(loket)
    if not hasil:
        raise HTTPException(400, "Tidak ada pelanggan yang sedang dilayani")

    audio_key = None
    teks_tts  = buat_pesan_selesai(hasil["nama"], loket)
    path      = generate_audio_file(teks_tts, f"selesai_{hasil['nomor']}")
    if path:
        audio_key = f"selesai_{hasil['nomor']}"

    return {"hasil": hasil, "audio": audio_key}

@app.post("/reset")
def reset():
    sistem.reset()
    return {"pesan": "Sistem berhasil direset"}

@app.get("/audio/{nama_file}")
def get_audio(nama_file: str):
    nama_bersih = "".join(c for c in nama_file if c.isalnum() or c in "_-")
    path = os.path.join(AUDIO_DIR, f"{nama_bersih}.mp3")
    if not os.path.exists(path):
        raise HTTPException(404, "File audio tidak ditemukan")
    return FileResponse(path, media_type="audio/mpeg")

@app.get("/layanan")
def get_layanan():
    return {"layanan": DAFTAR_LAYANAN, "loket_map": LOKET_MAP, "prefix_map": PREFIX_MAP}
