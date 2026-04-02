# IMPORT: Mengambil aturan dasar dan fitur tambahan (Mixin)
# Logika: Mengimpor 'kerangka' dan 'kemampuan tambahan' agar kelas Product punya fitur log, diskon, dan pajak secara otomatis.
from app.models.base import AbstractProduct
from app.models.mixins import LoggableMixin, DiscountableMixin, FinansialMixin

# --- 1. KELAS KATEGORI ---
class Category:
    """Label untuk pengelompokan barang agar lebih teratur."""
    def __init__(self, name: str):
        # Logika: Menandai produk ke dalam kelompok tertentu (misal: 'Kebutuhan Pokok').
        self.name = name

# --- 2. KELAS INDUK (BASE CLASS) ---
# Logika: Menjadi fondasi untuk semua jenis barang. Menggabungkan kontrak utama dengan berbagai Mixin.
class Product(AbstractProduct, LoggableMixin, DiscountableMixin, FinansialMixin):
    def __init__(self, product_id: str, name: str, price_obj, category: Category, stock: int = 0):
        # Logika: Menggunakan __ (double underscore) untuk enkapsulasi agar data tidak diubah sembarangan dari luar kelas.
        self.__product_id = product_id 
        self.__name = name
        # Sekarang menyimpan OBJEK harga (RetailPrice/WholesalePrice)
        # Logika: Delegasi tugas. Perhitungan harga diserahkan ke objek harga itu sendiri.
        self.__price_obj = price_obj 
        self.__category = category
        self.__stock = stock

    # --- Jendela Akses (Getter) ---
    @property
    def product_id(self): return self.__product_id
    
    @property
    def name(self): return self.__name
    
    @property
    def price(self): 
        # Logika: Mengambil nilai angka dari objek harga yang disimpan.
        """Mengambil NILAI angka harga dari objek harga."""
        return self.__price_obj.amount
    
    @property
    def stock(self): return self.__stock
    
    @property
    def category(self): return self.__category

    # --- Jendela Ubah (Setter) ---
    @name.setter
    def name(self, value):
        # Logika: Memberikan validasi agar nama tidak bisa diubah menjadi kosong.
        if value: self.__name = value

    @price.setter
    def price(self, value):
        # Logika: Jika harga diupdate, sistem otomatis menganggapnya sebagai harga Retail (eceran).
        # Jika ingin mengubah harga, kita buatkan objek RetailPrice baru
        from app.models.price import RetailPrice
        if value is not None and value >= 0: 
            self.__price_obj = RetailPrice(value)

    # --- FITUR UTAMA: MANAJEMEN STOK ---
    def add_stock(self, amount: int):
        # Logika: Mengelola mutasi barang (masuk/keluar) sekaligus mencatat riwayatnya (logging).
        if amount == 0: return 
        status = f"MASUK: +{amount}" if amount > 0 else f"KELUAR: {abs(amount)}"
        self.__stock += amount
        # Logika: Memanggil fitur dari LoggableMixin untuk mencatat aktivitas ke sistem.
        self.log_action(f"{self.__name:<15} | {status:<12} | Stok Akhir: {self.__stock}")

    def restock(self, amount: int, supplier: str = "Supplier Umum"):
        # Logika: Fungsi khusus untuk penambahan stok dari supplier dengan validasi input positif.
        if amount > 0:
            self.add_stock(amount)
            print(f"[RESTOCK] {amount} unit '{self.__name}' masuk dari {supplier}.")
        else:
            print("[ERROR] Jumlah restock harus positif!")

    def get_details(self):
        # Logika: Implementasi wajib dari AbstractProduct untuk menampilkan info dasar produk.
        # Menghitung pajak menggunakan mixin
        pajak = self.hitung_ppn(self.price)
        total = self.price + pajak
        return f"{'UMUM':<12} | ID:{self.product_id:<6} | {self.name:<15} | Rp{total:<10,.0f} | Stok:{self.stock}"


# ==============================================================================
# --- KELAS ANAK (KATEGORI SPESIFIK) ---
# ==============================================================================
# Logika: Subclass ini mewarisi semua fitur Product tapi punya atribut unik masing-masing.

class FoodProduct(Product):
    def __init__(self, product_id, name, price_obj, category, expiry_date, stock=0):
        # Logika: Mengirim data ke konstruktor kelas induk (Product).
        super().__init__(product_id, name, price_obj, category, stock)
        self.__expiry = expiry_date # Atribut khusus makanan

    def get_details(self):
        # Logika: Override (menimpa) fungsi get_details agar info kadaluarsa ikut muncul.
        pajak = self.hitung_ppn(self.price)
        return f"{'MAKANAN':<12} | ID:{self.product_id:<6} | {self.name:<15} | Rp{self.price + pajak:<10,.0f} | Exp:{self.__expiry:<10} | Stok:{self.stock}"

class DrinkProduct(Product):
    def __init__(self, product_id, name, price_obj, category, volume, stock=0):
        super().__init__(product_id, name, price_obj, category, stock)
        self.__volume = volume # Atribut khusus minuman

    def get_details(self):
        # Logika: Menampilkan volume (misal: 500ml) dalam rincian produk.
        pajak = self.hitung_ppn(self.price)
        return f"{'MINUMAN':<12} | ID:{self.product_id:<6} | {self.name:<15} | Rp{self.price + pajak:<10,.0f} | Vol:{self.__volume:<10} | Stok:{self.stock}"

class ToolsProduct(Product):
    def __init__(self, product_id, name, price_obj, category, material, stock=0):
        super().__init__(product_id, name, price_obj, category, stock)
        self.__material = material # Atribut khusus peralatan

    def get_details(self):
        # Logika: Menampilkan bahan material (misal: Besi/Plastik) dalam rincian produk.
        pajak = self.hitung_ppn(self.price)
        return f"{'TOOLS':<12} | ID:{self.product_id:<6} | {self.name:<15} | Rp{self.price + pajak:<10,.0f} | Mat:{self.__material:<10} | Stok:{self.stock}"