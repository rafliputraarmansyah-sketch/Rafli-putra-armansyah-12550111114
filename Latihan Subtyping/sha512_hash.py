# sha512_hash.py

import hashlib
from hash_algorithm import HashAlgorithm


class SHA512Hash(HashAlgorithm):
    """
    Subclass dari HashAlgorithm
    untuk algoritma SHA512.
    """

    def __init__(self):
        super().__init__("SHA512")

    def hash(self, text: str) -> str:
        """
        Mengubah string menjadi hash SHA512.
        """
        return hashlib.sha512(text.encode()).hexdigest()