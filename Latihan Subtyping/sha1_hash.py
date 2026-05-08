# sha1_hash.py

import hashlib
from hash_algorithm import HashAlgorithm


class SHA1Hash(HashAlgorithm):
    """
    Subclass dari HashAlgorithm
    untuk algoritma SHA1.
    """

    def __init__(self):
        super().__init__("SHA1")

    def hash(self, text: str) -> str:
        """
        Mengubah string menjadi hash SHA1.
        """
        return hashlib.sha1(text.encode()).hexdigest()