class LoggableMixin:
    """Mixin untuk mencatat aktivitas (Dinonaktifkan agar terminal bersih)."""
    
    def log_action(self, action: str, level: str = "INFO"):
        # Dikosongkan (pass) agar tidak ada log yang muncul di terminal atau file
        pass
        
class DiscountableMixin:
    """Mixin untuk memberikan fitur diskon pada produk."""
    
    def get_discounted_price(self, percentage: float):
        """Menghitung harga setelah diskon."""
        # Gunakan self.price (memanggil property price)
        if not (0 <= percentage <= 100):
            return self.price
        
        discount_amount = self.price * (percentage / 100)
        return self.price - discount_amount