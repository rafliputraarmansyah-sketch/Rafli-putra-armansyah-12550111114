from models.merchandise_game import MerchandiseGame

class FigureGame(MerchandiseGame):
    """Kelas entitas Figure Game, mewarisi MerchandiseGame."""

    def __init__(self, kode: str, nama: str, harga: int, stok: int, 
                bahan: str, asal: str, karakter: str, skala: str):
        super().__init__(kode, nama, harga, stok, bahan, asal)
        self.__nama_karakter = karakter
        self.__skala_ukuran = skala

    # ==========================
    # GETTER TAMBAHAN
    # ==========================
    def get_karakter(self) -> str:
        return self.__nama_karakter

    def get_skala(self) -> str:
        return self.__skala_ukuran

    # ==========================
    # POLYMORPHISM (OVERRIDE)
    # ==========================
    def info_barang(self) -> str:
        """Menampilkan detail spesifikasi figure."""
        return f"""
=== FIGURE GAME ===
Kode      : {self.get_kode()}
Nama      : {self.get_nama()}
Harga     : Rp {self.get_harga():,}
Stok      : {self.get_stok()}
Karakter  : {self.__nama_karakter}
Skala     : {self.__skala_ukuran}
"""