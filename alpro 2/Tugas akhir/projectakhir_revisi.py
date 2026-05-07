"""
╔══════════════════════════════════════════════════════╗
║         FurniSpace - E-Commerce Furnitur             ║
╚══════════════════════════════════════════════════════╝
"""

import hashlib
import os
from datetime import datetime

# ─────────────────────────────────────────
# 1. DATABASE SEDERHANA (Pakai Dictionary & List)
# ─────────────────────────────────────────

USERS = {}        # Menyimpan data pengguna
KERANJANG = []    # Menyimpan item belanja
CURRENT_USER = None  # Siapa yang sedang login

PRODUK = [
    {"id": 1, "nama": "Sofa Minimalis",    "kategori": "Sofa",  "harga": 4500000, "stok": 10, "rating": 4.8, "toko": "Mebel Jaya"},
    {"id": 2, "nama": "Meja Makan Jati",   "kategori": "Meja",  "harga": 3200000, "stok": 5,  "rating": 4.6, "toko": "Kayu Kita"},
    {"id": 3, "nama": "Lemari 4 Pintu",    "kategori": "Lemari","harga": 5800000, "stok": 8,  "rating": 4.7, "toko": "Home Elegance"},
    {"id": 4, "nama": "Kursi Ergonomis",   "kategori": "Kursi", "harga": 2100000, "stok": 20, "rating": 4.9, "toko": "ErgoFurn"},
    {"id": 5, "nama": "Tempat Tidur Queen","kategori": "Kasur", "harga": 6700000, "stok": 4,  "rating": 4.5, "toko": "Mebel Jaya"},
]


# ─────────────────────────────────────────
# 2. FUNGSI UTILITAS (Pembantu)
# ─────────────────────────────────────────

def format_rupiah(angka):
    """Mengubah angka menjadi format Rupiah. Contoh: 4500000 → Rp 4.500.000"""
    return f"Rp {angka:,.0f}".replace(",", ".")

def hash_password(password):
    """Mengenkripsi password agar tidak tersimpan sebagai teks biasa."""
    return hashlib.sha256(password.encode()).hexdigest()

def garis():
    """Mencetak garis pemisah horizontal."""
    print("─" * 50)

def garis_tebal():
    """Mencetak garis pemisah tebal (untuk judul section)."""
    print("═" * 50)

def jeda():
    """Menambahkan baris kosong sebagai jarak antar bagian."""
    print()

def bersihkan_layar():
    """Membersihkan layar terminal (cls untuk Windows, clear untuk Linux/Mac)."""
    os.system('cls' if os.name == 'nt' else 'clear')


# ─────────────────────────────────────────
# 3. FITUR AKUN (Daftar & Login)
#    Dibuat oleh: Akbar
# ─────────────────────────────────────────

def akbar_daftar_akun():
    """ Mendaftarkan pengguna baru ke dalam sistem."""
    global USERS

    bersihkan_layar()
    garis_tebal()
    print("           📋  DAFTAR AKUN BARU")
    garis_tebal()

    nama     = input("  Nama Lengkap : ")
    username = input("  Username     : ")
    password = input("  Password     : ")

    # Cek apakah username sudah dipakai
    if username in USERS:
        garis()
        print("  ⚠️  Username sudah digunakan!")
        garis()
        input("  Tekan Enter untuk kembali ke menu...")
        return

    # Simpan data user ke dictionary USERS
    USERS[username] = {
        "nama":          nama,
        "password_hash": hash_password(password),
        "tgl_daftar":    datetime.now().strftime("%d-%m-%Y"),
    }

    garis()
    print(f"  ✅ Akun '{username}' berhasil dibuat!")
    garis()
    input("  Tekan Enter untuk kembali ke menu...")


def akbar_login():
    """ Memverifikasi username dan password pengguna."""
    global CURRENT_USER

    bersihkan_layar()
    garis_tebal()
    print("              🔐  LOGIN AKUN")
    garis_tebal()

    username = input("  Username : ")
    password = input("  Password : ")

    # Cek apakah username ada & password cocok
    if username in USERS and USERS[username]["password_hash"] == hash_password(password):
        CURRENT_USER = username
        garis()
        print(f"  ✅ Login berhasil! Halo, {USERS[username]['nama']} 👋")
        garis()
    else:
        garis()
        print("  ❌ Username atau password salah!")
        garis()
    input("  Tekan Enter untuk kembali ke menu...")


def akbar_logout():
    """ Mengeluarkan pengguna dari sesi aktif."""
    global CURRENT_USER

    bersihkan_layar()
    garis()
    if CURRENT_USER:
        print(f"  👋 Sampai jumpa, {USERS[CURRENT_USER]['nama']}!")
        CURRENT_USER = None
    else:
        print("  ⚠️  Kamu belum login.")
    garis()
    input("  Tekan Enter untuk kembali ke menu...")


