from typing import List, Optional, Dict, Any
from tabulate import tabulate
from data.database import Database
from models.base import Barang

class InventoryManager:
    """Manajer utama untuk operasi CRUD pada daftar inventaris toko game."""

    def __init__(self):
        self.__daftar_barang: List[Barang] = []
        self.__database = Database()

    # ==========================
    # GET DATA BARANG
    # ==========================
    def get_daftar_barang(self) -> List[Barang]:
        return self.__daftar_barang

    # ==========================
    # SIMPAN & MUAT DATA JSON
    # ==========================
    def simpan_data(self) -> None:
        """Menyimpan list objek barang ke dalam bentuk JSON."""
        data = []
        for barang in self.__daftar_barang:
            data.append({
                "kode": barang.get_kode(),
                "nama": barang.get_nama(),
                "harga": barang.get_harga(),
                "stok": barang.get_stok(),
                "jenis": type(barang).__name__
            })
        self.__database.simpan_ke_berkas(data)

    def muat_data(self) -> List[Dict[str, Any]]:
        """Memuat data mentah dari database JSON."""
        return self.__database.muat_dari_berkas()

    # ==========================
    # TAMBAH BARANG
    # ==========================
    def tambah_barang(self, barang: Barang) -> None:
        self.__daftar_barang.append(barang)
        self.simpan_data()

    # ==========================
    # VALIDASI & PENCARIAN
    # ==========================
    def kode_sudah_ada(self, kode: str) -> bool:
        """Mengecek apakah kode barang duplikat."""
        for barang in self.__daftar_barang:
            if barang.get_kode() == kode:
                return True
        return False

    def cari_kode(self, kode: str) -> Optional[Barang]:
        """Mencari objek barang berdasarkan kode unik."""
        for barang in self.__daftar_barang:
            if barang.get_kode() == kode:
                return barang
        return None

    def cari_barang(self, keyword: str) -> List[Barang]:
        """Mencari barang berdasarkan potongan teks pada kode atau nama."""
        hasil = []
        keyword = keyword.lower().strip()
        for barang in self.__daftar_barang:
            if (keyword in barang.get_kode().lower()) or (keyword in barang.get_nama().lower()):
                hasil.append(barang)
        return hasil

    # ==========================
    # UPDATE & DELETE
    # ==========================
    def hapus_barang(self, kode: str) -> bool:
        barang = self.cari_kode(kode)
        if barang:
            self.__daftar_barang.remove(barang)
            self.simpan_data()
            return True
        return False

    def ubah_data_barang(self, kode: str, nama_baru: str = None, 
                        harga_baru: int = None, stok_baru: int = None) -> bool:
        barang = self.cari_kode(kode)
        if barang:
            if nama_baru is not None:
                barang.set_nama(nama_baru)
            if harga_baru is not None:
                barang.set_harga(harga_baru)
            if stok_baru is not None:
                barang.set_stok(stok_baru)
            self.simpan_data()
            return True
        return False

    # ==========================
    # TAMPIL SEMUA (TABEL & STATISTIK)
    # ==========================
    def tampil_semua(self) -> None:
        """Mencetak daftar inventaris dan statistik ke layar console."""
        if len(self.__daftar_barang) == 0:
            print("\n[INFO] Inventory kosong\n")
            return

        data = []
        for barang in self.__daftar_barang:
            data.append([
                barang.get_kode(),
                barang.get_nama(),
                f"Rp {barang.get_harga():,}",
                barang.get_stok()
            ])

        print(tabulate(data, headers=["Kode", "Nama", "Harga", "Stok"], tablefmt="fancy_grid"))

        total_barang = len(self.__daftar_barang)
        total_stok = sum(barang.get_stok() for barang in self.__daftar_barang)
        total_nilai = sum(barang.get_harga() * barang.get_stok() for barang in self.__daftar_barang)

        print(f"""
====================================
📊 STATISTIK INVENTORY
====================================
🎮 Total Jenis Barang : {total_barang}
📦 Total Stok         : {total_stok}
💰 Total Nilai Aset   : Rp {total_nilai:,}
====================================
""")

        ranking = sorted(self.__daftar_barang, key=lambda x: x.get_stok(), reverse=True)
        print("\n🏆 RANKING STOK TERBANYAK\n")
        for nomor, barang in enumerate(ranking, start=1):
            print(f"{nomor}. {barang.get_nama()} → {barang.get_stok()} pcs")