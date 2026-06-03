from models.barang_elektronik import BarangElektronik
from models.mixin import DiskonMixin

class AksesorisGaming(BarangElektronik, DiskonMixin):
    """Kelas entitas Aksesoris Gaming, mewarisi BarangElektronik dan DiskonMixin."""

    def __init__(self, kode: str, nama: str, harga: int, stok: int, 
                merek: str, garansi: int, jenis: str, kompatibilitas: str):
        super().__init__(kode, nama, harga, stok, merek, garansi)
        self.__jenis_aksesoris = jenis
        self.__daftar_kompatibilitas = kompatibilitas

    # ==========================
    # GETTER TAMBAHAN
    # ==========================
    def get_jenis(self) -> str:
        return self.__jenis_aksesoris

    def get_kompatibilitas(self) -> str:
        return self.__daftar_kompatibilitas

    # ==========================
    # POLYMORPHISM (OVERRIDE)
    # ==========================
    def info_barang(self) -> str:
        """Menampilkan detail spesifikasi aksesoris gaming."""
        return f"""
=== AKSESORIS GAMING ===
Kode           : {self.get_kode()}
Nama           : {self.get_nama()}
Harga          : Rp {self.get_harga():,}
Stok           : {self.get_stok()}
Merek          : {self.get_merek()}
Garansi        : {self.cek_garansi()}
Jenis          : {self.__jenis_aksesoris}
Kompatibilitas : {self.__daftar_kompatibilitas}
"""