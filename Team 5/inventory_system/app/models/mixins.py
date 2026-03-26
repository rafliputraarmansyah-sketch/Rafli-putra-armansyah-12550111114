# --- 1. MIXIN UNTUK LOGGING (PENCATATAN) ---
class LoggableMixin:
    """Mixin untuk mencatat aktivitas barang (Dinonaktifkan agar terminal bersih)."""
    
    def log_action(self, action: str, level: str = "INFO"):
        # KEGUNAAN: Tempat mencatat riwayat perubahan stok di belakang layar.
        # Saat ini dikosongkan (pass) agar tampilan terminal tetap rapi.
        pass
        
# --- 2. MIXIN UNTUK FITUR DISKON ---
class DiscountableMixin:
    """Mixin untuk memberikan kemampuan kalkulasi diskon pada produk."""
    
    def get_discounted_price(self, percentage: float):
        """Menghitung harga setelah dipotong diskon."""
        # Validasi: Persentase harus di antara 0-100 agar hitungan tidak kacau.
        if not (0 <= percentage <= 100):
            return self.price # Kembalikan harga asli jika input ngawur
        
        # Rumus: Harga - (Harga * Persen / 100)
        discount_amount = self.price * (percentage / 100)
        return self.price - discount_amount
    
# --- 3. MIXIN UNTUK FITUR FINANSIAL (DARI KAWANMU) ---
class FinansialMixin:
    """Mixin untuk perhitungan pajak PPN dan nilai total kekayaan (Aset)."""
    
    def hitung_ppn(self, harga):
        """Menghitung Pajak Pertambahan Nilai sebesar 11%."""
        # KEGUNAAN: Membantu sistem menentukan harga jual akhir setelah pajak.
        return harga * 0.11 # Pajak 11% sesuai standar aturan terbaru

    def hitung_total_aset(self, harga, stok):
        """Menghitung total nilai uang dari seluruh stok barang yang ada."""
        # KEGUNAAN: Untuk laporan keuangan, berapa total uang yang 'mengendap' di gudang.
        return harga * stok