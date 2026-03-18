from app.models.base import AbstractLocation

class Warehouse(AbstractLocation):
    def __init__(self, lid, name, capacity):
        self._lid = lid
        self.name = name
        self._capacity = capacity
        self.current_count = 0

    @property
    def location_id(self): return self._lid
    def is_full(self): return self.current_count >= self._capacity
    def get_info(self):
        return f"[LOKASI] Gudang: {self.name} | Kapasitas: {self.current_count}/{self._capacity}"