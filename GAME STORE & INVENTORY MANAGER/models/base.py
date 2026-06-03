from abc import ABC, abstractmethod

class Barang(ABC):
    """Abstract Base Class (ABC) sebagai cetak biru utama untuk semua jenis barang."""

    def __init__(self, kode: str, nama: str, harga: int, stok: int):
        self.__kode = kode
        self.__nama = nama
        self.__harga = harga
        self.__stok = stok

    # ==========================
    # GETTER
    # ==========================
    def get_kode(self) -> str:
        return self.__kode

    def get_nama(self) -> str:
        return self.__nama

    def get_harga(self) -> int:
        return self.__harga

    def get_stok(self) -> int:
        return self.__stok

    # ==========================
    # SETTER
    # ==========================
    def set_nama(self, nama: str) -> None:
        self.__nama = nama

    def set_harga(self, harga: int) -> None:
        self.__harga = harga

    def set_stok(self, stok: int) -> None:
        self.__stok = stok

    # ==========================
    # KELOLA STOK
    # ==========================
    def kurangi_stok(self, jumlah: int) -> None:
        """Mengurangi stok barang dengan validasi."""
        if jumlah > self.__stok:
            raise ValueError("Stok tidak mencukupi")
        self.__stok -= jumlah

    def tambah_stok(self, jumlah: int) -> None:
        """Menambah stok barang dengan validasi."""
        if jumlah < 0:
            raise ValueError("Jumlah tambah stok tidak valid")
        self.__stok += jumlah

    # ==========================
    # METHOD ABSTRAK
    # ==========================
    @abstractmethod
    def info_barang(self) -> str:
        """Wajib di-override oleh semua kelas turunan."""
        pass