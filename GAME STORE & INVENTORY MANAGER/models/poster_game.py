from models.merchandise_game import MerchandiseGame

class PosterGame(MerchandiseGame):
    """Kelas entitas Poster Game, mewarisi MerchandiseGame."""

    def __init__(self, kode: str, nama: str, harga: int, stok: int, 
                bahan: str, asal: str, ukuran: str, kertas: str):
        super().__init__(kode, nama, harga, stok, bahan, asal)
        self.__dimensi_ukuran = ukuran
        self.__jenis_kertas = kertas

    # ==========================
    # GETTER TAMBAHAN
    # ==========================
    def get_ukuran(self) -> str:
        return self.__dimensi_ukuran

    def get_kertas(self) -> str:
        return self.__jenis_kertas

    # ==========================
    # POLYMORPHISM (OVERRIDE)
    # ==========================
    def info_barang(self) -> str:
        """Menampilkan detail spesifikasi poster."""
        return f"""
=== POSTER GAME ===
Kode      : {self.get_kode()}
Nama      : {self.get_nama()}
Harga     : Rp {self.get_harga():,}
Stok      : {self.get_stok()}
Ukuran    : {self.__dimensi_ukuran}
Kertas    : {self.__jenis_kertas}
"""