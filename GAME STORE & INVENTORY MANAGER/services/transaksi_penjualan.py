from typing import List, Dict, Any
from datetime import datetime
from tabulate import tabulate
from services.inventory_manager import InventoryManager
from models.mixin import PajakMixin

class TransaksiPenjualan(PajakMixin):
    """
    Layanan untuk menangani proses kasir (Point of Sale).
    Mewarisi PajakMixin untuk perhitungan pajak secara otomatis.
    """

    def __init__(self, inventory_manager: InventoryManager):
        # Menerima instance inventory_manager agar sinkron dengan database
        self.__inventory = inventory_manager
        # Keranjang belanja berupa list of dictionary
        self.__keranjang: List[Dict[str, Any]] = []

    def tambah_ke_keranjang(self, kode: str, jumlah: int) -> bool:
        """Memasukkan barang ke keranjang dan memotong stok di inventory."""
        if jumlah <= 0:
            print("[ERROR] Jumlah beli harus lebih dari 0.")
            return False

        barang = self.__inventory.cari_kode(kode)
        if not barang:
            print(f"[ERROR] Barang dengan kode '{kode}' tidak ditemukan.")
            return False
        
        if barang.get_stok() < jumlah:
            print(f"[ERROR] Stok {barang.get_nama()} tidak mencukupi! Sisa stok: {barang.get_stok()}")
            return False

        # Kurangi stok barang secara real-time
        try:
            barang.kurangi_stok(jumlah)
            self.__inventory.simpan_data() # Simpan perubahan stok ke JSON
        except ValueError as e:
            print(f"[ERROR] {e}")
            return False

        # Masukkan ke keranjang
        subtotal = barang.get_harga() * jumlah
        self.__keranjang.append({
            "barang": barang,
            "jumlah": jumlah,
            "subtotal": subtotal
        })
        
        print(f"[SUKSES] {jumlah}x {barang.get_nama()} berhasil ditambahkan ke keranjang.")
        return True

    def cetak_struk(self) -> None:
        """Mencetak struk belanja, menghitung PPN, dan mengosongkan keranjang."""
        if not self.__keranjang:
            print("\n[INFO] Keranjang masih kosong. Belum ada transaksi.\n")
            return

        print("\n====================================================")
        print("             STRUK PEMBELIAN TOKO GAME              ")
        print(f"Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("====================================================")

        data = []
        total_belanja = 0
        for item in self.__keranjang:
            b = item["barang"]
            qty = item["jumlah"]
            sub = item["subtotal"]
            total_belanja += sub
            data.append([b.get_nama(), f"Rp {b.get_harga():,}", qty, f"Rp {sub:,}"])

        # Cetak tabel item yang dibeli
        print(tabulate(data, headers=["Item", "Harga Satuan", "Qty", "Subtotal"], tablefmt="simple"))
        print("----------------------------------------------------")
        
        # Kalkulasi pajak menggunakan method dari PajakMixin
        ppn = self.hitung_ppn(total_belanja)
        total_akhir = self.hitung_harga_dengan_ppn(total_belanja)

        print(f"Total Subtotal : Rp {total_belanja:,}")
        print(f"PPN (11%)      : Rp {int(ppn):,}")
        print("====================================================")
        print(f"TOTAL BAYAR    : Rp {int(total_akhir):,}")
        print("====================================================\n")
        
        # Selesaikan transaksi dengan mengosongkan keranjang
        self.__keranjang.clear()