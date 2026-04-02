from app.models.product import Product
from app.models.base import AbstractTransaction

# Logika: InventoryService bertindak sebagai 'Otak' yang mengelola seluruh database barang dan riwayat gudang.
class InventoryService:
    def __init__(self):
        # --- ENKAPSULASI: PENYIMPANAN DATA PRIVATE ---
        # Logika: Menggunakan dictionary agar pencarian barang berdasarkan ID bisa dilakukan secepat kilat (O(1)).
        self.__products = {}
        # Logika: List untuk menampung semua bukti transaksi resmi dari supplier atau penyesuaian stok.
        self.__transaction_history = [] 

    def exists(self, product_id):
        # Logika: Fungsi pembantu untuk mengecek apakah sebuah ID barang sudah ada di rak/database.
        return product_id in self.__products

    def add_product(self, product):
        # Logika: 'Pintu Masuk' pendaftaran barang baru. 
        # Melakukan validasi tipe data agar tidak ada objek asing yang masuk ke sistem.
        if not isinstance(product, Product):
            raise TypeError("Objek harus berupa instansi dari class Product!")
        
        # Logika: Mencegah adanya dua barang dengan ID yang sama (duplikasi ID).
        if self.exists(product.product_id):
            raise KeyError(f"ID '{product.product_id}' sudah terdaftar!")
            
        self.__products[product.product_id] = product
        # Logika: Mencatat aksi ke log produk tersebut sebagai bukti pendaftaran berhasil.
        product.log_action(f"Produk '{product.name}' didaftarkan ke sistem.")

    # --- FITUR KHUSUS SWALAYAN: SINKRONISASI PENJUALAN ---
    def record_sale(self, cart_items):
        """
        Menerima keranjang belanja dan memotong stok di sistem.
        PENTING: Pastikan logika potong stok di payment.py dihapus jika pakai ini, 
        agar stok tidak berkurang dua kali!
        """
        # Logika: Menghubungkan transaksi kasir dengan database stok. 
        # Setiap barang di keranjang akan otomatis dikurangi jumlahnya di database pusat.
        for product, qty in cart_items:
            product.add_stock(-qty)
            product.log_action(f"TRANSAKSI KASIR: Terjual {qty} unit.")
        
        print(f"[SISTEM] Inventaris diperbarui: {len(cart_items)} jenis barang terjual.")

    # --- FITUR MANAJER: LAPORAN NILAI ASET (BARU) ---
    def get_inventory_report(self):
        """Menghitung total nilai rupiah dari seluruh stok yang ada di swalayan."""
        # Logika: Menghitung total kekayaan swalayan berdasarkan nilai barang yang ada di gudang/rak saat ini.
        total_aset = 0
        for p in self.__products.values():
            # Menggunakan logika (Harga x Stok)
            total_aset += p.price * p.stock
            
        return f"\n[LAPORAN MANAJER]\nTotal Nilai Barang di Rak: Rp{total_aset:,.0f}"

    # --- FITUR UTAMA: EKSEKUSI TRANSAKSI (GUDANG/RESTOCK) ---
    def execute_transaction(self, transaction: AbstractTransaction):
        # Logika: Menjalankan perintah transaksi (StockIn/StockOut). 
        # Jika eksekusi berhasil (misal: gudang muat), barulah transaksi dicatat ke riwayat.
        if transaction.execute():
            self.__transaction_history.append(transaction)
            return True
        return False

    def get_transaction_history(self):
        # Logika: Mengambil semua ringkasan transaksi untuk ditampilkan sebagai laporan audit.
        if not self.__transaction_history:
            return "Belum ada riwayat transaksi masuk/keluar gudang."
        return [t.get_summary() for t in self.__transaction_history]

    # --- MANAJEMEN DATA PRODUK ---
    def update_product(self, product_id, new_name=None, new_price=None):
        # Logika: Mengubah data barang yang sudah ada. Menggunakan Setter agar validasi di kelas Product tetap berjalan.
        if not self.exists(product_id):
            raise KeyError(f"ID '{product_id}' tidak ditemukan.")
        
        p = self.__products[product_id]
        if new_name: p.name = new_name 
        if new_price is not None: p.price = new_price 
        p.log_action(f"Informasi produk {product_id} diperbarui.")

    def delete_product(self, product_id):
        # Logika: Menghapus barang dari sistem secara permanen.
        if not self.exists(product_id):
            raise KeyError(f"ID '{product_id}' tidak ditemukan.")
        removed = self.__products.pop(product_id)
        print(f"Sukses: Produk '{removed.name}' telah dihapus.")

    def get_all_products(self):
        # Logika: Menampilkan daftar seluruh barang. Melempar error jika sistem masih kosong.
        if not self.__products:
            raise IndexError("Gagal menampilkan: Belum ada data barang di sistem.")
        return list(self.__products.values())
    
    def get_product_by_id(self, product_id):
        # Logika: Mencari satu barang secara spesifik berdasarkan ID-nya.
        return self.__products.get(product_id)