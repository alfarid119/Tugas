"""
╔══════════════════════════════════════════════════════════════════════╗
║         IMPLEMENTASI ANTRIAN FIFO (FIRST IN FIRST OUT)             ║
║         Struktur Data: Linked List (Node-based Queue)               ║
║         Versi Multi-Loket: Setiap layanan punya antrian sendiri     ║
╚══════════════════════════════════════════════════════════════════════╝

Antrian FIFO bekerja dengan prinsip:
- Elemen yang PERTAMA masuk → PERTAMA keluar
- Operasi utama: enqueue (masuk dari belakang) & dequeue (keluar dari depan)
- Tidak boleh menyela antrian → FAIRNESS terjamin

Konfigurasi Loket:
    Loket 1  → Perpanjangan STNK Tahunan
    Loket 2  → Perpanjangan STNK 5 Tahunan
    Loket 3  → Balik Nama Kendaraan
    Loket 4  → Ganti STNK Hilang/Rusak
    Loket 5  → Mutasi Kendaraan
"""


# ── Mapping jenis layanan ke loket ───────────────────────────────────────────
LOKET_MAP = {
    "Perpanjangan STNK Tahunan":    1,
    "Perpanjangan STNK 5 Tahunan":  2,
    "Balik Nama Kendaraan":         3,
    "Ganti STNK Hilang/Rusak":      4,
    "Mutasi Kendaraan":             5,
}

# Prefix nomor antrian per loket
PREFIX_MAP = {
    1: "A",  # Loket 1 → A001, A002 …
    2: "B",  # Loket 2 → B001, B002 …
    3: "C",  # Loket 3 → C001 …
    4: "D",  # Loket 4 → D001 …
    5: "E",  # Loket 5 → E001 …
}

DAFTAR_LAYANAN = list(LOKET_MAP.keys())


def get_loket(jenis_layanan: str) -> int:
    """Mengembalikan nomor loket berdasarkan jenis layanan."""
    return LOKET_MAP.get(jenis_layanan, 1)


def get_prefix(jenis_layanan: str) -> str:
    """Mengembalikan prefix nomor antrian berdasarkan jenis layanan."""
    loket = get_loket(jenis_layanan)
    return PREFIX_MAP.get(loket, "A")


class Node:
    """
    Simpul (node) dalam linked list untuk antrian.
    Setiap node menyimpan data pelanggan dan pointer ke node berikutnya.
    """
    def __init__(self, data: dict):
        self.data = data
        self.next: "Node" = None


class AntrianFIFO:
    """
    Implementasi Antrian FIFO menggunakan Linked List.

    Struktur:
        DEPAN (head) ← keluar sini          masuk sini → BELAKANG (tail)
        [A] → [B] → [C] → [D] → None

    Kompleksitas:
        - enqueue (tambah): O(1)
        - dequeue (hapus) : O(1)
        - peek (lihat)    : O(1)
        - lihat_semua     : O(n)
        - ukuran          : O(1)
    """

    def __init__(self):
        self._depan: Node = None
        self._belakang: Node = None
        self._jumlah: int = 0

    def enqueue(self, data: dict) -> None:
        """Menambahkan pelanggan baru ke BELAKANG antrian."""
        node_baru = Node(data)
        if self.kosong():
            self._depan = node_baru
            self._belakang = node_baru
        else:
            self._belakang.next = node_baru
            self._belakang = node_baru
        self._jumlah += 1

    def dequeue(self) -> dict | None:
        """Mengambil dan menghapus pelanggan dari DEPAN antrian."""
        if self.kosong():
            return None
        data_keluar = self._depan.data
        self._depan = self._depan.next
        if self._depan is None:
            self._belakang = None
        self._jumlah -= 1
        return data_keluar

    def peek(self) -> dict | None:
        """Melihat data pelanggan paling depan tanpa memanggilnya."""
        if self.kosong():
            return None
        return self._depan.data

    def lihat_semua(self) -> list[dict]:
        """Mengembalikan daftar semua pelanggan dalam antrian."""
        hasil = []
        saat_ini = self._depan
        while saat_ini is not None:
            hasil.append(saat_ini.data)
            saat_ini = saat_ini.next
        return hasil

    def kosong(self) -> bool:
        return self._jumlah == 0

    def ukuran(self) -> int:
        return self._jumlah

    def clear(self) -> None:
        self._depan = None
        self._belakang = None
        self._jumlah = 0

    def __repr__(self) -> str:
        items = self.lihat_semua()
        if not items:
            return "AntrianFIFO: [KOSONG]"
        nomor_list = [item.get("nomor", "?") for item in items]
        return f"AntrianFIFO (DEPAN→): {' → '.join(nomor_list)} :→BELAKANG"

    def __len__(self) -> int:
        return self._jumlah


