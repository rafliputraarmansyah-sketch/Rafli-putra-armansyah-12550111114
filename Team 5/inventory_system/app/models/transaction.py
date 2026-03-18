from datetime import datetime
from app.models.base import AbstractTransaction
from app.models.product import Product
from app.models.location import Warehouse

class StockInTransaction(AbstractTransaction):
    def __init__(self, product: Product, quantity: int, location: Warehouse):
        self.product = product
        self.quantity = quantity
        self.location = location
        self.timestamp = datetime.now()

    def execute(self):
        if not self.location.is_full():
            self.product.add_stock(self.quantity)
            self.location.current_count += self.quantity 
            return True
        return False

    def get_summary(self):
        waktu = self.timestamp.strftime('%Y-%m-%d %H:%M')
        return f"[{waktu}] MASUK  | {self.quantity} unit {self.product.name} -> {self.location.name}"

class StockOutTransaction(AbstractTransaction):
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity
        self.timestamp = datetime.now()

    def execute(self):
        if self.product.stock >= self.quantity:
            self.product.add_stock(-self.quantity) 
            return True
        return False

    def get_summary(self):
        waktu = self.timestamp.strftime('%Y-%m-%d %H:%M')
        return f"[{waktu}] KELUAR | {self.quantity} unit {self.product.name}"