import os
import re
import time
from datetime import datetime
from colorama import *
from pyfiglet import Figlet

from models.konsol_game import KonsolGame
from models.aksesoris_gaming import AksesorisGaming
from models.perangkat_streaming import PerangkatStreaming
from models.figure_game import FigureGame
from models.poster_game import PosterGame
from models.apparel_game import ApparelGame

from services.inventory_manager import InventoryManager
from services.laporan_stok import LaporanStok

init(autoreset=True)

# ==========================================
# FUNGSI BERSIHKAN LAYAR
# ==========================================
def bersihkan_layar():
    """Membersihkan terminal agar tidak menumpuk."""
    os.system('cls' if os.name == 'nt' else 'clear')

# ==========================================
# BANNER
# ==========================================
bersihkan_layar()
judul = Figlet(font="slant")
print(Fore.CYAN + judul.renderText("GAME STORE"))

print(Fore.YELLOW + """
=================================================
🎮 GAME STORE INVENTORY SYSTEM 🎮

Universitas Islam Negeri Sultan Syarif Kasim Riau
Program Studi Teknik Informatika

Kelompok 5 Bixinary:
• Ahmad Farhan Rantisi
• Fitri Khairani Sitorus
• M. Musthofa Masyhur
• Rafli Putra Armansyah
=================================================
""")

# ==========================================
# LOADING
# ==========================================
print(Fore.MAGENTA + "Memulai sistem inventory...", end=" ")
for i in range(6):
    print("🎮", end="", flush=True)
    time.sleep(0.3)
print("\n")

# ==========================================
# DASHBOARD
# ==========================================
waktu = datetime.now()
print(Fore.BLUE + f"""
╔══════════════════════════════════════╗
║          📊 DASHBOARD SISTEM         ║
╠══════════════════════════════════════╣
║ 🟢 Status Sistem : Aktif             ║
║ 🎮 Jenis Sistem  : Game Store        ║
║ 📦 Inventory     : Siap Digunakan    ║
║ 💻 Platform      : Python            ║
║ 🕒 {waktu.strftime("%d-%m-%Y %H:%M:%S")}   ║
╚══════════════════════════════════════╝
""")
input(Fore.YELLOW + "Tekan Enter untuk masuk ke Menu Utama...")

# ==========================================
# OBJECT & MUAT DATA SINKRONISASI
# ==========================================
manager = InventoryManager()
laporan = LaporanStok(manager)

# Rekonstruksi data mentah JSON ke bentuk Objek Class agar bisa masuk ke daftar_barang
data_mentah = manager.muat_data()
if data_mentah:
    for item in data_mentah:
        kode = item.get("kode")
        nama = item.get("nama")
        harga = item.get("harga")
        stok = item.get("stok")
        jenis = item.get("jenis")
        
        barang_obj = None
        if jenis == "KonsolGame":
            barang_obj = KonsolGame(kode, nama, harga, stok, "-", 0, "-", "-")
        elif jenis == "AksesorisGaming":
            barang_obj = AksesorisGaming(kode, nama, harga, stok, "-", 0, "-", "-")
        elif jenis == "PerangkatStreaming":
            barang_obj = PerangkatStreaming(kode, nama, harga, stok, "-", 0, "-", "-")
        elif jenis == "FigureGame":
            barang_obj = FigureGame(kode, nama, harga, stok, "-", "-", "-", "-")
        elif jenis == "PosterGame":
            barang_obj = PosterGame(kode, nama, harga, stok, "-", "-", "-", "-")
        elif jenis == "ApparelGame":
            barang_obj = ApparelGame(kode, nama, harga, stok, "-", "-", "-", "-")
            
        if barang_obj:
            manager.get_daftar_barang().append(barang_obj)

# ==========================================
# VALIDASI
# ==========================================
def input_kode():
    pola = r"^(KG|AG|PS|FG|PG|AP)[0-9]{3}$"
    while True:
        kode = input("Kode Barang : ").upper().strip()
        if re.match(pola, kode):
            return kode
        print("""
FORMAT SALAH
KG001 = Konsol      FG001 = Figure
AG001 = Aksesoris   PG001 = Poster
PS001 = Streaming   AP001 = Apparel
""")


def input_teks(pesan):
    while True:
        data = input(pesan).strip()
        if data == "":
            print("Input kosong")
            continue
        if any(x.isalpha() for x in data):
            return data
        print("Masukkan teks")


def input_angka(pesan):
    while True:
        try:
            nilai = int(input(pesan))
            if nilai < 0:
                print("Tidak boleh negatif")
                continue
            return nilai
        except ValueError:
            print("Masukkan angka")


