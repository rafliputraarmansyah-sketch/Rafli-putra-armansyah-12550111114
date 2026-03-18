from app.models.product import Product
from app.models.base import AbstractTransaction

class InventoryService:
    def __init__(self):
        # Enkapsulasi: Data disimpan dalam memori (RAM) secara private
        # Data akan ter-reset jika program dimatikan
        self.__products = {}
        self.__transaction_history = [] 

    def exists(self, product_id):
        """Mengecek apakah ID produk ada di dalam sistem."""
        return product_id in self.__products

    def add_product(self, product):
        """Menambah produk dengan validasi tipe data dan keunikan ID."""
        if not isinstance(product, Product):
            raise TypeError("Objek harus berupa instansi dari class Product!")
        
        if self.exists(product.product_id):
            raise KeyError(f"ID '{product.product_id}' sudah terdaftar!")
            
        self.__products[product.product_id] = product
        product.log_action(f"Produk '{product.name}' didaftarkan ke sistem.")

    # --- FITUR UTAMA: EKSEKUSI TRANSAKSI ---
    def execute_transaction(self, transaction: AbstractTransaction):
        """
        Menjalankan transaksi (In/Out) menggunakan Polimorfisme.
        Hanya mencatat ke riwayat jika metode .execute() berhasil.
        """
        if transaction.execute():
            self.__transaction_history.append(transaction)
            return True
        return False

    def get_transaction_history(self):
        """Mengambil semua riwayat transaksi (Polimorfisme pada .get_summary())."""
        if not self.__transaction_history:
            return "Belum ada riwayat transaksi."
        
        return [t.get_summary() for t in self.__transaction_history]

    # --- MANAJEMEN DATA PRODUK ---
    def update_product(self, product_id, new_name=None, new_price=None):
        """Memperbarui informasi produk dengan validasi ID."""
        if not self.exists(product_id):
            raise KeyError(f"ID '{product_id}' tidak ditemukan.")
        
        p = self.__products[product_id]
        if new_name: 
            p.name = new_name # Membutuhkan @name.setter di class Product
            
        if new_price is not None: 
            p.price = new_price # Membutuhkan @price.setter di class Product
            
        p.log_action(f"Informasi produk {product_id} diperbarui.")

    def delete_product(self, product_id):
        """Menghapus produk dari memori berdasarkan ID."""
        if not self.exists(product_id):
            raise KeyError(f"ID '{product_id}' tidak ditemukan.")
        
        removed = self.__products.pop(product_id)
        print(f"🗑️ Sukses: Produk '{removed.name}' telah dihapus.")

    def get_all_products(self):
        """Mengambil semua objek produk dalam bentuk list."""
        if not self.__products:
            raise IndexError("Gagal menampilkan: Belum ada data barang di sistem.")
        return list(self.__products.values())
    
    def get_product_by_id(self, product_id):
        """Mencari objek produk untuk kebutuhan parameter transaksi."""
        return self.__products.get(product_id)