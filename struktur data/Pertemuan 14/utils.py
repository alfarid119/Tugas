"""
╔══════════════════════════════════════════════════════════════════╗
║              MODUL UTILITAS — Fungsi Pembantu                   ║
╚══════════════════════════════════════════════════════════════════╝
"""

from datetime import datetime, time


# ── Konfigurasi Jam & Hari Pelayanan ─────────────────────────────────────────
JAM_BUKA   = time(8, 0)    # 08:00 WIB
JAM_TUTUP  = time(16, 0)   # 16:00 WIB
HARI_AKTIF = {0, 1, 2, 3, 4}  # Senin=0 … Jumat=4 (Sabtu=5, Minggu=6 libur)

NAMA_HARI = {
    0: "Senin",
    1: "Selasa",
    2: "Rabu",
    3: "Kamis",
    4: "Jumat",
    5: "Sabtu",
    6: "Minggu",
}


def cek_jam_pelayanan() -> tuple[bool, str]:
    """
    Mengecek apakah saat ini dalam jam dan hari pelayanan.

    Returns:
        tuple[bool, str]:
            - bool  : True jika sedang dalam jam pelayanan
            - str   : Pesan status pelayanan
    """
    sekarang = datetime.now()
    jam_sekarang = sekarang.time()
    hari_sekarang = sekarang.weekday()   # 0=Senin … 6=Minggu

    if hari_sekarang not in HARI_AKTIF:
        nama = NAMA_HARI.get(hari_sekarang, "")
        return False, f"Hari {nama} — Pelayanan tutup (Senin–Jumat)"

    if jam_sekarang < JAM_BUKA:
        return False, f"Pelayanan belum dibuka (buka pukul 08:00 WIB)"

    if jam_sekarang >= JAM_TUTUP:
        return False, f"Pelayanan sudah ditutup (tutup pukul 16:00 WIB)"

    return True, "Pelayanan sedang berjalan"


def get_info_pelayanan() -> dict:
    """
    Mengembalikan informasi lengkap status pelayanan saat ini.

    Returns:
        dict dengan key:
            aktif (bool), jam_buka (str), jam_tutup (str),
            hari_ini (str), pesan (str), hari_aktif_list (str)
    """
    aktif, pesan = cek_jam_pelayanan()
    sekarang = datetime.now()
    return {
        "aktif": aktif,
        "jam_buka": "08:00",
        "jam_tutup": "16:00",
        "hari_ini": NAMA_HARI.get(sekarang.weekday(), ""),
        "tanggal": sekarang.strftime("%d %B %Y"),
        "pesan": pesan,
        "hari_aktif_list": "Senin – Jumat",
    }


def format_nomor_antrian(counter: int, prefix: str = "A") -> str:
    """
    Memformat nomor antrian dengan prefix dan padding nol.

    Args:
        counter (int): Nomor urut (1, 2, 3, ...).
        prefix (str): Huruf awalan nomor antrian.

    Returns:
        str: Nomor antrian terformat (misal: A001, A012, A100).
    """
    return f"{prefix}{counter:03d}"


def get_estimasi_waktu(posisi_dalam_antrian: int, menit_per_pelanggan: int = 5) -> int:
    """
    Menghitung estimasi waktu tunggu berdasarkan posisi dalam antrian.

    Args:
        posisi_dalam_antrian (int): Posisi ke-N dari depan antrian.
        menit_per_pelanggan (int): Rata-rata waktu pelayanan per pelanggan.

    Returns:
        int: Estimasi waktu tunggu dalam menit.
    """
    return posisi_dalam_antrian * menit_per_pelanggan


def format_waktu_sekarang() -> str:
    """Mengembalikan waktu saat ini dalam format HH:MM:SS."""
    return datetime.now().strftime("%H:%M:%S")


def format_tanggal_sekarang() -> str:
    """Mengembalikan tanggal saat ini dalam format DD/MM/YYYY."""
    return datetime.now().strftime("%d/%m/%Y")


def validasi_nomor_polisi(nomor: str) -> bool:
    """
    Validasi format nomor polisi kendaraan Indonesia.
    Format umum: [1-2 huruf] [1-4 angka] [1-3 huruf]
    """
    import re
    bersih = nomor.replace(" ", "").upper()
    pola = r'^[A-Z]{1,2}\d{1,4}[A-Z]{1,3}$'
    return bool(re.match(pola, bersih))


def validasi_nomor_hp(nomor: str) -> bool:
    """Validasi format nomor HP Indonesia."""
    if not nomor or nomor == "-":
        return True
    import re
    bersih = nomor.replace(" ", "").replace("-", "")
    pola = r'^(\+62|62|0)8[1-9][0-9]{6,10}$'
    return bool(re.match(pola, bersih))


def hitung_durasi_pelayanan(waktu_mulai: str, waktu_selesai: str) -> str:
    """Menghitung durasi pelayanan antara dua timestamp HH:MM:SS."""
    try:
        fmt = "%H:%M:%S"
        mulai = datetime.strptime(waktu_mulai, fmt)
        selesai = datetime.strptime(waktu_selesai, fmt)
        delta = (selesai - mulai).seconds
        menit = delta // 60
        detik = delta % 60
        return f"{menit} menit {detik} detik"
    except Exception:
        return "—"


def singkat_jenis_layanan(layanan: str, maks_karakter: int = 20) -> str:
    """Mempersingkat nama jenis layanan jika terlalu panjang."""
    if len(layanan) <= maks_karakter:
        return layanan
    return layanan[:maks_karakter - 3] + "..."


# ── Test ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("== Test Utilitas ==")
    print(format_nomor_antrian(1))
    print(format_nomor_antrian(42))
    print(get_estimasi_waktu(3))
    info = get_info_pelayanan()
    print(f"Status: {info['pesan']}")
    print(f"Aktif: {info['aktif']}")
    aktif, pesan = cek_jam_pelayanan()
    print(f"Cek jam: {aktif} — {pesan}")