# ==========================================
# PROGRAM UTAMA
# ==========================================
while True:
    bersihkan_layar()  # Membersihkan layar setiap kali menu dipanggil
    print("""
╔══════════════════════════════════════╗
║          🎮 GAME STORE MENU 🎮       ║
╠══════════════════════════════════════╣
║ 1. Tambah Barang                     ║
║ 2. Hapus Barang                      ║
║ 3. Update Barang                     ║
║ 4. Cari Barang                       ║
║ 5. Tampilkan Semua                   ║
║ 6. Laporan Stok                      ║
║ 0. Keluar                            ║
╚══════════════════════════════════════╝
""")

    pilihan = input("Pilih menu : ").strip()

    # ======================================
    # 1. TAMBAH BARANG
    # ======================================
    if pilihan == "1":
        print("""
1. Konsol    (KODE: KG001)   4. Figure  (KODE: FG001)
2. Aksesoris (KODE: AG001)   5. Poster  (KODE: PG001)
3. Streaming (KODE: PS001)   6. Apparel (KODE: AP001)
""")
        sub = input("Pilih kategori : ").strip()
        if sub not in ["1", "2", "3", "4", "5", "6"]:
            print(Fore.RED + "\n[ERROR] Kategori tidak valid!\n")
            input(Fore.YELLOW + "Tekan Enter untuk kembali...")
            continue

        kode = input_kode()
        if manager.kode_sudah_ada(kode):
            print(Fore.RED + "\n[ERROR] Kode sudah dipakai\n")
            input(Fore.YELLOW + "Tekan Enter untuk kembali...")
            continue

        nama = input_teks("Nama : ")
        harga = input_angka("Harga : ")
        stok = input_angka("Stok : ")
        barang = None

        # KONSOL
        if sub == "1":
            merek = input_teks("Merek : ")
            garansi = input_angka("Garansi (Bulan) : ")
            tipe = input_teks("Tipe : ")
            storage = input_teks("Gudang : ")
            barang = KonsolGame(kode, nama, harga, stok, merek, garansi, tipe, storage)

        # AKSESORIS
        elif sub == "2":
            merek = input_teks("Merek : ")
            garansi = input_angka("Garansi (Bulan) : ")
            jenis = input_teks("Jenis : ")
            kompatibel = input_teks("Kompatibel : ")
            barang = AksesorisGaming(kode, nama, harga, stok, merek, garansi, jenis, kompatibel)

        # STREAMING
        elif sub == "3":
            merek = input_teks("Merek : ")
            garansi = input_angka("Garansi (Bulan) : ")
            resolusi = input_teks("Resolusi : ")
            koneksi = input_teks("Koneksi : ")
            barang = PerangkatStreaming(kode, nama, harga, stok, merek, garansi, resolusi, koneksi)

        # FIGURE
        elif sub == "4":
            bahan = input_teks("Bahan : ")
            asal = input_teks("Asal : ")
            karakter = input_teks("Karakter : ")
            skala = input_teks("Skala : ")
            barang = FigureGame(kode, nama, harga, stok, bahan, asal, karakter, skala)

        # POSTER
        elif sub == "5":
            bahan = input_teks("Bahan : ")
            asal = input_teks("Asal : ")
            ukuran = input_teks("Ukuran : ")
            kertas = input_teks("Jenis Kertas : ")
            barang = PosterGame(kode, nama, harga, stok, bahan, asal, ukuran, kertas)

        # APPAREL
        elif sub == "6":
            bahan = input_teks("Bahan : ")
            asal = input_teks("Asal : ")
            ukuran = input_teks("Ukuran : ")
            usia = input_teks("Kategori Usia : ")
            barang = ApparelGame(kode, nama, harga, stok, bahan, asal, ukuran, usia)

        if barang:
            manager.tambah_barang(barang)
            print(Fore.GREEN + f"\n[SUKSES] {nama} berhasil dimasukkan ke inventory!\n")
            
        input(Fore.YELLOW + "Tekan Enter untuk kembali ke Menu Utama...")

    # ======================================
    # 2. HAPUS BARANG
    # ======================================
    elif pilihan == "2":
        print(Fore.YELLOW + "\n--- MENU HAPUS BARANG ---")
        kode = input_kode()
        if manager.hapus_barang(kode):
            print(Fore.GREEN + f"\n[SUKSES] Barang dengan kode {kode} telah dihapus.\n")
        else:
            print(Fore.RED + f"\n[ERROR] Kode {kode} tidak ditemukan di sistem.\n")
            
        input(Fore.YELLOW + "Tekan Enter untuk kembali ke Menu Utama...")

    # ======================================
    # 3. UPDATE BARANG
    # ======================================
    elif pilihan == "3":
        print(Fore.YELLOW + "\n--- MENU UPDATE BARANG ---")
        kode = input_kode()
        barang_ditemukan = manager.cari_kode(kode)
        
        if barang_ditemukan:
            print(Fore.BLUE + f"\nData saat ini -> Nama: {barang_ditemukan.get_nama()} | Harga: {barang_ditemukan.get_harga()} | Stok: {barang_ditemukan.get_stok()}")
            print("*(Kosongkan/Tekan Enter langsung jika tidak ingin mengubah data tersebut)*\n")
            
            nama_baru = input("Nama Baru : ").strip()
            if nama_baru == "":
                nama_baru = None
                
            harga_in = input("Harga Baru : ").strip()
            harga_baru = int(harga_in) if (harga_in.isdigit() and int(harga_in) >= 0) else None
            
            stok_in = input("Stok Baru : ").strip()
            stok_baru = int(stok_in) if (stok_in.isdigit() and int(stok_in) >= 0) else None
            
            if manager.ubah_data_barang(kode, nama_baru, harga_baru, stok_baru):
                print(Fore.GREEN + "\n[SUKSES] Data barang berhasil diperbarui!\n")
        else:
            print(Fore.RED + f"\n[ERROR] Barang dengan kode {kode} tidak ditemukan.\n")
            
        input(Fore.YELLOW + "Tekan Enter untuk kembali ke Menu Utama...")

    # ======================================
    # 4. CARI BARANG
    # ======================================
    elif pilihan == "4":
        print(Fore.YELLOW + "\n--- MENU PENCARIAN BARANG ---")
        keyword = input("Masukkan Nama / Kode Barang: ").strip()
        hasil = manager.cari_barang(keyword)
        
        if hasil:
            print(Fore.GREEN + f"\n[INFO] Ditemukan {len(hasil)} item cocok:")
            for b in hasil:
                print(b.info_barang())
        else:
            print(Fore.RED + f"\n[INFO] Tidak ada barang dengan keyword '{keyword}'.\n")
            
        input(Fore.YELLOW + "Tekan Enter untuk kembali ke Menu Utama...")

    # ======================================
    # 5. TAMPILKAN SEMUA
    # ======================================
    elif pilihan == "5":
        print(Fore.YELLOW + "\n--- SELURUH DATA INVENTARIS TOKO ---")
        manager.tampil_semua()
        input(Fore.YELLOW + "Tekan Enter untuk kembali ke Menu Utama...")

    # ======================================
    # 6. LAPORAN STOK
    # ======================================
    elif pilihan == "6":
        while True:
            bersihkan_layar()
            print("""
╔══════════════════════════════════════╗
║         📊 SELEKSI LAPORAN STOK      ║
╠══════════════════════════════════════╣
║ 1. Laporan Barang Habis (Stok 0)     ║
║ 2. Laporan Barang Menipis            ║
║ 3. Laporan Spesifik Per Kategori     ║
║ 0. Kembali ke Menu Utama             ║
╚══════════════════════════════════════╝
""")
            pilihan_lap = input("Pilih tipe laporan : ").strip()
            
            if pilihan_lap == "1":
                laporan.laporan_stok_habis()
                input(Fore.YELLOW + "Tekan Enter untuk kembali...")
            elif pilihan_lap == "2":
                batas = input_angka("Masukkan batas minimum stok (Contoh: 5): ")
                laporan.laporan_stok_menipis(batas)
                input(Fore.YELLOW + "Tekan Enter untuk kembali...")
            elif pilihan_lap == "3":
                print("\nPilihan Valid: KonsolGame, AksesorisGaming, PerangkatStreaming, FigureGame, PosterGame, ApparelGame")
                kategori = input("Ketik nama kategori (Persis): ").strip()
                laporan.laporan_per_kategori(kategori)
                input(Fore.YELLOW + "Tekan Enter untuk kembali...")
            elif pilihan_lap == "0":
                break
            else:
                print(Fore.RED + "\nMenu laporan tidak valid.\n")
                input(Fore.YELLOW + "Tekan Enter untuk mencoba lagi...")

    # ======================================
    # 0. KELUAR
    # ======================================
    elif pilihan == "0":
        print(Fore.GREEN + "\nSistem dinonaktifkan. Terima kasih telah menggunakan Game Store Inventory System!\n")
        break
        
    else:
        print(Fore.RED + "\nPilihan menu salah. Silakan coba lagi.\n")
        input(Fore.YELLOW + "Tekan Enter untuk mencoba lagi...")