# hash_manager.py

from hash_algorithm import HashAlgorithm


class HashManager:
    """
    Class untuk mengatur penggunaan algoritma hashing.
    Memanfaatkan konsep subtyping/polymorphism.
    """

    def __init__(self, algorithm: HashAlgorithm):
        self.algorithm = algorithm

    def set_algorithm(self, algorithm: HashAlgorithm):
        """
        Mengganti algoritma hashing.
        """
        self.algorithm = algorithm

    def generate_hash(self, text: str) -> str:
        """
        Menghasilkan hash dari text menggunakan
        algoritma yang sedang dipakai.
        """
        return self.algorithm.hash(text)