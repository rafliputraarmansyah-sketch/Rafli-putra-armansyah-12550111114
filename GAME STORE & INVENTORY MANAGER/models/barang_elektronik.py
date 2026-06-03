from models.base import Barang

class BarangElektronik(Barang):
    """Kelas induk (subclass dari Barang) untuk semua item elektronik."""

    def __init__(self, kode: str, nama: str, harga: int, stok: int, merek: str, garansi: int):
        super().__init__(kode, nama, harga, stok)
        self.__merek = merek
        self.__masa_garansi = garansi

    # ==========================
    # GETTER & UTILITY
    # ==========================
    def get_merek(self) -> str:
        return self.__merek

    def get_masa_garansi(self) -> int:
        return self.__masa_garansi

    def cek_garansi(self) -> str:
        """Mengembalikan masa garansi dalam satuan bulan."""
        return f"{self.__masa_garansi} bulan"