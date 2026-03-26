# IMPORT: Mengambil aturan dasar dan fitur tambahan (Mixin)
from app.models.base import AbstractProduct
from app.models.mixins import LoggableMixin, DiscountableMixin, FinansialMixin

# --- 1. KELAS KATEGORI ---
class Category:
    """Label untuk pengelompokan barang agar lebih teratur."""
    def __init__(self, name: str):
        self.name = name

# --- 2. KELAS INDUK (BASE CLASS) ---
# Menggunakan MULTIPLE INHERITANCE agar Product punya banyak 'bakat' (Mixin)
class Product(AbstractProduct, LoggableMixin, DiscountableMixin, FinansialMixin):
    def __init__(self, product_id: str, name: str, price: float, category: Category, stock: int = 0):
        # ENKAPSULASI: Mengunci data dengan __ (Private) agar tidak diubah sembarangan
        self.__product_id = product_id 
        self.__name = name
        self.__price = price
        self.__category = category
        self.__stock = stock

    # --- GETTER (@property) ---
    # Jendela akses untuk membaca data yang dikunci (Private)
    @property
    def product_id(self): return self.__product_id
    @property
    def name(self): return self.__name
    @property
    def price(self): return self.__price
    @property
    def stock(self): return self.__stock
    @property
    def category(self): return self.__category

    # --- SETTER (@setter) ---
    # Satpam penjaga: Validasi data sebelum diubah
    @name.setter
    def name(self, value):
        if value: self.__name = value

    @price.setter
    def price(self, value):
        # Validasi: Harga tidak boleh negatif
        if value is not None and value >= 0: self.__price = value

    # --- METHOD LOGIKA (SMART LOGGING) ---
    def add_stock(self, amount: int):
        """Deteksi Otomatis: Menentukan status Masuk/Keluar berdasarkan angka."""
        if amount == 0: return 
        
        # Logika: Jika positif (+) berarti Masuk, jika negatif (-) berarti Keluar
        if amount > 0:
            status = f"MASUK: +{amount}"
        else:
            status = f"KELUAR: {abs(amount)}" # abs() membuang tanda minus agar rapi

        # Update nilai stok di memori
        self.__stock += amount
        
        # Mencatat riwayat ke LoggableMixin (Audit Trail)
        self.log_action(f"{self.__name:<15} | {status:<12} | Stok Akhir: {self.__stock}")

    def get_details(self):
        """POLIMORFISME: Format laporan dasar untuk produk UMUM."""
        pajak = self.hitung_ppn(self.price) # Bakat dari FinansialMixin
        total = self.price + pajak
        return f"{'UMUM':<12} | ID:{self.product_id:<6} | {self.name:<15} | Rp{total:<10,.0f} | Stok:{self.stock}"

# ==============================================================================
# --- KELAS ANAK (INHERITANCE & POLIMORFISME) ---
# ==============================================================================

# 3. KELAS ANAK: ELEKTRONIK (Punya info Garansi)
class ElectronicProduct(Product):
    def __init__(self, product_id, name, price, category, warranty_months, stock=0):
        super().__init__(product_id, name, price, category, stock) # Panggil Induk
        self.__warranty = warranty_months

    def get_details(self):
        pajak = self.hitung_ppn(self.price)
        return f"{'ELEKTRONIK':<12} | ID:{self.product_id:<6} | {self.name:<15} | Rp{self.price + pajak:<10,.0f} | Garansi:{self.__warranty} Bln | Stok:{self.stock}"

# 4. KELAS ANAK: BUKU (Punya info Penulis)
class Buku(Product):
    def __init__(self, product_id, name, price, category, penulis, stock=0):
        super().__init__(product_id, name, price, category, stock)
        self.__penulis = penulis

    def get_details(self):
        pajak = self.hitung_ppn(self.price)
        return f"{'BUKU':<12} | ID:{self.product_id:<6} | {self.name:<15} | Rp{self.price + pajak:<10,.0f} | Penulis:{self.__penulis:<10} | Stok:{self.stock}"

# 5. KELAS ANAK: PAKAIAN (Punya info Ukuran/Size)
class Pakaian(Product):
    def __init__(self, product_id, name, price, category, ukuran, stock=0):
        super().__init__(product_id, name, price, category, stock)
        self.__ukuran = ukuran

    def get_details(self):
        pajak = self.hitung_ppn(self.price)
        return f"{'PAKAIAN':<12} | ID:{self.product_id:<6} | {self.name:<15} | Rp{self.price + pajak:<10,.0f} | Size:{self.__ukuran:<3} | Stok:{self.stock}"

# 6. KELAS ANAK: AKSESORIS (Hanya beda label kategori)
class Aksesoris(Product):
    def get_details(self):
        pajak = self.hitung_ppn(self.price)
        return f"{'AKSESORIS':<12} | ID:{self.product_id:<6} | {self.name:<15} | Rp{self.price + pajak:<10,.0f} | Stok:{self.stock}"