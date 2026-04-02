# Mengambil 'kontrak' atau aturan dasar harga dari file base.py
from app.models.base import AbstractPrice

# --- 1. KELAS HARGA ECERAN (RETAIL) ---
# Logika: Digunakan untuk barang yang dibeli satuan tanpa ada potongan harga khusus jumlah.
class RetailPrice(AbstractPrice): 
    def __init__(self, amount):
        # Inisialisasi nominal harga asli
        self._amount = amount

    @property
    def amount(self):
        # Logika: Mengembalikan nilai harga asli agar bisa dibaca oleh modul lain (misal: modul diskon).
        """Memberi izin sistem untuk membaca angka harganya saja."""
        return self._amount

    def calculate_total(self, quantity):
        # LOGIKA: Perkalian sederhana. Karena retail, tidak ada pengecekan kondisi jumlah.
        # Harga standar dikali jumlah barang
        return self._amount * quantity

    def format_rupiah(self):
        # Logika: Mengubah angka polos menjadi format mata uang agar user tidak bingung membaca angka nol.
        # Format Rupiah standar (Contoh: Rp15,000)
        return f"Rp{self._amount:,.0f}"

# --- 2. KELAS HARGA GROSIR (WHOLESALE) ---
# Logika: Memberikan insentif kepada pembeli agar membeli dalam jumlah banyak (Bulk Buying).
class WholesalePrice(AbstractPrice): 
    def __init__(self, amount: float, discount_percent: float, min_qty: int = 12):
        # Inisialisasi harga dasar, besar diskon, dan MINIMAL BELI (Default: 12)
        # Logika: Menyimpan syarat 'ambang batas' (min_qty) kapan diskon mulai berlaku.
        self._amount = amount
        self._discount_percent = discount_percent
        self._min_qty = min_qty 

    @property
    def amount(self):
        # Logika: Mengembalikan harga dasar sebelum diskon grosir diterapkan.
        return self._amount

    def calculate_total(self, quantity):
        # LOGIKA SWALAYAN: Menggunakan gerbang logika (if-else) untuk menentukan harga.
        # Cek apakah jumlah beli sudah mencapai syarat grosir?
        if quantity >= self._min_qty:
            # Logika: Jika jumlah beli memenuhi syarat, hitung harga per unit yang sudah didiskon.
            # Jika mencapai minimal (misal 12), diskon aktif
            multiplier = (100 - self._discount_percent) / 100
            return (self._amount * multiplier) * quantity
        else:
            # Logika: Jika jumlah beli kurang dari syarat, kembalikan ke perhitungan harga normal.
            # Jika beli satuan (di bawah 12), pakai harga normal
            return self._amount * quantity

    def format_rupiah(self):
        # Logika: Memberikan transparansi harga kepada pembeli mengenai keuntungan beli grosir.
        # Menampilkan info minimal pembelian agar pembeli tahu syarat harga grosir
        return f"Rp{self._amount:,.0f} (Grosir min.{self._min_qty}pcs: -{self._discount_percent}%)"