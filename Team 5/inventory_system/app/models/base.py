from abc import ABC, abstractmethod # Mengambil library untuk membuat kelas abstrak (blueprint)

# --- 1. KONTRAK UNTUK PRODUK ---
class AbstractProduct(ABC):
    @abstractmethod
    def get_details(self):
        # Setiap kelas anak (Electronic, Buku, dll) WAJIB punya fungsi get_details sendiri
        pass

# --- 2. KONTRAK UNTUK TRANSAKSI ---
class AbstractTransaction(ABC):
    @abstractmethod
    def execute(self):
        # Mewajibkan adanya logika 'eksekusi' (tambah/kurang stok) di setiap transaksi
        pass

    @abstractmethod
    def get_summary(self):
        # Mewajibkan adanya fungsi untuk merangkum hasil transaksi (laporan singkat)
        pass

# --- 3. KONTRAK UNTUK LOKASI/GUDANG ---
class AbstractLocation(ABC):
    @property
    @abstractmethod
    def location_id(self):
        # Mewajibkan setiap lokasi memiliki ID unik yang bisa diakses sebagai properti
        pass

    @abstractmethod
    def is_full(self) -> bool:
        # Aturan: Harus bisa mengecek apakah gudang sudah penuh atau belum
        pass

    @abstractmethod
    def get_info(self):
        # Harus bisa menampilkan informasi nama dan kapasitas lokasi
        pass

# --- 4. KONTRAK UNTUK HARGA ---
class AbstractPrice(ABC):
    @abstractmethod
    def calculate_total(self, quantity: int) -> float:
        # Aturan: Semua yang berhubungan dengan harga harus bisa menghitung total (harga * qty)
        pass

    @abstractmethod
    def format_rupiah(self) -> str:
        # Aturan: Harus bisa mengubah angka harga menjadi format teks Rupiah (Rp.xxx)
        pass