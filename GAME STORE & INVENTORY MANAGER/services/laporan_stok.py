from typing import List
from tabulate import tabulate
from services.inventory_manager import InventoryManager
from models.base import Barang

class LaporanStok:
    """Layanan untuk mencetak berbagai laporan terkait ketersediaan stok barang."""

    def __init__(self, inventory_manager: InventoryManager):
        """
        Dependency Injection: Menerima objek InventoryManager yang sudah ada 
        agar laporan selalu mengambil data terbaru.
        """
        self.__inventory = inventory_manager

    def __cetak_tabel(self, judul: str, daftar_barang: List[Barang]) -> None:
        """Method private (internal) untuk mencetak tabel dengan format konsisten."""
        print(f"\n=== {judul.upper()} ===")
        if not daftar_barang:
            print("[INFO] Tidak ada data yang sesuai kriteria.\n")
            return
        
        data = []
        for barang in daftar_barang:
            data.append([
                barang.get_kode(),
                barang.get_nama(),
                type(barang).__name__,  # Mengambil nama kelas sebagai Kategori
                barang.get_stok()
            ])
        
        # tablefmt="grid" memberikan tampilan tabel yang tegas dan rapi
        print(tabulate(data, headers=["Kode", "Nama", "Kategori", "Stok"], tablefmt="grid"))
        print()

    # ==========================
    # FITUR LAPORAN
    # ==========================
    def laporan_stok_habis(self) -> None:
        """Menampilkan daftar barang yang stoknya sudah 0."""
        # Menggunakan List Comprehension agar ringkas dan cepat (standar profesional)
        barang_habis = [b for b in self.__inventory.get_daftar_barang() if b.get_stok() == 0]
        self.__cetak_tabel("Laporan Barang Habis", barang_habis)

    def laporan_stok_menipis(self, batas_stok: int = 5) -> None:
        """Menampilkan daftar barang yang stoknya di ambang batas minimum."""
        barang_menipis = [b for b in self.__inventory.get_daftar_barang() if 0 < b.get_stok() <= batas_stok]
        self.__cetak_tabel(f"Laporan Barang Menipis (Stok <= {batas_stok})", barang_menipis)

    def laporan_per_kategori(self, nama_kategori: str) -> None:
        """Menampilkan daftar barang berdasarkan jenis/kategori (nama class)."""
        barang_kategori = [
            b for b in self.__inventory.get_daftar_barang() 
            if type(b).__name__.lower() == nama_kategori.lower()
        ]
        self.__cetak_tabel(f"Laporan Kategori: {nama_kategori.capitalize()}", barang_kategori)