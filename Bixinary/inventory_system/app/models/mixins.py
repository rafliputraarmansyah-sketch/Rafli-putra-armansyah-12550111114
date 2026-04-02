#Mixin prinsip DRY (Don't Repeat Yourself)

# --- 1. MIXIN UNTUK LOGGING (PENCATATAN) ---
# Logika: Menyediakan 'wadah' agar setiap aksi barang bisa dicatat di masa depan.
class LoggableMixin:
    """Mixin untuk mencatat aktivitas barang."""
    def log_action(self, action: str, level: str = "INFO"):
        # Logika: Dikosongkan agar terminal tidak penuh, namun siap digunakan jika ingin debugging.
        # Tetap seperti permintaanmu: dikosongkan agar terminal bersih
        pass
        
# --- 2. MIXIN UNTUK FITUR DISKON ---
# Logika: Memberikan kemampuan menghitung harga promo pada produk yang memiliki atribut harga.
class DiscountableMixin:
    """Mixin untuk memberikan kemampuan kalkulasi diskon pada produk."""
    def get_discounted_price(self, percentage: float):
        """Menghitung harga setelah dipotong diskon umum."""
        # Logika: Validasi agar persentase tidak minus atau lebih dari 100% (mencegah error harga).
        if not (0 <= percentage <= 100):
            return self.price 
        # Logika: Menghitung nominal potongan dari harga dasar.
        discount_amount = self.price * (percentage / 100)
        # Logika: Mengembalikan harga akhir setelah dipotong diskon.
        return self.price - discount_amount

# --- 3.  MIXIN UNTUK MEMBER SWALAYAN ---
# Logika: Menangani aturan bisnis khusus untuk pelanggan setia (loyalty program).
class MemberMixin:
    """Mixin khusus untuk menangani diskon kartu member swalayan."""
    def hitung_diskon_member(self, harga_total: float, is_member: bool):
        """Potongan tambahan 5% jika pembeli adalah member."""
        # Logika: Cek status member; jika True, berikan potongan harga instan.
        if is_member:
            # Logika: Mengalikan dengan 0.95 sama dengan memotong harga sebesar 5%.
            return harga_total * 0.95 # Diskon 5% langsung
        return harga_total

# --- 4. MIXIN UNTUK FITUR FINANSIAL ---
# Logika: Kumpulan fungsi perhitungan uang dan identifikasi barang (barcode).
class FinansialMixin:
    """Mixin untuk perhitungan pajak PPN dan scan barcode."""
    
    def hitung_ppn(self, harga):
        """Menghitung Pajak Pertambahan Nilai sebesar 11%."""
        # Logika: Standarisasi perhitungan pajak sesuai aturan pemerintah (11%).
        return harga * 0.11

    def scan_barcode(self):
        """Simulasi pembacaan ID produk sebagai barcode teks."""
        # Logika: Mengambil product_id dari kelas utama dan mengubahnya menjadi format visual barcode.
        # Mengambil product_id dari class yang menggunakan Mixin ini
        return f"|| ||| | || {self.product_id} [BARCODE SCANNED]"

    def hitung_total_aset(self, harga, stok):
        """Menghitung total nilai uang dari seluruh stok barang yang ada."""
        # Logika: Membantu manajemen stok untuk mengetahui total modal/aset di gudang (Harga x Qty).
        return harga * stok