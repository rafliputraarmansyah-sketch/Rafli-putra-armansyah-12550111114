from models.base import Barang
from models.mixin import DiskonMixin

class MerchandiseGame(Barang, DiskonMixin):
    """Kelas induk (subclass dari Barang) untuk semua item merchandise game."""

    def __init__(self, kode: str, nama: str, harga: int, stok: int, bahan: str, asal: str):
        super().__init__(kode, nama, harga, stok)
        self.__jenis_bahan = bahan
        self.__asal_produksi = asal

    # ==========================
    # GETTER
    # ==========================
    def get_bahan(self) -> str:
        return self.__jenis_bahan

    def get_asal(self) -> str:
        return self.__asal_produksi

    def cek_kualitas_bahan(self) -> str:
        """Mengembalikan informasi bahan merchandise."""
        return f"Bahan: {self.__jenis_bahan}"

    # ==========================
    # POLYMORPHISM (OVERRIDE)
    # ==========================
    def info_barang(self) -> str:
        """Menampilkan detail spesifikasi merchandise."""
        return f"""
=== MERCHANDISE GAME ===
Kode  : {self.get_kode()}
Nama  : {self.get_nama()}
Harga : Rp {self.get_harga():,}
Stok  : {self.get_stok()}
Bahan : {self.__jenis_bahan}
Asal  : {self.__asal_produksi}
"""