# ─────────────────────────────────────────
# 4. FITUR PRODUK (Lihat & Cari)
#    Dibuat oleh: Piga
# ─────────────────────────────────────────

def piga_tampil_semua_produk():
    """ Menampilkan seluruh daftar produk yang tersedia."""
    bersihkan_layar()
    garis_tebal()
    print("           🛋️   DAFTAR SEMUA PRODUK")
    garis_tebal()
    print(f"  {'No':<4} {'Nama Produk':<25} {'Harga':<15} {'Stok':<6} {'Rating'}")
    garis()
    for i, p in enumerate(PRODUK, 1):
        print(f"  {i:<4} {p['nama']:<25} {format_rupiah(p['harga']):<15} {p['stok']:<6} ★{p['rating']}")
    garis()


def piga_cari_produk():
    """Mencari produk berdasarkan kata kunci nama atau kategori."""
    bersihkan_layar()
    garis_tebal()
    print("           🔍  CARI PRODUK")
    garis_tebal()

    kata = input("  Kata kunci : ").strip().lower()
    hasil = [p for p in PRODUK if kata in p["nama"].lower() or kata in p["kategori"].lower()]

    garis()
    if hasil:
        print(f"  🔍 Ditemukan {len(hasil)} produk:")
        jeda()
        for p in hasil:
            print(f"  • {p['nama']:<25} | {format_rupiah(p['harga']):<15} | Toko: {p['toko']}")
    else:
        print("  ❌ Produk tidak ditemukan.")
    garis()
    input("  Tekan Enter untuk kembali ke menu...")


def piga_filter_kategori():
    """ Menampilkan produk berdasarkan kategori tertentu."""
    bersihkan_layar()
    garis_tebal()
    print("           📂  FILTER KATEGORI")
    garis_tebal()

    # Ambil semua kategori unik dari PRODUK
    kategori_list = list(set(p["kategori"] for p in PRODUK))

    print("  Kategori yang tersedia:")
    jeda()
    for i, k in enumerate(kategori_list, 1):
        print(f"    [{i}] {k}")

    garis()
    pilihan = int(input("  Pilih nomor kategori: ")) - 1
    kategori = kategori_list[pilihan]

    hasil = [p for p in PRODUK if p["kategori"] == kategori]

    jeda()
    garis_tebal()
    print(f"      📦  Produk Kategori: {kategori}")
    garis_tebal()
    for p in hasil:
        print(f"  • {p['nama']:<25} | {format_rupiah(p['harga']):<15} | Stok: {p['stok']}")
    garis()
    input("  Tekan Enter untuk kembali ke menu...")


# ─────────────────────────────────────────
# 5. FITUR KERANJANG & CHECKOUT
#    Dibuat oleh: Alfa
# ─────────────────────────────────────────

def alfa_tambah_keranjang():
    """ Menambahkan produk ke keranjang belanja."""
    bersihkan_layar()
    piga_tampil_semua_produk()

    garis()
    no    = int(input("  Pilih nomor produk : ")) - 1
    jml   = int(input("  Jumlah             : "))
    produk = PRODUK[no]

    # Hitung jumlah yg sudah ada di keranjang untuk produk ini
    sudah_di_keranjang = 0
    for item in KERANJANG:
        if item["id"] == produk["id"]:
            sudah_di_keranjang = item["jumlah"]
            break

    # Validasi stok mencukupi
    if jml <= 0:
        garis()
        print("  ⚠️  Jumlah harus lebih dari 0!")
        garis()
        input("  Tekan Enter untuk kembali ke menu...")
        return

    if (sudah_di_keranjang + jml) > produk["stok"]:
        garis()
        print(f"  ❌ Stok tidak mencukupi! Stok tersedia: {produk['stok']}")
        if sudah_di_keranjang > 0:
            print(f"     (Sudah {sudah_di_keranjang} pcs di keranjang)")
        garis()
        input("  Tekan Enter untuk kembali ke menu...")
        return

    # Cek apakah produk sudah ada di keranjang
    for item in KERANJANG:
        if item["id"] == produk["id"]:
            item["jumlah"] += jml
            garis()
            print(f"  ✅ Jumlah {produk['nama']} diperbarui menjadi {item['jumlah']} pcs.")
            garis()
            input("  Tekan Enter untuk kembali ke menu...")
            return

    KERANJANG.append({
        "id":     produk["id"],
        "nama":   produk["nama"],
        "harga":  produk["harga"],
        "jumlah": jml,
    })
    garis()
    print(f"  ✅ {produk['nama']} x{jml} ditambahkan ke keranjang!")
    garis()
    input("  Tekan Enter untuk kembali ke menu...")


