# 1. IMPORT: Mengambil 'kontrak' atau aturan dasar dari file base.py
from app.models.base import AbstractLocation

# --- 2. IMPLEMENTASI LOKASI SWALAYAN ---
# Logika: Kelas Warehouse adalah wujud nyata (objek fisik) dari aturan yang ada di AbstractLocation.
class Warehouse(AbstractLocation): # Mewarisi aturan dari AbstractLocation
    def __init__(self, lid, name, capacity):
        # Logika: Method ini menyiapkan 'ruangan' baru di memori dengan identitas dan batas daya tampung tertentu.
        # Inisialisasi atribut dasar lokasi
        self._lid = lid           # ID lokasi (Protected) -> Logika: Identitas unik agar sistem tidak salah alamat.
        self.name = name          # Nama (misal: 'Gudang Belakang' atau 'Rak Display')
        self._capacity = capacity # Batas maksimal barang -> Logika: Menentukan 'pagar' agar gudang tidak kelebihan beban.
        self.current_count = 0    # Jumlah barang saat ini -> Logika: Dimulai dari 0 karena gudang baru dianggap kosong.

    # --- Jendela Akses (Getter) ---
    @property
    def capacity(self):
        # Logika: Menyediakan akses 'baca saja' (read-only) agar pihak luar bisa tahu kapasitas tanpa bisa mengubahnya sembarangan.
        """Memberi izin sistem untuk mengecek batas maksimal lokasi."""
        return self._capacity

    @property
    def location_id(self): 
        # Logika: Kewajiban dari kontrak; mengembalikan ID lokasi agar bisa dikenali oleh sistem transaksi.
        """Implementasi wajib: Mengembalikan ID lokasi."""
        return self._lid

    # --- METHOD LOGIKA ---
    def is_full(self): 
        # Logika: Melakukan perbandingan matematika. Jika stok saat ini sudah mencapai atau melewati kapasitas, return True.
        """Cek apakah lokasi sudah penuh."""
        return self.current_count >= self._capacity

    def update_stock_count(self, amount: int):
        # Logika: Mesin penggerak stok. Menghandle arus masuk (positif) dan arus keluar (negatif) dalam satu fungsi.
        """
        TAMBAHAN: Memudahkan transaksi untuk menambah/kurangi isi lokasi.
        amount: bisa positif (barang masuk) atau negatif (barang keluar).
        """
        self.current_count += amount

    def get_info(self):
        # Logika: Mengubah data angka yang kaku menjadi informasi yang cantik dan mudah dibaca oleh admin atau kasir.
        """Menampilkan status lokasi dengan format yang lebih rapi untuk swalayan."""
        # Menambahkan label [INFO LOKASI] agar lebih jelas saat di-print
        return f"[INFO LOKASI] {self.name:<18} | Kapasitas: {self.current_count}/{self._capacity} Unit"