# ==============================================================================
# FILE: inventory_service.py (MANAJER / OTAK SISTEM)
# ==============================================================================

# Mengambil referensi class agar Service bisa mengenali jenis objek yang dikelola
from app.models.product import Product
from app.models.base import AbstractTransaction

class InventoryService:
    def __init__(self):
        # --- ENKAPSULASI: PENYIMPANAN DATA PRIVATE ---
        # Menggunakan double underscore (__) agar data tidak bisa diacak-acak dari luar.
        # self.__products: Menggunakan Dictionary {} agar pencarian ID barang sangat cepat.
        self.__products = {}
        
        # self.__transaction_history: List [] untuk menampung semua objek riwayat transaksi.
        self.__transaction_history = [] 

    def exists(self, product_id):
        """Mengecek apakah ID produk ada di dalam sistem."""
        # Fungsi pembantu untuk memvalidasi apakah sebuah barang sudah terdaftar atau belum.
        return product_id in self.__products

    def add_product(self, product):
        """Menambah produk dengan validasi tipe data dan keunikan ID."""
        # 1. VALIDASI TIPE: Memastikan yang dimasukkan benar-benar objek Produk (bukan teks biasa).
        if not isinstance(product, Product):
            raise TypeError("Objek harus berupa instansi dari class Product!")
        
        # 2. VALIDASI ID: Mencegah adanya dua barang dengan ID yang sama (Duplikat).
        if self.exists(product.product_id):
            raise KeyError(f"ID '{product.product_id}' sudah terdaftar!")
            
        # 3. PENYIMPANAN: Memasukkan objek ke dalam dictionary dengan ID sebagai kuncinya.
        self.__products[product.product_id] = product
        
        # Mencatat aktivitas pendaftaran ke dalam log internal produk.
        product.log_action(f"Produk '{product.name}' didaftarkan ke sistem.")

    # --- FITUR UTAMA: EKSEKUSI TRANSAKSI (PENERAPAN POLIMORFISME) ---
    def execute_transaction(self, transaction: AbstractTransaction):
        """
        Menjalankan transaksi (In/Out) tanpa perlu tahu jenis transaksinya.
        Cukup panggil .execute(), maka class transaksi masing-masing yang bekerja.
        """
        # Polimorfisme: .execute() bisa berarti 'Tambah Stok' atau 'Kurang Stok'
        if transaction.execute():
            # Jika transaksi sukses (Gudang gak penuh / Stok cukup), masukkan ke riwayat.
            self.__transaction_history.append(transaction)
            return True
        return False # Transaksi gagal jika validasi di class transaksi tidak lolos

    def get_transaction_history(self):
        """Mengambil semua riwayat transaksi dalam bentuk teks."""
        if not self.__transaction_history:
            return "Belum ada riwayat transaksi."
        
        # Polimorfisme: Memanggil .get_summary() dari setiap objek transaksi di dalam list.
        return [t.get_summary() for t in self.__transaction_history]

    # --- MANAJEMEN DATA PRODUK (UPDATE & DELETE) ---
    def update_product(self, product_id, new_name=None, new_price=None):
        """Memperbarui informasi produk dengan validasi ID."""
        if not self.exists(product_id):
            raise KeyError(f"ID '{product_id}' tidak ditemukan.")
        
        # Mengambil objek produk berdasarkan ID
        p = self.__products[product_id]
        
        # Menggunakan Setter yang ada di class Product untuk mengubah nama
        if new_name: 
            p.name = new_name 
            
        # Menggunakan Setter untuk mengubah harga (aman karena ada validasi angka di setter)
        if new_price is not None: 
            p.price = new_price 
            
        p.log_action(f"Informasi produk {product_id} diperbarui.")

    def delete_product(self, product_id):
        """Menghapus produk dari memori berdasarkan ID."""
        if not self.exists(product_id):
            raise KeyError(f"ID '{product_id}' tidak ditemukan.")
        
        # Menghapus barang dari dictionary menggunakan .pop()
        removed = self.__products.pop(product_id)
        # Menghapus emoji sesuai permintaan agar tampilan terminal bersih
        print(f"Sukses: Produk '{removed.name}' telah dihapus.")

    def get_all_products(self):
        """Mengambil semua objek produk untuk ditampilkan di Menu 2."""
        if not self.__products:
            # Memberi tahu menu utama jika data masih kosong
            raise IndexError("Gagal menampilkan: Belum ada data barang di sistem.")
            
        # Mengubah data dictionary menjadi list agar bisa di-loop di main.py
        return list(self.__products.values())
    
    def get_product_by_id(self, product_id):
        """Mencari objek produk untuk kebutuhan parameter transaksi (Menu 5 & 6)."""
        # Mengembalikan objek utuh (bukan cuma teks) agar bisa dimanipulasi stoknya.
        return self.__products.get(product_id)