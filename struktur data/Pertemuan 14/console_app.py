"""
╔══════════════════════════════════════════════════════════════════════╗
║      SISTEM ANTRIAN FIFO — MODE CONSOLE (TERMINAL)                 ║
║      Pelayanan Perpanjangan STNK Pajak Tahunan                     ║
║      Multi-Loket | Senin–Jumat | 08:00–16:00 WIB                  ║
║                                                                      ║
║  Jalankan: python console_app.py                                    ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
from datetime import datetime

from queue_system import SistemMultiLoket, LOKET_MAP, DAFTAR_LAYANAN, get_loket
from tts_helper import generate_audio_file, buat_pesan_panggil, buat_pesan_daftar, buat_pesan_selesai
from utils import get_estimasi_waktu, format_waktu_sekarang, cek_jam_pelayanan, get_info_pelayanan


# ─── Warna ANSI ───────────────────────────────────────────────────────────────
class W:
    MERAH    = "\033[91m"
    HIJAU    = "\033[92m"
    KUNING   = "\033[93m"
    BIRU     = "\033[94m"
    MAGENTA  = "\033[95m"
    CYAN     = "\033[96m"
    PUTIH    = "\033[97m"
    BOLD     = "\033[1m"
    DIM      = "\033[2m"
    RESET    = "\033[0m"
    BG_MERAH = "\033[41m"
    BG_BIRU  = "\033[44m"
    BG_HIJAU = "\033[42m"
    BG_ABU   = "\033[100m"


# Warna per loket di terminal
WARNA_LOKET_TERM = {
    1: W.MERAH,
    2: W.KUNING,
    3: W.CYAN,
    4: W.HIJAU,
    5: W.BIRU,
}


def bersihkan_layar():
    os.system("cls" if os.name == "nt" else "clear")


def garis(kar: str = "═", lebar: int = 70, warna: str = W.CYAN):
    print(f"{warna}{kar * lebar}{W.RESET}")


def cetak_header():
    bersihkan_layar()
    garis("═", 70, W.MERAH)
    print(f"{W.BOLD}{W.MERAH}{'🚗  SISTEM ANTRIAN FIFO MULTI-LOKET  🚗':^70}{W.RESET}")
    print(f"{W.KUNING}{'Pelayanan Perpanjangan STNK Pajak Tahunan':^70}{W.RESET}")
    print(f"{W.DIM}{'SAMSAT — Jam Pelayanan: Senin–Jumat 08:00–16:00 WIB':^70}{W.RESET}")
    garis("═", 70, W.MERAH)
    waktu = datetime.now().strftime("%A, %d %B %Y  |  %H:%M:%S")
    print(f"{W.DIM}{waktu:^70}{W.RESET}")

    # Status jam pelayanan
    aktif, pesan = cek_jam_pelayanan()
    if aktif:
        print(f"{W.BG_HIJAU}{W.BOLD}{'  ✅ PELAYANAN SEDANG BERJALAN  ':^70}{W.RESET}")
    else:
        print(f"{W.BG_MERAH}{W.BOLD}{'  ⛔ ' + pesan + '  ':^70}{W.RESET}")

    garis("─", 70, W.DIM)


def cetak_menu():
    print(f"\n{W.BOLD}{W.PUTIH}  MENU UTAMA:{W.RESET}")
    print(f"  {W.CYAN}[1]{W.RESET} 📋  Daftar Antrian Baru")
    print(f"  {W.CYAN}[2]{W.RESET} 📢  Panggil Pelanggan (pilih loket)")
    print(f"  {W.CYAN}[3]{W.RESET} ✅  Selesaikan Pelayanan (pilih loket)")
    print(f"  {W.CYAN}[4]{W.RESET} 👁   Lihat Semua Antrian")
    print(f"  {W.CYAN}[5]{W.RESET} 📜  Riwayat per Jenis Layanan")
    print(f"  {W.CYAN}[6]{W.RESET} 📊  Statistik")
    print(f"  {W.CYAN}[0]{W.RESET} 🚪  Keluar\n")
    garis("─", 70, W.DIM)


def tampil_status_loket(sistem: SistemMultiLoket):
    """Menampilkan status ringkas semua loket."""
    print(f"\n  {W.BOLD}Status Loket:{W.RESET}")
    for loket in range(1, 6):
        nama_layanan = DAFTAR_LAYANAN[loket - 1]
        warna = WARNA_LOKET_TERM[loket]
        dilayani = sistem.sedang_dilayani[loket]
        jml = sistem.antrian[loket].ukuran()

        if dilayani:
            status = f"{W.BG_HIJAU}{W.BOLD} AKTIF {W.RESET} {W.HIJAU}{dilayani['nomor']} — {dilayani['nama']}{W.RESET}"
        elif jml > 0:
            status = f"{W.DIM}[Kosong]{W.RESET} {W.KUNING}{jml} menunggu{W.RESET}"
        else:
            status = f"{W.DIM}[Kosong — tidak ada antrian]{W.RESET}"

        print(f"  {warna}Loket {loket}{W.RESET} {W.DIM}({nama_layanan[:25]}){W.RESET}")
        print(f"    {status}")

    total = sistem.total_menunggu()
    warna_jml = W.HIJAU if total == 0 else W.KUNING if total < 10 else W.MERAH
    print(f"\n  {W.BOLD}Total menunggu:{W.RESET} {warna_jml}{total} orang{W.RESET}")


def pilih_loket(sistem: SistemMultiLoket, mode: str = "panggil") -> int | None:
    """Interaktif memilih loket."""
    print(f"\n{W.BOLD}{W.CYAN}  Pilih Loket:{W.RESET}")
    for loket in range(1, 6):
        nama_layanan = DAFTAR_LAYANAN[loket - 1]
        warna = WARNA_LOKET_TERM[loket]
        dilayani = sistem.sedang_dilayani[loket]
        jml = sistem.antrian[loket].ukuran()

        if mode == "panggil":
            keterangan = f"{W.KUNING}{jml} menunggu{W.RESET}" if jml > 0 else f"{W.DIM}kosong{W.RESET}"
            if dilayani:
                keterangan += f" | {W.DIM}sedang dilayani: {dilayani['nomor']}{W.RESET}"
        else:  # selesai
            if dilayani:
                keterangan = f"{W.HIJAU}sedang: {dilayani['nomor']} — {dilayani['nama']}{W.RESET}"
            else:
                keterangan = f"{W.DIM}tidak ada yang dilayani{W.RESET}"

        print(f"  {W.CYAN}[{loket}]{W.RESET} {warna}Loket {loket}{W.RESET} "
              f"{W.DIM}({nama_layanan[:28]}){W.RESET} — {keterangan}")

    print(f"  {W.CYAN}[0]{W.RESET} Batal")
    pilih = input(f"\n  {W.KUNING}Pilih loket [0-5]:{W.RESET} ").strip()
    try:
        n = int(pilih)
        if n == 0:
            return None
        if 1 <= n <= 5:
            return n
        return None
    except ValueError:
        return None


def input_pelanggan() -> dict | None:
    """Interaktif input data pelanggan baru."""
    print(f"\n{W.BOLD}{W.CYAN}  ╔═══ PENDAFTARAN ANTRIAN ═══╗{W.RESET}")

    nama = input(f"  {W.KUNING}Nama Lengkap      :{W.RESET} ").strip().title()
    if not nama:
        print(f"  {W.MERAH}✗ Nama tidak boleh kosong!{W.RESET}")
        return None

    no_polisi = input(f"  {W.KUNING}Nomor Polisi       :{W.RESET} ").strip().upper()
    if not no_polisi:
        print(f"  {W.MERAH}✗ Nomor polisi tidak boleh kosong!{W.RESET}")
        return None

    print(f"\n  {W.BOLD}Jenis Layanan & Loket:{W.RESET}")
    for i, layanan in enumerate(DAFTAR_LAYANAN, 1):
        loket = LOKET_MAP[layanan]
        warna = WARNA_LOKET_TERM[loket]
        print(f"    {W.CYAN}[{i}]{W.RESET} {warna}Loket {loket}{W.RESET} — {layanan}")

    pilih = input(f"  {W.KUNING}Pilih [1-5]        :{W.RESET} ").strip()
    try:
        idx = int(pilih) - 1
        if not (0 <= idx < len(DAFTAR_LAYANAN)):
            raise ValueError
        jenis_layanan = DAFTAR_LAYANAN[idx]
    except (ValueError, IndexError):
        print(f"  {W.MERAH}✗ Pilihan tidak valid! Menggunakan pilihan 1.{W.RESET}")
        jenis_layanan = DAFTAR_LAYANAN[0]

    no_hp = input(f"  {W.KUNING}Nomor HP (opsional):{W.RESET} ").strip() or "-"

    return {
        "nama":           nama,
        "no_polisi":      no_polisi,
        "jenis_layanan":  jenis_layanan,
        "no_hp":          no_hp,
        "waktu_daftar":   format_waktu_sekarang(),
        "tanggal":        datetime.now().strftime("%d/%m/%Y"),
    }


def tampil_semua_antrian(sistem: SistemMultiLoket):
    """Menampilkan seluruh isi antrian per loket."""
    print(f"\n{W.BOLD}{W.CYAN}  ╔═══ DAFTAR ANTRIAN PER LOKET ═══╗{W.RESET}")
    ada = False
    for loket in range(1, 6):
        items = sistem.antrian[loket].lihat_semua()
        if not items:
            continue
        ada = True
        nama_layanan = DAFTAR_LAYANAN[loket - 1]
        warna = WARNA_LOKET_TERM[loket]
        print(f"\n  {warna}Loket {loket} — {nama_layanan}{W.RESET} ({len(items)} orang)")
        garis("─", 60, W.DIM)
        print(f"  {'Posisi':<8} {'Nomor':<7} {'Nama':<22} {'Estimasi':<10}")
        garis("─", 60, W.DIM)
        for i, item in enumerate(items, 1):
            estimasi = get_estimasi_waktu(i)
            print(f"  {W.DIM}{i:<8}{W.RESET}"
                  f"{warna}{item['nomor']:<7}{W.RESET}"
                  f"{item['nama']:<22}"
                  f"{W.KUNING}~{estimasi} mnt{W.RESET}")

    if not ada:
        print(f"\n  {W.DIM}(Semua antrian kosong){W.RESET}")
    garis("─", 70, W.DIM)


def tampil_riwayat(sistem: SistemMultiLoket):
    """Menampilkan riwayat pelayanan dipisah per jenis layanan."""
    print(f"\n{W.BOLD}{W.CYAN}  ╔═══ RIWAYAT PELAYANAN PER LOKET ═══╗{W.RESET}")

    ada_riwayat = False
    for loket in range(1, 6):
        riwayat = sistem.riwayat[loket]
        if not riwayat:
            continue
        ada_riwayat = True
        nama_layanan = DAFTAR_LAYANAN[loket - 1]
        warna = WARNA_LOKET_TERM[loket]

        print(f"\n  {warna}{W.BOLD}Loket {loket} — {nama_layanan}{W.RESET} ({len(riwayat)} selesai)")
        garis("─", 60, W.DIM)

        for item in reversed(riwayat[-10:]):
            print(f"  {W.HIJAU}✅{W.RESET} [{item['nomor']}] "
                  f"{W.BOLD}{item['nama']}{W.RESET} "
                  f"{W.DIM}| {item['no_polisi']}{W.RESET}")
            print(f"     {W.DIM}Selesai: {item.get('waktu_selesai','—')}{W.RESET}")

    if not ada_riwayat:
        print(f"\n  {W.DIM}(Belum ada riwayat){W.RESET}")

    garis("─", 70, W.DIM)


def tampil_statistik(sistem: SistemMultiLoket):
    """Menampilkan statistik sistem antrian per loket."""
    print(f"\n{W.BOLD}{W.CYAN}  ╔═══ STATISTIK HARI INI ═══╗{W.RESET}")
    garis("─", 50, W.DIM)

    for loket in range(1, 6):
        nama_layanan = DAFTAR_LAYANAN[loket - 1]
        warna = WARNA_LOKET_TERM[loket]
        dilayani = sistem.sedang_dilayani[loket]
        jml_antrian = sistem.antrian[loket].ukuran()
        jml_selesai = len(sistem.riwayat[loket])

        print(f"  {warna}Loket {loket}{W.RESET} {W.DIM}({nama_layanan[:25]}){W.RESET}")
        print(f"    Menunggu: {W.KUNING}{jml_antrian:>3}{W.RESET}  |  "
              f"Aktif: {W.HIJAU}{1 if dilayani else 0:>1}{W.RESET}  |  "
              f"Selesai: {W.HIJAU}{jml_selesai:>3}{W.RESET}")

    garis("─", 50, W.DIM)
    total = sistem.total_menunggu() + sistem.total_selesai() + sistem.total_aktif()
    print(f"  Total keseluruhan : {W.BOLD}{total:>3}{W.RESET} orang")
    print(f"  Selesai hari ini  : {W.HIJAU}{sistem.total_selesai():>3}{W.RESET} orang")

    if sistem.total_menunggu() > 0:
        estimasi_max = get_estimasi_waktu(max(
            sistem.antrian[l].ukuran() for l in range(1, 6)
        ))
        print(f"  Estimasi terlama  : {W.KUNING}~{estimasi_max} menit{W.RESET}")


def main():
    """Fungsi utama — loop program console."""
    sistem = SistemMultiLoket()

    while True:
        cetak_header()
        tampil_status_loket(sistem)
        cetak_menu()

        pilihan = input(f"  {W.BOLD}Pilih menu [{W.CYAN}0-6{W.PUTIH}]{W.RESET}: ").strip()

        # ── [1] Daftar Antrian ────────────────────────────────────────────────
        if pilihan == "1":
            aktif, pesan = cek_jam_pelayanan()
            if not aktif:
                cetak_header()
                print(f"\n  {W.MERAH}⛔ {pesan}{W.RESET}")
                print(f"  {W.DIM}Pendaftaran hanya Senin–Jumat pukul 08:00–16:00 WIB.{W.RESET}")
            else:
                cetak_header()
                data = input_pelanggan()
                if data:
                    nomor = sistem.daftar(data)
                    loket = data["loket"]
                    estimasi = get_estimasi_waktu(sistem.antrian[loket].ukuran())
                    warna_l = WARNA_LOKET_TERM[loket]

                    # TTS
                    pesan_tts = buat_pesan_daftar(nomor, data["nama"], estimasi, loket)
                    audio = generate_audio_file(pesan_tts, f"daftar_{nomor}")

                    print(f"\n  {W.HIJAU}✅ Berhasil!{W.RESET}")
                    print(f"  Nomor antrian : {W.BOLD}{W.KUNING}{nomor}{W.RESET}")
                    print(f"  Loket         : {warna_l}{W.BOLD}Loket {loket}{W.RESET} "
                          f"{W.DIM}({data['jenis_layanan']}){W.RESET}")
                    print(f"  Estimasi tunggu: {W.KUNING}~{estimasi} menit{W.RESET}")
                    if audio:
                        print(f"  {W.CYAN}🔊 Audio: {audio}{W.RESET}")

            input(f"\n  {W.DIM}[Tekan Enter untuk lanjut...]{W.RESET}")

        # ── [2] Panggil Berikutnya ────────────────────────────────────────────
        elif pilihan == "2":
            cetak_header()
            loket = pilih_loket(sistem, mode="panggil")
            if loket is None:
                pass
            elif sistem.sedang_dilayani[loket] is not None:
                print(f"\n  {W.KUNING}⚠ Loket {loket} masih melayani: "
                      f"{sistem.sedang_dilayani[loket]['nomor']} — "
                      f"{sistem.sedang_dilayani[loket]['nama']}{W.RESET}")
                print(f"  Selesaikan pelayanan dulu (menu 3).")
            elif sistem.antrian[loket].kosong():
                print(f"\n  {W.DIM}Tidak ada antrian di Loket {loket}.{W.RESET}")
            else:
                pelanggan = sistem.panggil(loket)
                if pelanggan:
                    warna_l = WARNA_LOKET_TERM[loket]
                    pesan_tts = buat_pesan_panggil(pelanggan["nomor"], pelanggan["nama"], loket)
                    audio = generate_audio_file(pesan_tts, f"panggil_{pelanggan['nomor']}")

                    garis("═", 70, W.HIJAU)
                    print(f"\n{W.BOLD}{W.HIJAU}  📢 MEMANGGIL — LOKET {loket}:{W.RESET}")
                    print(f"\n    {W.BOLD}Nomor  : {W.KUNING}{pelanggan['nomor']}{W.RESET}")
                    print(f"    {W.BOLD}Nama   : {pelanggan['nama']}{W.RESET}")
                    print(f"    {W.BOLD}Loket  : {warna_l}Loket {loket}{W.RESET} "
                          f"{W.DIM}({pelanggan['jenis_layanan']}){W.RESET}")
                    print(f"    {W.BOLD}Polisi : {pelanggan['no_polisi']}{W.RESET}\n")
                    garis("═", 70, W.HIJAU)
                    if audio:
                        print(f"  {W.CYAN}🔊 Audio: {audio}{W.RESET}")

            input(f"\n  {W.DIM}[Tekan Enter untuk lanjut...]{W.RESET}")

        # ── [3] Selesaikan Pelayanan ──────────────────────────────────────────
        elif pilihan == "3":
            cetak_header()
            loket = pilih_loket(sistem, mode="selesai")
            if loket is None:
                pass
            elif sistem.sedang_dilayani[loket] is None:
                print(f"\n  {W.DIM}Tidak ada pelanggan yang sedang dilayani di Loket {loket}.{W.RESET}")
            else:
                hasil = sistem.selesai(loket)
                if hasil:
                    pesan_tts = buat_pesan_selesai(hasil["nama"], loket)
                    audio = generate_audio_file(pesan_tts, f"selesai_{hasil['nomor']}")

                    print(f"\n  {W.HIJAU}✅ Pelayanan selesai!{W.RESET}")
                    print(f"  [{hasil['nomor']}] {hasil['nama']} — Loket {loket}")
                    print(f"  {W.DIM}Waktu selesai: {hasil['waktu_selesai']}{W.RESET}")
                    if audio:
                        print(f"  {W.CYAN}🔊 Audio: {audio}{W.RESET}")

            input(f"\n  {W.DIM}[Tekan Enter untuk lanjut...]{W.RESET}")

        # ── [4] Lihat Semua Antrian ───────────────────────────────────────────
        elif pilihan == "4":
            cetak_header()
            tampil_semua_antrian(sistem)
            input(f"\n  {W.DIM}[Tekan Enter untuk lanjut...]{W.RESET}")

        # ── [5] Riwayat ───────────────────────────────────────────────────────
        elif pilihan == "5":
            cetak_header()
            tampil_riwayat(sistem)
            input(f"\n  {W.DIM}[Tekan Enter untuk lanjut...]{W.RESET}")

        # ── [6] Statistik ─────────────────────────────────────────────────────
        elif pilihan == "6":
            cetak_header()
            tampil_statistik(sistem)
            input(f"\n  {W.DIM}[Tekan Enter untuk lanjut...]{W.RESET}")

        # ── [0] Keluar ────────────────────────────────────────────────────────
        elif pilihan == "0":
            cetak_header()
            print(f"\n  {W.KUNING}Terima kasih telah menggunakan Sistem Antrian STNK.{W.RESET}")
            print(f"  {W.DIM}Total dilayani hari ini: {sistem.total_selesai()} orang{W.RESET}\n")
            garis("═", 70, W.MERAH)
            sys.exit(0)

        else:
            print(f"\n  {W.MERAH}✗ Pilihan tidak valid! Masukkan angka 0-6.{W.RESET}")
            time.sleep(1)


if __name__ == "__main__":
    main()