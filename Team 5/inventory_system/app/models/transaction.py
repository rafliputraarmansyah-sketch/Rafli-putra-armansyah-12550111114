from datetime import datetime 
from app.models.base import AbstractTransaction 
from app.models.product import Product 
from app.models.location import Warehouse 

# --- 1. TRANSAKSI BARANG MASUK ---
class StockInTransaction(AbstractTransaction): 
    def __init__(self, product: Product, quantity: int, location: Warehouse):
        # Simpan data barang, jumlah, dan lokasi secara aman (Private)
        self.__product = product
        self.__quantity = quantity
        self.__location = location
        self.__timestamp = datetime.now() # Catat waktu otomatis

    # Getter: Jendela untuk mengintip data tanpa bisa mengubahnya
    @property
    def product(self): return self.__product
    @property
    def quantity(self): return self.__quantity
    @property
    def location(self): return self.__location

    def execute(self):
        """Logika eksekusi barang masuk."""
        # VALIDASI: Cek apakah gudang masih muat menampung barang baru
        if self.__location.current_count + self.__quantity <= self.__location.capacity:
            # PBO: Tambah stok produk dengan angka positif (+)
            self.__product.add_stock(self.__quantity)
            # Update hitungan barang di lokasi gudang
            self.__location.current_count += self.__quantity 
            return True # Berhasil
        return False # Gagal (Gudang Penuh)

    def get_summary(self):
        """Format laporan untuk menu riwayat MASUK."""
        waktu = self.__timestamp.strftime('%Y-%m-%d %H:%M')
        return f"[{waktu}] MASUK  | {self.__quantity:<3} unit {self.__product.name:<15} -> {self.__location.name}"

# --- 2. TRANSAKSI BARANG KELUAR ---
class StockOutTransaction(AbstractTransaction): 
    def __init__(self, product: Product, quantity: int):
        # Keluar tidak butuh lokasi gudang di skenario ini
        self.__product = product
        self.__quantity = quantity
        self.__timestamp = datetime.now()

    @property
    def product(self): return self.__product
    @property
    def quantity(self): return self.__quantity

    def execute(self):
        """Logika eksekusi barang keluar."""
        # VALIDASI: Cek sisa stok agar tidak kurang saat diambil
        if self.__product.stock >= self.__quantity:
            # PBO: Kurangi stok produk dengan angka negatif (-)
            self.__product.add_stock(-self.__quantity) 
            return True # Berhasil
        return False # Gagal (Stok Kurang)

    def get_summary(self):
        """Format laporan untuk menu riwayat KELUAR."""
        waktu = self.__timestamp.strftime('%Y-%m-%d %H:%M')
        return f"[{waktu}] KELUAR | {self.__quantity:<3} unit {self.__product.name:<15}"