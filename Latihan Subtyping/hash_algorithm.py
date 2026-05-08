# hash_algorithm.py

from abc import ABC, abstractmethod


class HashAlgorithm(ABC):
    """
    Abstract Base Class untuk semua algoritma hashing.

    Semua subclass WAJIB mengimplementasikan:
        hash(text: str) -> str
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def hash(self, text: str) -> str:
        """
        Mengubah string menjadi hash text.

        Parameters:
            text (str): text yang akan di-hash

        Returns:
            str: hasil hash
        """
        pass