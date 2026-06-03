import json
import os

class Database:
    """Menangani operasi I/O (simpan & muat) file JSON untuk data inventaris."""

    def __init__(self, lokasi="data_barang.json"):
        self.__lokasi_file = lokasi

    def simpan_ke_berkas(self, data):
        """Menyimpan list data ke dalam file JSON."""
        direktori = os.path.dirname(self.__lokasi_file)
        if direktori and not os.path.exists(direktori):
            os.makedirs(direktori)

        try:
            with open(self.__lokasi_file, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] Gagal menyimpan data: {e}")

    def muat_dari_berkas(self):
        """Membaca dan memuat data dari file JSON."""
        if not os.path.exists(self.__lokasi_file):
            return []

        try:
            with open(self.__lokasi_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("[WARNING] Format JSON rusak. Memulai dengan data kosong.")
            return []
        except Exception as e:
            print(f"[ERROR] Gagal memuat data: {e}")
            return []