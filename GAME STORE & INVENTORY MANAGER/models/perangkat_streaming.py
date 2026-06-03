from models.barang_elektronik import BarangElektronik

class PerangkatStreaming(BarangElektronik):
    """Kelas entitas Perangkat Streaming, mewarisi BarangElektronik."""

    def __init__(self, kode: str, nama: str, harga: int, stok: int, 
                merek: str, garansi: int, resolusi: str, koneksi: str):
        super().__init__(kode, nama, harga, stok, merek, garansi)
        self.__resolusi_output = resolusi
        self.__jenis_koneksi = koneksi

    # ==========================
    # GETTER TAMBAHAN
    # ==========================
    def get_resolusi(self) -> str:
        return self.__resolusi_output

    def get_koneksi(self) -> str:
        return self.__jenis_koneksi

    # ==========================
    # POLYMORPHISM (OVERRIDE)
    # ==========================
    def info_barang(self) -> str:
        """Menampilkan detail spesifikasi perangkat streaming."""
        return f"""
=== STREAMING DEVICE ===
Kode      : {self.get_kode()}
Nama      : {self.get_nama()}
Harga     : Rp {self.get_harga():,}
Stok      : {self.get_stok()}
Merek     : {self.get_merek()}
Garansi   : {self.cek_garansi()}
Resolusi  : {self.__resolusi_output}
Koneksi   : {self.__jenis_koneksi}
"""