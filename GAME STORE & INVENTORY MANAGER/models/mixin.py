from typing import Any, Union

class DiskonMixin:
    """Mixin untuk fungsionalitas perhitungan diskon."""

    def hitung_nilai_diskon(self, harga: Union[int, float], persen: Union[int, float]) -> float:
        """Menghitung nominal diskon berdasarkan persentase."""
        return harga * persen / 100

    def terapkan_potongan_harga(self, harga: Union[int, float], persen: Union[int, float]) -> float:
        """Menerapkan diskon dan mengembalikan harga akhir."""
        diskon = self.hitung_nilai_diskon(harga, persen)
        return harga - diskon


class PajakMixin:
    """Mixin tambahan untuk kalkulasi finansial seperti Pajak (PPN), Keuntungan, dan Format Uang."""

    def hitung_ppn(self, harga: Union[int, float], persen_ppn: int = 11) -> float:
        """Menghitung nilai Pajak Pertambahan Nilai (PPN). Default 11%."""
        return harga * (persen_ppn / 100)

    def hitung_harga_jual_dengan_ppn(self, harga: Union[int, float], persen_ppn: int = 11) -> float:
        """Mengembalikan total harga setelah ditambah PPN."""
        return harga + self.hitung_ppn(harga, persen_ppn)

    def hitung_profit_margin(self, harga_beli: Union[int, float], harga_jual: Union[int, float]) -> float:
        """Menghitung persentase keuntungan (margin) dari suatu barang."""
        if harga_beli <= 0:
            return 0.0
        profit = harga_jual - harga_beli
        return (profit / harga_beli) * 100

    def format_rupiah(self, nominal: Union[int, float]) -> str:
        """Mengubah angka nominal menjadi format mata uang Rupiah yang rapi."""
        return f"Rp {int(nominal):,}".replace(",", ".")