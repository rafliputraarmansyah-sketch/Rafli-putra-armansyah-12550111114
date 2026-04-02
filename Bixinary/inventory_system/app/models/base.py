from abc import ABC, abstractmethod # Mengambil library untuk membuat kelas abstrak (blueprint)

# --- 1. KONTRAK UNTUK PRODUK ---
# Logika: Menjamin semua item di sistem memiliki identitas yang jelas.
class AbstractProduct(ABC):
    @abstractmethod
    def get_details(self):
        # Logika: Memastikan setiap produk (seperti HP atau Buku) bisa mendeskripsikan dirinya sendiri.
        # Tanpa ini, sistem tidak akan tahu spesifikasi produk saat ditampilkan di katalog.
        pass

# --- 2. KONTRAK UNTUK TRANSAKSI ---
# Logika: Mengatur alur keluar-masuk barang agar stok tetap akurat.
class AbstractTransaction(ABC):
    @abstractmethod
    def execute(self):
        # Logika: Pusat perubahan data. Di sini stok akan dikurangi atau ditambah.
        # Ini mencegah adanya transaksi yang 'menggantung' tanpa memproses data stok.
        pass

    @abstractmethod
    def get_summary(self):
        # Logika: Menyediakan data mentah untuk kebutuhan log atau riwayat transaksi.
        # Berguna agar admin bisa melacak kapan dan apa yang ditransaksikan.
        pass

# --- 3. KONTRAK UNTUK LOKASI/GUDANG ---
# Logika: Mengelola manajemen ruang dan penyimpanan agar tidak terjadi overcapacity.
class AbstractLocation(ABC):
    @property
    @abstractmethod
    def location_id(self):
        # Logika: Mewajibkan adanya ID unik (seperti kode Rak atau Baris) untuk validasi posisi barang.
        pass

    @abstractmethod
    def is_full(self) -> bool:
        # Logika: Fungsi kontrol. Sebelum memasukkan barang, sistem wajib mengecek sisa kapasitas.
        # Mengembalikan True jika penuh, False jika masih ada ruang.
        pass

    @abstractmethod
    def get_info(self):
        # Logika: Memberikan gambaran visual/teks mengenai kondisi gudang saat ini.
        pass

# --- 4. KONTRAK UNTUK HARGA ---
# Logika: Standarisasi perhitungan uang dan tampilan mata uang di seluruh aplikasi.
class AbstractPrice(ABC):
    @abstractmethod
    def calculate_total(self, quantity: int) -> float:
        # Logika: Mengalikan harga dasar dengan jumlah barang. 
        # Menjamin perhitungan matematika yang konsisten di semua jenis produk.
        pass

    @abstractmethod
    def format_rupiah(self) -> str:
        # Logika: Mengubah angka (float/int) menjadi string cantik (Rp. 10.000).
        # Memastikan user interface (UI) seragam dalam menampilkan harga.
        pass

# --- 5. KONTRAK UNTUK PEMBAYARAN (TAMBAHAN SWALAYAN) ---
# Logika: Menangani fase akhir transaksi (Checkout).
class AbstractPayment(ABC):
    @abstractmethod
    def calculate_total_bill(self):
        # Logika: Menghitung total akhir termasuk pajak, diskon, atau biaya tambahan lainnya.
        pass

    @abstractmethod
    def print_receipt(self):
        # Logika: Output fisik/digital sebagai bukti sah pembayaran bagi pelanggan.
        pass