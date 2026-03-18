from abc import ABC, abstractmethod

class AbstractProduct(ABC):
    @abstractmethod
    def get_details(self):
        pass

class AbstractTransaction(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def get_summary(self):
        pass

class AbstractLocation(ABC):
    @property
    @abstractmethod
    def location_id(self):
        pass

    @abstractmethod
    def is_full(self) -> bool:
        pass

    @abstractmethod
    def get_info(self):
        pass

class AbstractPrice(ABC):
    @abstractmethod
    def calculate_total(self, quantity: int) -> float:
        pass

    @abstractmethod
    def format_rupiah(self) -> str:
        pass