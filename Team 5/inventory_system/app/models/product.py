from app.models.base import AbstractProduct
from app.models.mixins import LoggableMixin, DiscountableMixin

# --- KATEGORI ---
class Category:
    def __init__(self, name: str):
        self.name = name

# --- CLASS INDUK (BASE CLASS) ---
class Product(AbstractProduct, LoggableMixin, DiscountableMixin):
    def __init__(self, product_id: str, name: str, price: float, category: Category, stock: int = 0):
        # Enkapsulasi: Atribut private (__)
        self.__product_id = product_id 
        self.__name = name
        self.__price = price
        self.__category = category
        self.__stock = stock

    # --- GETTER ---
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

    # --- SETTER (REVISI: Agar bisa di-update dari Service) ---
    @name.setter
    def name(self, value):
        if value: self.__name = value

    @price.setter
    def price(self, value):
        if value is not None and value >= 0: self.__price = value

    # --- METHOD ---
    def add_stock(self, amount: int):
        if amount != 0:
            self.__stock += amount
            self.log_action(f"Update stok {self.__name}: {amount}")

    def get_details(self):
        """Laporan Detail Produk Umum."""
        return f"{'UMUM':<12} | ID:{self.__product_id:<6} | {self.__name:<15} | Rp{self.__price:<10,.0f} | Stok:{self.__stock}"

# ==========================================
# --- PEWARISAN & POLIMORFISME (REVISI DETAIL) ---
# ==========================================

class ElectronicProduct(Product):
    def __init__(self, product_id, name, price, category, warranty_months, stock=0):
        super().__init__(product_id, name, price, category, stock)
        self.__warranty = warranty_months

    def get_details(self):
        """Menampilkan Detail + Garansi."""
        return f"{'ELEKTRONIK':<12} | ID:{self.product_id:<6} | {self.name:<15} | Rp{self.price:<10,.0f} | Garansi:{self.__warranty} Bln | Stok:{self.stock}"

class Buku(Product):
    def __init__(self, product_id, name, price, category, penulis, stock=0):
        super().__init__(product_id, name, price, category, stock)
        self.__penulis = penulis

    def get_details(self):
        """Menampilkan Detail + Penulis."""
        return f"{'BUKU':<12} | ID:{self.product_id:<6} | {self.name:<15} | Rp{self.price:<10,.0f} | Penulis:{self.__penulis:<10} | Stok:{self.stock}"

class Pakaian(Product):
    def __init__(self, product_id, name, price, category, ukuran, stock=0):
        super().__init__(product_id, name, price, category, stock)
        self.__ukuran = ukuran

    def get_details(self):
        """Menampilkan Detail + Ukuran."""
        return f"{'PAKAIAN':<12} | ID:{self.product_id:<6} | {self.name:<15} | Rp{self.price:<10,.0f} | Size:{self.__ukuran:<3} | Stok:{self.stock}"

class Aksesoris(Product):
    def get_details(self):
        """Menampilkan Detail Aksesoris."""
        return f"{'AKSESORIS':<12} | ID:{self.product_id:<6} | {self.name:<15} | Rp{self.price:<10,.0f} | Stok:{self.stock}"