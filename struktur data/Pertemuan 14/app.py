import streamlit as st
import os
from datetime import datetime

from queue_system import SistemMultiLoket, LOKET_MAP, DAFTAR_LAYANAN, get_loket, PREFIX_MAP
from tts_helper import generate_audio_file, buat_pesan_panggil, buat_pesan_daftar, buat_pesan_selesai
from utils import get_estimasi_waktu, format_waktu_sekarang, get_info_pelayanan, cek_jam_pelayanan

# ─── Konfigurasi Halaman ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Antrian STNK - Samsat",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS Custom ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

:root {
    --merah: #C0392B;
    --merah-gelap: #922B21;
    --emas: #F39C12;
    --emas-muda: #FAD7A0;
    --hitam: #1A1A1A;
    --abu-tua: #2C2C2C;
    --abu: #4A4A4A;
    --putih: #F5F5F0;
    --putih-krem: #FAFAF7;
    --hijau: #27AE60;
    --biru: #2980B9;
}

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: var(--hitam);
    color: var(--putih);
}

.header-banner {
    background: linear-gradient(135deg, var(--merah-gelap) 0%, var(--merah) 50%, #E74C3C 100%);
    border-bottom: 4px solid var(--emas);
    padding: 24px 32px;
    margin: -16px -16px 24px -16px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.header-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        45deg, transparent, transparent 10px,
        rgba(255,255,255,0.03) 10px, rgba(255,255,255,0.03) 20px
    );
}
.header-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    letter-spacing: 4px;
    color: #FFFFFF;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
    margin: 0;
}
.header-subtitle {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    color: var(--emas-muda);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* Banner tutup / di luar jam */
.banner-tutup {
    background: linear-gradient(135deg, #2C2C2C, #1A1A1A);
    border: 2px solid #555;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    margin: 12px 0;
    font-family: 'IBM Plex Mono', monospace;
}
.banner-tutup .icon { font-size: 2.5rem; }
.banner-tutup .judul { font-size: 1.1rem; font-weight: 600; color: var(--emas); margin: 8px 0 4px; }
.banner-tutup .info { font-size: 0.82rem; color: #888; }

/* Kartu loket */
.kartu-loket {
    background: var(--abu-tua);
    border: 1px solid #3A3A3A;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 12px;
    transition: border-color 0.2s;
}
.kartu-loket.aktif { border-color: var(--emas); box-shadow: 0 0 16px rgba(243,156,18,0.12); }
.kartu-loket.kosong { border-color: #333; opacity: 0.7; }

.loket-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
}
.loket-badge {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    background: var(--merah);
    color: white;
    padding: 2px 10px;
    border-radius: 4px;
    letter-spacing: 1px;
}
.loket-nama {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #AAA;
    letter-spacing: 1px;
    flex: 1;
}
.nomor-aktif-loket {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3rem;
    color: var(--emas);
    line-height: 1;
    text-align: center;
    text-shadow: 0 0 16px rgba(243,156,18,0.3);
}
.nama-aktif-loket {
    font-size: 0.9rem;
    font-weight: 600;
    text-align: center;
    margin-top: 4px;
}
.detail-aktif-loket {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #888;
    text-align: center;
    margin-top: 2px;
}

/* Antrian menunggu */
.antrian-item {
    background: var(--abu-tua);
    border: 1px solid #333;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
}
.antrian-item:hover { border-color: var(--emas); }
.nomor-kecil {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    color: var(--merah);
    width: 60px;
    min-width: 60px;
}
.info-pelanggan { flex: 1; }
.nama-kecil { font-weight: 600; font-size: 0.9rem; }
.detail-kecil { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; color: #888; margin-top: 2px; }
.waktu-estimasi { font-family: 'IBM Plex Mono', monospace; font-size: 0.73rem; color: var(--emas); text-align: right; }

/* Stat card */
.stat-card {
    background: var(--abu-tua);
    border-left: 4px solid var(--merah);
    padding: 14px 18px;
    border-radius: 8px;
    margin-bottom: 10px;
}
.stat-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; letter-spacing: 2px; color: #888; text-transform: uppercase; }
.stat-value { font-family: 'Bebas Neue', sans-serif; font-size: 2.2rem; color: var(--emas); line-height: 1.1; }

/* Riwayat */
.riwayat-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 2px;
    color: var(--emas);
    text-transform: uppercase;
    border-bottom: 1px solid #333;
    padding-bottom: 6px;
    margin: 14px 0 8px;
}
.riwayat-item {
    background: var(--abu-tua);
    border-left: 3px solid #555;
    padding: 8px 12px;
    border-radius: 4px;
    margin-bottom: 5px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: #AAA;
}
.riwayat-item.loket-1 { border-left-color: #E74C3C; }
.riwayat-item.loket-2 { border-left-color: #E67E22; }
.riwayat-item.loket-3 { border-left-color: #F1C40F; }
.riwayat-item.loket-4 { border-left-color: #1ABC9C; }
.riwayat-item.loket-5 { border-left-color: #3498DB; }

/* Alert */
.alert-sukses { background:rgba(39,174,96,0.15); border:1px solid #27AE60; border-radius:8px; padding:10px 14px; color:#2ECC71; font-family:'IBM Plex Mono',monospace; font-size:0.83rem; margin:6px 0; }
.alert-info   { background:rgba(52,152,219,0.15); border:1px solid #2980B9; border-radius:8px; padding:10px 14px; color:#5DADE2; font-family:'IBM Plex Mono',monospace; font-size:0.83rem; margin:6px 0; }
.alert-warning{ background:rgba(243,156,18,0.15); border:1px solid var(--emas); border-radius:8px; padding:10px 14px; color:var(--emas); font-family:'IBM Plex Mono',monospace; font-size:0.83rem; margin:6px 0; }

.ticker-bar {
    background: var(--merah-gelap);
    border-top: 1px solid var(--emas);
    border-bottom: 1px solid var(--emas);
    padding: 6px 0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 2px;
    color: var(--emas-muda);
    text-align: center;
    margin: 16px 0;
}
.ticker-tutup {
    background: #2C2C2C;
    border-top: 1px solid #555;
    border-bottom: 1px solid #555;
    padding: 6px 0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 2px;
    color: #888;
    text-align: center;
    margin: 16px 0;
}

.stButton > button {
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    border-radius: 6px !important;
    transition: all 0.2s !important;
}
[data-testid="stSidebar"] { background-color: var(--abu-tua) !important; border-right: 2px solid #333; }
[data-testid="stSidebar"] .stMarkdown { color: var(--putih) !important; }
.stTextInput > div > div > input,
.stSelectbox > div > div > div {
    background-color: var(--abu-tua) !important;
    color: var(--putih) !important;
    border: 1px solid #444 !important;
    border-radius: 6px !important;
}
hr { border-color: var(--merah) !important; opacity: 0.3; }
</style>
""", unsafe_allow_html=True)

# ─── Warna per loket (untuk label) ────────────────────────────────────────────
WARNA_LOKET = {1: "#E74C3C", 2: "#E67E22", 3: "#F1C40F", 4: "#1ABC9C", 5: "#3498DB"}
ICON_LOKET  = {1: "📄", 2: "🔄", 3: "🔑", 4: "🔍", 5: "🚚"}

# ─── Inisialisasi Session State ────────────────────────────────────────────────
if "sistem" not in st.session_state:
    st.session_state.sistem = SistemMultiLoket()
if "audio_path" not in st.session_state:
    st.session_state.audio_path = None

sistem: SistemMultiLoket = st.session_state.sistem

# ─── Cek Jam & Hari Pelayanan ─────────────────────────────────────────────────
layanan_aktif, pesan_status = cek_jam_pelayanan()
info_pelayanan = get_info_pelayanan()

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
    <div class="header-title">🚗 SISTEM ANTRIAN STNK 🚗</div>
    <div class="header-subtitle">Samsat — Pelayanan Perpanjangan Pajak Tahunan Kendaraan Bermotor</div>
</div>
""", unsafe_allow_html=True)

# ─── Ticker Info ──────────────────────────────────────────────────────────────
hari_tanggal = datetime.now().strftime("%A, %d %B %Y")
jam_sekarang = datetime.now().strftime("%H:%M")

if layanan_aktif:
    st.markdown(f"""
    <div class="ticker-bar">
        📅 {hari_tanggal} &nbsp;|&nbsp; 🕐 {jam_sekarang} WIB &nbsp;|&nbsp;
        ✅ JAM PELAYANAN: 08:00 – 16:00 WIB &nbsp;|&nbsp;
        🗓 SENIN – JUMAT &nbsp;|&nbsp; ☎ INFO: 1500-599
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="ticker-tutup">
        📅 {hari_tanggal} &nbsp;|&nbsp; 🕐 {jam_sekarang} WIB &nbsp;|&nbsp;
        ⛔ {pesan_status} &nbsp;|&nbsp;
        🗓 JAM PELAYANAN: SENIN–JUMAT 08:00–16:00 WIB
    </div>
    """, unsafe_allow_html=True)

# ─── Banner Tutup (jika di luar jam/hari) ─────────────────────────────────────
if not layanan_aktif:
    st.markdown(f"""
    <div class="banner-tutup">
        <div class="icon">⛔</div>
        <div class="judul">{pesan_status}</div>
        <div class="info">
            Jam Pelayanan: <strong>Senin – Jumat, 08:00 – 16:00 WIB</strong><br>
            Silakan datang kembali pada hari dan jam pelayanan.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

# ─── Layout Utama (3 Kolom) ───────────────────────────────────────────────────
col_kiri, col_tengah, col_kanan = st.columns([1.2, 1.8, 1.0])

# ══════════════════════════════════════════════════════════════════════
# KOLOM KIRI – Form Pendaftaran & Statistik
# ══════════════════════════════════════════════════════════════════════
with col_kiri:
    st.markdown("### 📋 Daftar Antrian")
    st.markdown("---")

    if not layanan_aktif:
        st.markdown(f'<div class="alert-warning">⛔ {pesan_status}</div>', unsafe_allow_html=True)
        st.markdown('<div class="alert-info">ℹ Pendaftaran hanya dapat dilakukan pada Senin–Jumat pukul 08:00–16:00 WIB.</div>', unsafe_allow_html=True)
    else:
        with st.container():
            nama       = st.text_input("👤 Nama Lengkap", placeholder="Masukkan nama sesuai BPKB...")
            no_polisi  = st.text_input("🚘 Nomor Polisi", placeholder="Contoh: E 1234 AB").upper()
            jenis_layanan = st.selectbox("🔧 Jenis Layanan", DAFTAR_LAYANAN)
            no_hp      = st.text_input("📱 Nomor HP (opsional)", placeholder="08xxxxxxxxxx")

            loket_preview = get_loket(jenis_layanan)
            st.markdown(f"""
            <div style="font-family:'IBM Plex Mono',monospace; font-size:0.75rem;
                        color:{WARNA_LOKET[loket_preview]}; margin-bottom:10px;">
                → Akan dilayani di <strong>Loket {loket_preview}</strong>
                ({ICON_LOKET[loket_preview]} {jenis_layanan})
            </div>
            """, unsafe_allow_html=True)

            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                daftar_btn = st.button("✅ Ambil Nomor", use_container_width=True, type="primary")
            with col_btn2:
                reset_btn = st.button("🔄 Reset Semua", use_container_width=True)

        # Proses pendaftaran
        if daftar_btn:
            if not nama.strip():
                st.markdown('<div class="alert-warning">⚠ Nama tidak boleh kosong!</div>', unsafe_allow_html=True)
            elif not no_polisi.strip():
                st.markdown('<div class="alert-warning">⚠ Nomor polisi tidak boleh kosong!</div>', unsafe_allow_html=True)
            else:
                data_pelanggan = {
                    "nama":           nama.strip().title(),
                    "no_polisi":      no_polisi.strip(),
                    "jenis_layanan":  jenis_layanan,
                    "no_hp":          no_hp.strip() or "-",
                    "waktu_daftar":   format_waktu_sekarang(),
                    "tanggal":        datetime.now().strftime("%d/%m/%Y"),
                }
                nomor = sistem.daftar(data_pelanggan)
                loket = get_loket(jenis_layanan)
                estimasi = get_estimasi_waktu(sistem.antrian[loket].ukuran())

                # TTS konfirmasi
                pesan_tts = buat_pesan_daftar(nomor, nama.strip().title(), estimasi, loket)
                audio_file = generate_audio_file(pesan_tts, f"daftar_{nomor}")
                if audio_file:
                    st.session_state.audio_path = audio_file

                st.markdown(f"""
                <div class="alert-sukses">
                    ✅ Berhasil! Nomor antrian: <strong>{nomor}</strong><br>
                    Loket: <strong>{loket}</strong> — {jenis_layanan}<br>
                    Estimasi tunggu: ~{estimasi} menit
                </div>
                """, unsafe_allow_html=True)
                st.rerun()

    # Reset sistem
    if 'reset_btn' in dir() and reset_btn:
        sistem.reset()
        st.session_state.audio_path = None
        st.rerun()

    # Audio
    if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
        with open(st.session_state.audio_path, "rb") as f:
            st.audio(f.read(), format="audio/mp3", autoplay=True)
        st.session_state.audio_path = None

    # Statistik
    st.markdown("---")
    st.markdown("### 📊 Statistik Hari Ini")
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown(f"""<div class="stat-card">
            <div class="stat-label">Menunggu</div>
            <div class="stat-value">{sistem.total_menunggu()}</div>
        </div>""", unsafe_allow_html=True)
    with col_s2:
        st.markdown(f"""<div class="stat-card" style="border-left-color:#F39C12;">
            <div class="stat-label">Aktif</div>
            <div class="stat-value" style="color:#F39C12;">{sistem.total_aktif()}</div>
        </div>""", unsafe_allow_html=True)
    with col_s3:
        st.markdown(f"""<div class="stat-card" style="border-left-color:#27AE60;">
            <div class="stat-label">Selesai</div>
            <div class="stat-value" style="color:#2ECC71;">{sistem.total_selesai()}</div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# KOLOM TENGAH – Panel Loket (5 Loket)
# ══════════════════════════════════════════════════════════════════════
with col_tengah:
    st.markdown("### 🖥️ Panel Multi-Loket")
    st.markdown("---")

    # Iterasi tiap loket
    for loket in range(1, 6):
        nama_layanan = DAFTAR_LAYANAN[loket - 1]
        warna        = WARNA_LOKET[loket]
        icon         = ICON_LOKET[loket]
        dilayani     = sistem.sedang_dilayani[loket]
        jml_antrian  = sistem.antrian[loket].ukuran()

        kelas_kartu  = "aktif" if dilayani else "kosong"

        # Tampilan kartu loket — header dulu, lalu isi terpisah
        border_color = warna if dilayani else "#3A3A3A"
        st.markdown(f"""
        <div class="kartu-loket {kelas_kartu}" style="border-color:{border_color};">
            <div class="loket-header">
                <span class="loket-badge" style="background:{warna};">LOKET {loket}</span>
                <span class="loket-nama">{icon} {nama_layanan}</span>
                <span style="font-family:'IBM Plex Mono',monospace; font-size:0.68rem; color:#666;">
                    {jml_antrian} antrian
                </span>
            </div>
        """, unsafe_allow_html=True)

        if dilayani:
            st.markdown(f"""
            <div class="nomor-aktif-loket">{dilayani['nomor']}</div>
            <div class="nama-aktif-loket">{dilayani['nama']}</div>
            <div class="detail-aktif-loket">🚘 {dilayani['no_polisi']} &nbsp;|&nbsp; ⏰ {dilayani['waktu_daftar']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="text-align:center; padding:8px 0;">
                <span style="font-family:'Bebas Neue',sans-serif; font-size:2rem; color:#444;">— — —</span><br>
                <span style="font-family:'IBM Plex Mono',monospace; font-size:0.72rem; color:#555;">
                    {jml_antrian} menunggu
                </span>
            </div>
            </div>
            """, unsafe_allow_html=True)

        # Tombol Panggil & Selesai untuk tiap loket
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            panggil_disabled = sistem.antrian[loket].kosong() or dilayani is not None
            if st.button(
                f"📢 Panggil",
                key=f"panggil_{loket}",
                use_container_width=True,
                type="primary",
                disabled=panggil_disabled
            ):
                pelanggan = sistem.panggil(loket)
                if pelanggan:
                    pesan_tts = buat_pesan_panggil(pelanggan["nomor"], pelanggan["nama"], loket)
                    audio_file = generate_audio_file(pesan_tts, f"panggil_{pelanggan['nomor']}")
                    if audio_file:
                        st.session_state.audio_path = audio_file
                    st.rerun()

        with c2:
            selesai_disabled = dilayani is None
            if st.button(
                f"✔ Selesai",
                key=f"selesai_{loket}",
                use_container_width=True,
                disabled=selesai_disabled
            ):
                hasil = sistem.selesai(loket)
                if hasil:
                    pesan_tts = buat_pesan_selesai(hasil["nama"], loket)
                    audio_file = generate_audio_file(pesan_tts, f"selesai_{hasil['nomor']}")
                    if audio_file:
                        st.session_state.audio_path = audio_file
                    st.rerun()

        with c3:
            # Tampilkan antrian menunggu berikutnya di loket ini
            berikutnya = sistem.antrian[loket].peek()
            if berikutnya:
                st.markdown(f"""
                <div style="font-family:'IBM Plex Mono',monospace; font-size:0.7rem;
                            color:#888; padding:6px 0; text-align:center;">
                    Berikutnya:<br>
                    <span style="color:{warna}; font-weight:600;">{berikutnya['nomor']}</span>
                    &nbsp;{berikutnya['nama'][:15]}
                </div>
                """, unsafe_allow_html=True)

        # Audio playback setelah tombol ditekan
        if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
            with open(st.session_state.audio_path, "rb") as f:
                st.audio(f.read(), format="audio/mp3", autoplay=True)
            st.session_state.audio_path = None

        st.markdown('<hr style="margin:6px 0; opacity:0.1;">', unsafe_allow_html=True)

    # ── Daftar Tunggu Per Loket ──
    st.markdown("### 🕐 Daftar Tunggu")
    st.markdown("---")

    ada_antrian = False
    for loket in range(1, 6):
        items = sistem.antrian[loket].lihat_semua()
        if not items:
            continue
        ada_antrian = True
        nama_layanan = DAFTAR_LAYANAN[loket - 1]
        warna = WARNA_LOKET[loket]
        st.markdown(f"""
        <div style="font-family:'IBM Plex Mono',monospace; font-size:0.7rem;
                    color:{warna}; letter-spacing:2px; text-transform:uppercase;
                    border-bottom:1px solid #333; padding-bottom:4px; margin:10px 0 6px;">
            Loket {loket} — {nama_layanan}
        </div>
        """, unsafe_allow_html=True)
        for i, item in enumerate(items):
            estimasi = get_estimasi_waktu(i + 1)
            st.markdown(f"""
            <div class="antrian-item">
                <div class="nomor-kecil" style="color:{warna};">{item['nomor']}</div>
                <div class="info-pelanggan">
                    <div class="nama-kecil">{item['nama']}</div>
                    <div class="detail-kecil">🚘 {item['no_polisi']}</div>
                </div>
                <div class="waktu-estimasi">~{estimasi} mnt</div>
            </div>
            """, unsafe_allow_html=True)

    if not ada_antrian:
        st.markdown('<div class="alert-info">ℹ Semua antrian kosong.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# KOLOM KANAN – Riwayat Per Jenis Layanan & Info Dokumen
# ══════════════════════════════════════════════════════════════════════
with col_kanan:
    st.markdown("### 📜 Riwayat Pelayanan")
    st.markdown("---")

    tab_labels = [f"Loket {l}" for l in range(1, 6)] + ["Semua"]
    tabs = st.tabs(tab_labels)

    for idx, loket in enumerate(range(1, 6)):
        with tabs[idx]:
            nama_layanan = DAFTAR_LAYANAN[loket - 1]
            warna = WARNA_LOKET[loket]
            riwayat_loket = sistem.riwayat[loket]

            st.markdown(f"""
            <div style="font-family:'IBM Plex Mono',monospace; font-size:0.68rem;
                        color:{warna}; letter-spacing:1px; margin-bottom:8px;">
                {ICON_LOKET[loket]} {nama_layanan}
                &nbsp;|&nbsp; {len(riwayat_loket)} selesai
            </div>
            """, unsafe_allow_html=True)

            if not riwayat_loket:
                st.markdown('<div class="alert-info" style="font-size:0.78rem;">Belum ada pelayanan selesai.</div>', unsafe_allow_html=True)
            else:
                for item in reversed(riwayat_loket[-15:]):
                    st.markdown(f"""
                    <div class="riwayat-item loket-{loket}">
                        ✅ [{item['nomor']}] <strong style="color:#DDD;">{item['nama']}</strong><br>
                        🚘 {item['no_polisi']}<br>
                        🕐 Selesai: {item.get('waktu_selesai','—')}
                    </div>
                    """, unsafe_allow_html=True)

    # Tab "Semua"
    with tabs[5]:
        semua = sistem.semua_riwayat()
        if not semua:
            st.markdown('<div class="alert-info" style="font-size:0.78rem;">Belum ada riwayat hari ini.</div>', unsafe_allow_html=True)
        else:
            for item in semua[:20]:
                loket = item.get("loket", 1)
                warna = WARNA_LOKET.get(loket, "#888")
                st.markdown(f"""
                <div class="riwayat-item loket-{loket}">
                    ✅ [{item['nomor']}] <strong style="color:#DDD;">{item['nama']}</strong><br>
                    <span style="color:{warna}; font-size:0.7rem;">{item['jenis_layanan']}</span><br>
                    🕐 {item.get('waktu_selesai','—')}
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Bebas Neue',sans-serif; font-size:1.1rem;
                letter-spacing:2px; color:#F5F5F0; margin-bottom:10px;">
        ℹ️ JAM &amp; HARI PELAYANAN
    </div>
    """, unsafe_allow_html=True)
    status_warna = "#27AE60" if layanan_aktif else "#C0392B"
    status_teks  = "BUKA" if layanan_aktif else "TUTUP"
    st.markdown(f"""
    <div style="font-family:'IBM Plex Mono',monospace; font-size:0.8rem; line-height:2;">
        <span style="color:{status_warna}; font-weight:700;">● {status_teks}</span><br>
        🗓 <b style="color:#F5F5F0;">Senin – Jumat</b><br>
        🕐 <b style="color:#F5F5F0;">08:00 – 16:00 WIB</b><br>
        <span style="color:#666;">Sabtu & Minggu: Libur</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Bebas Neue',sans-serif; font-size:1.1rem;
                letter-spacing:2px; color:#F5F5F0; margin-bottom:10px;">
        📋 INFO NOMOR LOKET
    </div>
    """, unsafe_allow_html=True)
    for loket in range(1, 6):
        warna = WARNA_LOKET[loket]
        nama_layanan = DAFTAR_LAYANAN[loket - 1]
        prefix = PREFIX_MAP[loket]
        st.markdown(f"""
        <div style="font-family:'IBM Plex Mono',monospace; font-size:0.72rem;
                    margin-bottom:6px; padding:8px 12px;
                    border-left:3px solid {warna}; background:#2C2C2C; border-radius:4px;
                    display:flex; align-items:center; gap:8px;">
            <div>
                <span style="color:{warna}; font-weight:700;">Loket {loket}</span>
                &nbsp;<span style="color:#555; font-size:0.65rem;">[{prefix}001–{prefix}999]</span><br>
                <span style="color:#AAA;">{ICON_LOKET[loket]} {nama_layanan}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    # Progress bar kapasitas
    maks_kapasitas = 50
    terisi = sistem.total_menunggu() + sistem.total_selesai() + sistem.total_aktif()
    persen = min(terisi / maks_kapasitas, 1.0)
    warna_bar = "#27AE60" if persen < 0.6 else "#F39C12" if persen < 0.85 else "#C0392B"
    st.markdown(f"""
    <div style="margin-bottom:6px;">
        <span style="font-family:'IBM Plex Mono',monospace; font-size:0.7rem; color:#888;">
            KAPASITAS HARI INI
        </span>
    </div>
    <div style="background:#333; border-radius:4px; height:10px; overflow:hidden;">
        <div style="background:{warna_bar}; width:{persen*100:.0f}%; height:100%; transition:width 0.3s;"></div>
    </div>
    <div style="font-family:'IBM Plex Mono',monospace; font-size:0.7rem; color:#888; margin-top:4px;">
        {terisi} / {maks_kapasitas} total
    </div>
    """, unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; font-family:'IBM Plex Mono',monospace; font-size:0.72rem; color:#555; padding:12px 0;">
    SISTEM ANTRIAN FIFO MULTI-LOKET — PELAYANAN PERPANJANGAN STNK<br>
    Jam Pelayanan: Senin–Jumat 08:00–16:00 WIB &nbsp;|&nbsp; Python + Streamlit + gTTS<br>
    <span style="color:#333;">──────────────────────────────</span>
</div>
""", unsafe_allow_html=True)