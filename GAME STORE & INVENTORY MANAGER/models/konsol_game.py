from models.barang_elektronik import BarangElektronik
from models.mixin import DiskonMixin

class KonsolGame(BarangElektronik, DiskonMixin):
    """Kelas entitas Konsol Game, mewarisi BarangElektronik dan DiskonMixin."""

    def __init__(self, kode: str, nama: str, harga: int, stok: int, 
                merek: str, garansi: int, tipe: str, storage: str):
        super().__init__(kode, nama, harga, stok, merek, garansi)
        self.__tipe_konsol = tipe
        self.__kapasitas = storage

    # ==========================
    # GETTER TAMBAHAN
    # ==========================
    def get_tipe(self) -> str:
        return self.__tipe_konsol

    def get_kapasitas(self) -> str:
        return self.__kapasitas

    # ==========================
    # POLYMORPHISM (OVERRIDE)
    # ==========================
    def info_barang(self) -> str:
        """Menampilkan detail spesifikasi konsol game."""
        return f"""
=== KONSOL GAME ===
Kode      : {self.get_kode()}
Nama      : {self.get_nama()}
Harga     : Rp {self.get_harga():,}
Stok      : {self.get_stok()}
Merek     : {self.get_merek()}
Garansi   : {self.cek_garansi()}
Tipe      : {self.__tipe_konsol}
Storage   : {self.__kapasitas}
"""