def alfa_lihat_keranjang():
    """ Menampilkan isi keranjang dan total belanja."""
    bersihkan_layar()
    garis_tebal()
    print("           🛒  KERANJANG BELANJA")
    garis_tebal()

    if not KERANJANG:
        print("  🛒 Keranjang masih kosong!")
        garis()
        input("  Tekan Enter untuk kembali ke menu...")
        return

    total = 0
    for i, item in enumerate(KERANJANG, 1):
        subtotal = item["harga"] * item["jumlah"]
        total   += subtotal
        print(f"  {i}. {item['nama']:<25} x{item['jumlah']}  =  {format_rupiah(subtotal)}")

    garis()
    print(f"  💰 TOTAL BELANJA  :  {format_rupiah(total)}")
    garis()
    input("  Tekan Enter untuk kembali ke menu...")


def alfa_checkout():
    """ Memproses pembelian dan mengosongkan keranjang."""
    if not CURRENT_USER:
        bersihkan_layar()
        garis()
        print("  ⚠️  Harap login terlebih dahulu!")
        garis()
        input("  Tekan Enter untuk kembali ke menu...")
        return

    # Tampilkan keranjang dulu (tanpa pause otomatis)
    bersihkan_layar()
    garis_tebal()
    print("           🛒  KERANJANG BELANJA")
    garis_tebal()

    if not KERANJANG:
        print("  🛒 Keranjang masih kosong!")
        garis()
        input("  Tekan Enter untuk kembali ke menu...")
        return

    total = 0
    for i, item in enumerate(KERANJANG, 1):
        subtotal = item["harga"] * item["jumlah"]
        total   += subtotal
        print(f"  {i}. {item['nama']:<25} x{item['jumlah']}  =  {format_rupiah(subtotal)}")
    garis()
    print(f"  💰 TOTAL BELANJA  :  {format_rupiah(total)}")
    garis()

    jeda()
    konfirm = input("  Konfirmasi pembelian? (y/n): ").strip().lower()
    garis()
    if konfirm == "y":
        # Kurangi stok setiap produk yang dibeli
        for item in KERANJANG:
            for produk in PRODUK:
                if produk["id"] == item["id"]:
                    produk["stok"] -= item["jumlah"]
                    break

        no_pesanan = f"FN{datetime.now().strftime('%d%m%Y%H%M%S')}"
        KERANJANG.clear()
        print(f"  🎉 Pesanan berhasil diproses!")
        print(f"  📦 No. Pesanan : {no_pesanan}")
        print(f"  📉 Stok produk telah diperbarui.")
    else:
        print("  ❌ Checkout dibatalkan.")
    garis()
    input("  Tekan Enter untuk kembali ke menu...")


# ─────────────────────────────────────────
# 6. MENU UTAMA
# ─────────────────────────────────────────

def menu_utama():
    """Titik masuk utama program — menampilkan pilihan menu."""
    # Tambahkan akun demo agar bisa langsung dicoba
    USERS["demo"] = {
        "nama":          "Pengguna Demo",
        "password_hash": hash_password("demo123"),
        "tgl_daftar":    "01-01-2025",
    }

    while True:
        bersihkan_layar()
        garis_tebal()
        print("       🪑  FurniSpace — E-Commerce Furnitur")
        garis_tebal()

        status = f"✅ Login sebagai: {CURRENT_USER}" if CURRENT_USER else "🔴 Belum Login"
        print(f"  {status}")
        garis()

        print("  ── AKUN (Akbar) ──────────────────────────")
        print("  [1] Daftar Akun")
        print("  [2] Login")
        print("  [3] Logout")
        garis()
        print("  ── PRODUK (Piga) ─────────────────────────")
        print("  [4] Lihat Semua Produk")
        print("  [5] Cari Produk")
        print("  [6] Filter Kategori")
        garis()
        print("  ── BELANJA (Alfa) ────────────────────────")
        print("  [7] Tambah ke Keranjang")
        print("  [8] Lihat Keranjang")
        print("  [9] Checkout")
        garis()
        print("  [0] Keluar")
        garis_tebal()

        pilihan = input("  Pilih menu: ").strip()

        if   pilihan == "1": akbar_daftar_akun()
        elif pilihan == "2": akbar_login()
        elif pilihan == "3": akbar_logout()
        elif pilihan == "4":
            piga_tampil_semua_produk()
            input("  Tekan Enter untuk kembali ke menu...")
        elif pilihan == "5": piga_cari_produk()
        elif pilihan == "6": piga_filter_kategori()
        elif pilihan == "7": alfa_tambah_keranjang()
        elif pilihan == "8": alfa_lihat_keranjang()
        elif pilihan == "9": alfa_checkout()
        elif pilihan == "0":
            jeda()
            garis_tebal()
            print("  👋 Terima kasih telah menggunakan FurniSpace!")
            print("       Sampai jumpa kembali! 🪑")
            garis_tebal()
            break
        else:
            garis()
            print("  ⚠️  Pilihan tidak valid! Silakan coba lagi.")
            garis()


# ─────────────────────────────────────────
# JALANKAN PROGRAM
# ─────────────────────────────────────────
if __name__ == "__main__":
    menu_utama()