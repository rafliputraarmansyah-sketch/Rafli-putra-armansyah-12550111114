from models.merchandise_game import MerchandiseGame

class ApparelGame(MerchandiseGame):
    """Kelas entitas Apparel Game, mewarisi MerchandiseGame."""

    def __init__(self, kode: str, nama: str, harga: int, stok: int, 
                bahan: str, asal: str, ukuran: str, usia: str):
        super().__init__(kode, nama, harga, stok, bahan, asal)
        self.__ukuran_pakaian = ukuran
        self.__kategori_usia = usia

    # ==========================
    # GETTER TAMBAHAN
    # ==========================
    def get_ukuran(self) -> str:
        return self.__ukuran_pakaian

    def get_usia(self) -> str:
        return self.__kategori_usia

    # ==========================
    # POLYMORPHISM (OVERRIDE)
    # ==========================
    def info_barang(self) -> str:
        """Menampilkan detail spesifikasi apparel game."""
        return f"""
=== APPAREL GAME ===
Kode      : {self.get_kode()}
Nama      : {self.get_nama()}
Harga     : Rp {self.get_harga():,}
Stok      : {self.get_stok()}
Ukuran    : {self.__ukuran_pakaian}
Usia      : {self.__kategori_usia}
"""