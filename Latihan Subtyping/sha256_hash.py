# sha256_hash.py

import hashlib
from hash_algorithm import HashAlgorithm


class SHA256Hash(HashAlgorithm):
    """
    Subclass dari HashAlgorithm
    untuk algoritma SHA256.
    """

    def __init__(self):
        super().__init__("SHA256")

    def hash(self, text: str) -> str:
        """
        Mengubah string menjadi hash SHA256.
        """
        return hashlib.sha256(text.encode()).hexdigest()