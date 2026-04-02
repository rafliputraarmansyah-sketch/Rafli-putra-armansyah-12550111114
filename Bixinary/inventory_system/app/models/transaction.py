from datetime import datetime 
from app.models.base import AbstractTransaction 
from app.models.product import Product 
from app.models.location import Warehouse 

# --- 1. TRANSAKSI BARANG MASUK (RESTOCK DARI SUPPLIER) ---
# Logika: Menangani alur masuknya barang baru ke dalam sistem agar stok dan gudang sinkron.
class StockInTransaction(AbstractTransaction): 
    def __init__(self, product: Product, quantity: int, location: Warehouse):
        # Logika: Mengikat objek produk dan lokasi asli ke dalam transaksi ini.
        # Simpan data barang, jumlah, dan lokasi secara aman (Private)
        self.__product = product
        self.__quantity = quantity
        self.__location = location
        self.__timestamp = datetime.now() # Logika: Mencatat waktu kejadian secara otomatis.

    @property
    def product(self): return self.__product
    @property
    def quantity(self): return self.__quantity
    @property
    def location(self): return self.__location

    def execute(self):
        """Logika eksekusi barang masuk ke gudang/rak."""
        # VALIDASI: Logika 'Gerbang Keamanan'. Cek apakah gudang masih muat sebelum barang dimasukkan.
        if self.__location.current_count + self.__quantity <= self.__location.capacity:
            # 1. Tambah stok di objek Produk
            # Logika: Memperbarui data jumlah barang yang tersedia di katalog.
            self.__product.add_stock(self.__quantity)
            
            # 2. Update hitungan di objek Lokasi menggunakan helper yang baru kita buat
            # Logika: Memperbarui data okupansi fisik gudang agar sistem tahu gudang makin penuh.
            self.__location.update_stock_count(self.__quantity) 
            return True # Transaksi sukses
        return False # Transaksi gagal karena gudang penuh

    def get_summary(self):
        # Logika: Menghasilkan string laporan yang rapi untuk keperluan audit atau log sistem.
        waktu = self.__timestamp.strftime('%Y-%m-%d %H:%M')
        return f"[{waktu}] RESTOCK | {self.__quantity:<3} unit {self.__product.name:<15} -> {self.__location.name}"


# --- 2. TRANSAKSI BARANG KELUAR (NON-PENJUALAN: RUSAK/KADALUARSA) ---
# Logika: Menangani pengurangan stok yang bukan karena pembeli (misal: barang pecah atau hilang).
class StockOutTransaction(AbstractTransaction): 
    def __init__(self, product: Product, quantity: int, location: Warehouse, reason: str = "Lainnya"):
        """
        Sekarang butuh Lokasi dan Alasan agar laporan inventaris sinkron.
        reason: Misal 'Rusak', 'Hilang', atau 'Kadaluarsa'.
        """
        self.__product = product
        self.__quantity = quantity
        self.__location = location
        self.__reason = reason
        self.__timestamp = datetime.now()

    @property
    def product(self): return self.__product
    @property
    def quantity(self): return self.__quantity

    def execute(self):
        """Logika eksekusi barang keluar gudang (bukan lewat kasir)."""
        # VALIDASI: Logika 'Cek Saldo'. Memastikan barang yang mau dikeluarkan memang ada stoknya.
        if self.__product.stock >= self.__quantity:
            # 1. Kurangi stok di objek Produk
            # Logika: Mengurangi jumlah barang di katalog.
            self.__product.add_stock(-self.__quantity) 
            
            # 2. Kurangi hitungan di objek Lokasi
            # Logika: Memberi ruang kosong kembali di gudang/rak karena barang sudah dikeluarkan.
            self.__location.update_stock_count(-self.__quantity)
            return True 
        return False # Gagal jika stok produk tidak mencukupi

    def get_summary(self):
        # Logika: Memberikan alasan yang jelas kenapa stok berkurang agar admin tidak bingung saat audit.
        waktu = self.__timestamp.strftime('%Y-%m-%d %H:%M')
        # Menampilkan alasan kenapa stok berkurang (sangat disukai dosen)
        return f"[{waktu}] ADJUST  | {self.__quantity:<3} unit {self.__product.name:<15} | Ket: {self.__reason}"