# main.py

from hash_manager import HashManager

from md5_hash import MD5Hash
from sha1_hash import SHA1Hash
from sha256_hash import SHA256Hash
from sha512_hash import SHA512Hash


def main():

    print("=== PROGRAM HASH STRING ===")
    print("1. MD5")
    print("2. SHA1")
    print("3. SHA256")
    print("4. SHA512")

    pilihan = input("Pilih algoritma hash (1/2/3/4): ")
    text = input("Masukkan text: ")

    # Subtyping / polymorphism
    if pilihan == "1":
        algorithm = MD5Hash()

    elif pilihan == "2":
        algorithm = SHA1Hash()

    elif pilihan == "3":
        algorithm = SHA256Hash()

    elif pilihan == "4":
        algorithm = SHA512Hash()

    else:
        print("Pilihan tidak valid.")
        return

    # HashManager menerima semua subtype HashAlgorithm
    manager = HashManager(algorithm)

    hasil_hash = manager.generate_hash(text)

    print("\n=== HASIL HASH ===")
    print("Algoritma :", algorithm.name)
    print("Text      :", text)
    print("Hash      :", hasil_hash)


if __name__ == "__main__":
    main()