class SistemMultiLoket:
    """
    Manajemen antrian untuk seluruh loket pelayanan.

    Setiap jenis layanan memiliki:
    - Antrian sendiri (AntrianFIFO)
    - Slot 'sedang_dilayani' sendiri
    - Counter nomor sendiri
    - Riwayat sendiri

    Sehingga Loket 1 bisa melayani A001 sementara Loket 2 melayani B001
    secara bersamaan dan independen.
    """

    def __init__(self):
        # Satu antrian per loket
        self.antrian: dict[int, AntrianFIFO] = {
            loket: AntrianFIFO() for loket in range(1, 6)
        }
        # Siapa yang sedang dilayani di tiap loket (None jika kosong)
        self.sedang_dilayani: dict[int, dict | None] = {
            loket: None for loket in range(1, 6)
        }
        # Counter nomor per loket
        self.counter: dict[int, int] = {loket: 1 for loket in range(1, 6)}
        # Riwayat per loket
        self.riwayat: dict[int, list] = {loket: [] for loket in range(1, 6)}

    def buat_nomor(self, loket: int) -> str:
        """Membuat nomor antrian berikutnya untuk loket tertentu."""
        prefix = PREFIX_MAP.get(loket, "A")
        nomor = f"{prefix}{self.counter[loket]:03d}"
        self.counter[loket] += 1
        return nomor

    def daftar(self, data_pelanggan: dict) -> str:
        """
        Mendaftarkan pelanggan ke antrian sesuai jenis layanannya.
        Mengembalikan nomor antrian yang diberikan.
        """
        jenis = data_pelanggan.get("jenis_layanan", "Perpanjangan STNK Tahunan")
        loket = get_loket(jenis)
        nomor = self.buat_nomor(loket)
        data_pelanggan["nomor"] = nomor
        data_pelanggan["loket"] = loket
        self.antrian[loket].enqueue(data_pelanggan)
        return nomor

    def panggil(self, loket: int) -> dict | None:
        """
        Memanggil pelanggan berikutnya di loket tertentu.
        Hanya bisa jika loket sedang tidak melayani siapapun.
        """
        if self.sedang_dilayani[loket] is not None:
            return None  # Masih ada yang dilayani
        if self.antrian[loket].kosong():
            return None  # Tidak ada antrian
        pelanggan = self.antrian[loket].dequeue()
        self.sedang_dilayani[loket] = pelanggan
        return pelanggan

    def selesai(self, loket: int) -> dict | None:
        """
        Menyelesaikan pelayanan di loket tertentu.
        Pelanggan dipindah ke riwayat.
        """
        if self.sedang_dilayani[loket] is None:
            return None
        from utils import format_waktu_sekarang
        selesai = self.sedang_dilayani[loket]
        selesai["waktu_selesai"] = format_waktu_sekarang()
        self.riwayat[loket].append(selesai)
        self.sedang_dilayani[loket] = None
        return selesai

    def reset(self) -> None:
        """Reset seluruh sistem ke kondisi awal."""
        for loket in range(1, 6):
            self.antrian[loket].clear()
            self.sedang_dilayani[loket] = None
            self.counter[loket] = 1
            self.riwayat[loket] = []

    def total_menunggu(self) -> int:
        return sum(self.antrian[l].ukuran() for l in range(1, 6))

    def total_selesai(self) -> int:
        return sum(len(self.riwayat[l]) for l in range(1, 6))

    def total_aktif(self) -> int:
        return sum(1 for l in range(1, 6) if self.sedang_dilayani[l] is not None)

    def semua_riwayat(self) -> list[dict]:
        """Gabungan riwayat semua loket, diurutkan dari terbaru."""
        hasil = []
        for loket in range(1, 6):
            hasil.extend(self.riwayat[loket])
        # Sort berdasarkan waktu_selesai jika ada
        hasil.sort(key=lambda x: x.get("waktu_selesai", ""), reverse=True)
        return hasil


# ══════════════════════════════════════════════════════════════════════════════
# DEMO / TEST (jalankan langsung: python queue_system.py)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("  DEMO SISTEM MULTI-LOKET")
    print("=" * 60)

    sistem = SistemMultiLoket()

    # Daftarkan pelanggan di berbagai loket
    pelanggan_demo = [
        {"nama": "Budi Santoso",  "no_polisi": "E 1234 AB", "jenis_layanan": "Perpanjangan STNK Tahunan"},
        {"nama": "Dewi Rahayu",   "no_polisi": "B 5678 CD", "jenis_layanan": "Perpanjangan STNK 5 Tahunan"},
        {"nama": "Ahmad Fauzi",   "no_polisi": "E 9012 EF", "jenis_layanan": "Perpanjangan STNK Tahunan"},
        {"nama": "Sari Indah",    "no_polisi": "D 3456 GH", "jenis_layanan": "Balik Nama Kendaraan"},
        {"nama": "Rizky Maulana", "no_polisi": "E 7890 IJ", "jenis_layanan": "Ganti STNK Hilang/Rusak"},
    ]

    print("\n📋 Mendaftarkan pelanggan...")
    for p in pelanggan_demo:
        import datetime
        p["waktu_daftar"] = datetime.datetime.now().strftime("%H:%M:%S")
        p["tanggal"] = datetime.datetime.now().strftime("%d/%m/%Y")
        p["no_hp"] = "-"
        nomor = sistem.daftar(p)
        loket = get_loket(p["jenis_layanan"])
        print(f"  ✅ {nomor} → Loket {loket} | {p['nama']} | {p['jenis_layanan']}")

    print(f"\nTotal menunggu: {sistem.total_menunggu()}")

    print("\n📢 Panggil semua loket secara bersamaan...")
    for loket in range(1, 6):
        hasil = sistem.panggil(loket)
        if hasil:
            print(f"  Loket {loket}: 🔔 {hasil['nomor']} - {hasil['nama']}")
        else:
            print(f"  Loket {loket}: (kosong)")

    print("\n✅ Selesaikan semua loket...")
    for loket in range(1, 6):
        hasil = sistem.selesai(loket)
        if hasil:
            print(f"  Loket {loket}: ✅ {hasil['nomor']} - {hasil['nama']} selesai")