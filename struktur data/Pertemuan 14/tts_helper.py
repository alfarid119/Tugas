"""
╔══════════════════════════════════════════════════════════════════╗
║         MODUL TEXT-TO-SPEECH (TTS) — gTTS Helper               ║
║         Mengubah teks pengumuman antrian menjadi suara          ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import tempfile
from typing import Optional


AUDIO_DIR = tempfile.gettempdir()


def generate_audio_file(teks: str, nama_file: str = "antrian") -> Optional[str]:
    """Menghasilkan file audio MP3 dari teks menggunakan gTTS."""
    try:
        from gtts import gTTS
        nama_bersih = "".join(c for c in nama_file if c.isalnum() or c in "_-")
        output_path = os.path.join(AUDIO_DIR, f"{nama_bersih}.mp3")
        tts = gTTS(text=teks, lang="id", slow=False)
        tts.save(output_path)
        return output_path
    except ImportError:
        print("[TTS] gTTS tidak terinstall. Jalankan: pip install gtts")
        return None
    except Exception as e:
        print(f"[TTS] Gagal membuat audio: {e}")
        return None


def speak_text(teks: str) -> bool:
    """Mengucapkan teks (untuk mode console)."""
    audio_file = generate_audio_file(teks, "temp_speak")
    if not audio_file:
        print(f"[SUARA] {teks}")
        return False

    try:
        try:
            from playsound import playsound
            playsound(audio_file)
            return True
        except ImportError:
            pass

        try:
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            return True
        except ImportError:
            pass

        if os.name != "nt":
            os.system(f'mpg123 -q "{audio_file}" 2>/dev/null || '
                      f'ffplay -nodisp -autoexit "{audio_file}" 2>/dev/null')
            return True

        print(f"[SUARA] {teks}")
        return False

    except Exception as e:
        print(f"[TTS] Error saat memutar audio: {e}")
        print(f"[SUARA] {teks}")
        return False


def buat_pesan_panggil(nomor: str, nama: str, loket: int = 1) -> str:
    """
    Membuat teks pengumuman pemanggilan antrian.
    Menyebutkan nomor loket yang spesifik sesuai jenis layanan.
    """
    return (
        f"Perhatian. "
        f"Nomor antrian {nomor}, "
        f"atas nama {nama}, "
        f"dimohon segera menuju loket {loket}. "
        f"Terima kasih."
    )


def buat_pesan_daftar(nomor: str, nama: str, estimasi_menit: int, loket: int = 1) -> str:
    """Membuat teks konfirmasi pendaftaran antrian dengan info loket."""
    return (
        f"Selamat datang, {nama}. "
        f"Nomor antrian Anda adalah {nomor}, "
        f"untuk loket {loket}. "
        f"Estimasi waktu tunggu sekitar {estimasi_menit} menit. "
        f"Mohon menunggu di ruang tunggu yang telah disediakan."
    )


def buat_pesan_selesai(nama: str, loket: int = 1) -> str:
    """Membuat teks pengumuman selesai dilayani."""
    return (
        f"Pelayanan atas nama {nama} di loket {loket} telah selesai. "
        f"Terima kasih telah menggunakan layanan Samsat. "
        f"Semoga harimu menyenangkan."
    )


def hapus_file_audio_lama(maks_file: int = 20) -> None:
    """Membersihkan file audio lama dari direktori temp."""
    try:
        files = [
            os.path.join(AUDIO_DIR, f)
            for f in os.listdir(AUDIO_DIR)
            if f.endswith(".mp3") and f.startswith(("daftar_", "panggil_", "selesai_"))
        ]
        files.sort(key=os.path.getmtime)
        while len(files) > maks_file:
            os.remove(files.pop(0))
    except Exception:
        pass


if __name__ == "__main__":
    print("Testing gTTS helper...")
    pesan = buat_pesan_panggil("A001", "Budi Santoso", loket=1)
    print(f"Pesan: {pesan}")
    audio = generate_audio_file(pesan, "test_panggil")
    if audio:
        print(f"✅ File audio dibuat: {audio}")
    else:
        print("❌ Gagal membuat audio (pastikan gTTS terinstall)")