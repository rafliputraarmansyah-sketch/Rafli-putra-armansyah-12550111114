# Mengambil 'kontrak' atau aturan dasar harga dari file base.py
from app.models.base import AbstractPrice

# --- 1. KELAS HARGA ECERAN (RETAIL) ---
class RetailPrice(AbstractPrice): # Mewarisi aturan dari AbstractPrice
    def __init__(self, amount):
        # Inisialisasi nominal harga asli
        self._amount = amount

    def calculate_total(self, quantity):
        # LOGIKA: Harga standar dikali jumlah barang tanpa ada potongan
        return self._amount * quantity

    def format_rupiah(self):
        # Mengubah angka menjadi format teks Rp dengan pemisah ribuan
        return f"Rp{self._amount:,.0f}"

# --- 2. KELAS HARGA GROSIR (WHOLESALE) ---
class WholesalePrice(AbstractPrice): # Mewarisi aturan yang sama tapi logikanya berbeda
    def __init__(self, amount: float, discount_percent: float):
        # Inisialisasi harga dasar dan besar persen diskon khusus grosir
        self._amount = amount
        self._discount_percent = discount_percent

    def calculate_total(self, quantity):
        # LOGIKA: Menghitung harga setelah dipotong diskon grosir dulu, baru dikali jumlah
        # Contoh: Jika diskon 10%, maka multiplier-nya adalah 0.9 (90%)
        multiplier = (100 - self._discount_percent) / 100
        return (self._amount * multiplier) * quantity

    def format_rupiah(self):
        # Menampilkan harga asli sekaligus memberi keterangan berapa potongan grosirnya
        return f"Rp{self._amount:,.0f} (Potongan {self._discount_percent}%)"