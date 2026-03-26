# 1. IMPORT: Mengambil 'kontrak' atau aturan dasar dari file base.py
from app.models.base import AbstractLocation

# --- 2. IMPLEMENTASI NYATA GUDANG ---
class Warehouse(AbstractLocation): # Mewarisi aturan dari AbstractLocation
    def __init__(self, lid, name, capacity):
        # Inisialisasi atribut dasar gudang
        self._lid = lid           # ID lokasi (Protected)
        self.name = name          # Nama gudang (misal: 'Gudang Pusat')
        self._capacity = capacity # Batas maksimal barang (Ini yang bikin error tadi)
        self.current_count = 0    # Jumlah barang yang ada saat ini (dimulai dari 0)

    # --- TAMBAHAN PENTING: Jendela Akses untuk Transaction.py ---
    @property
    def capacity(self):
        """Memperbaiki error: Memberi izin file lain untuk membaca nilai _capacity."""
        return self._capacity

    @property
    def location_id(self): 
        # Implementasi wajib: Mengembalikan ID lokasi agar bisa diakses sistem
        return self._lid

    # --- METHOD LOGIKA ---
    def is_full(self): 
        # Logika pengecekan: Jika jumlah barang >= kapasitas, berarti penuh (True)
        return self.current_count >= self._capacity

    def get_info(self):
        """Menampilkan status gudang (berapa yang sudah terisi dari total kapasitas)."""
        return f"[LOKASI] Gudang: {self.name} | Kapasitas: {self.current_count}/{self._capacity}"