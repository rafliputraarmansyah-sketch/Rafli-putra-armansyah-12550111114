# md5_hash.py

import hashlib
from hash_algorithm import HashAlgorithm


class MD5Hash(HashAlgorithm):
    """
    Subclass dari HashAlgorithm
    untuk algoritma MD5.
    """

    def __init__(self):
        super().__init__("MD5")

    def hash(self, text: str) -> str:
        """
        Mengubah string menjadi hash MD5.
        """
        return hashlib.md5(text.encode()).hexdigest()