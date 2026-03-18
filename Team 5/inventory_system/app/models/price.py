from app.models.base import AbstractPrice

class RetailPrice(AbstractPrice):
    def __init__(self, amount):
        self._amount = amount
    def calculate_total(self, quantity):
        return self._amount * quantity
    def format_rupiah(self):
        return f"Rp{self._amount:,.0f}"

class WholesalePrice(AbstractPrice):
    def __init__(self, amount: float, discount_percent: float):
        self._amount = amount
        self._discount_percent = discount_percent
    def calculate_total(self, quantity):
        multiplier = (100 - self._discount_percent) / 100
        return (self._amount * multiplier) * quantity
    def format_rupiah(self):
        return f"Rp{self._amount:,.0f} (Potongan {self._discount_percent}%)"