
#======================================================*Simulasi Pengelolaan Informasi Buku dalam Sebuah Perpustakaan*===================================

#========================= CLASS BUKU ==================================
class Buku:
    def __init__(self, judul, penulis, isbn, tahun):
        if not judul or not isbn:
            raise ValueError("Judul dan ISBN tidak boleh kosong.")
        self.__judul = judul
        self.__penulis = penulis
        self.__isbn = isbn
        self.__tahun = tahun
        self.__status_pinjaman = False
        self.__dipinjam_oleh = None
    

    @property # Berguna untuk membaca dan melihat data yang privat diluar class
    def isbn(self): return self.__isbn
    @property
    def judul(self): return self.__judul
    @property
    def status_pinjaman(self): return self.__status_pinjaman
    @status_pinjaman.setter # Berguna untuk mengganti dan mengisi ulang data privat dari luar class
    def status_pinjaman(self, value): self.__status_pinjaman = value
    @property
    def dipinjam_oleh(self): return self.__dipinjam_oleh
    @dipinjam_oleh.setter
    def dipinjam_oleh(self, value): self.__dipinjam_oleh = value

    def get_info(self):
        return f"[FISIK] {self.__judul}"

    def __str__(self):
        status_dipinjam = f"Buku sedang dipinjam oleh member dengan NIM {self.__dipinjam_oleh}" if self.__status_pinjaman else "Belum dipinjam siapapun"
        return (f"Judul: {self.__judul}, "
                f"Penulis: {self.__penulis}, "
                f"ISBN: {self.__isbn}, "
                f"Status_pinjaman: {status_dipinjam}")

#========================= CLASS BUKU DIGITAL ==================================
class BukuDigital(Buku):
    def __init__(self, judul, penulis, isbn, tahun, link):
        super().__init__(judul, penulis, isbn, tahun)
        self.__link = link

    def get_info(self):
            return f"[DIGITAL] {self.judul} (Link: {self.__link})"

    def __str__(self):
        return super().__str__() + f" | Link: {self.__link}"

#======================== CLASS MEMBER =================================
class Member:
    def __init__(self, nim, nama, email):
        if not nim or not nama:
            raise ValueError("NIM dan Nama member wajib diisi.")
        self.__nim = nim
        self.__nama = nama
        self.__email = email
        self.__daftar_pinjaman = []

    @property 
    def nim(self): return self.__nim 
    @property
    def nama(self): return self.__nama
    @nama.setter
    def nama(self, value): self.__nama = value
    @property
    def email(self): return self.__email
    @email.setter
    def email(self, value): self.__email = value
    @property
    def daftar_pinjaman(self): return self.__daftar_pinjaman

    def __str__(self):
        if self.__daftar_pinjaman:
            judul_buku = ",".join([buku.judul for buku in self.daftar_pinjaman])
        else:
            judul_buku = "Tidak ada buku yang dipinjam"
        return (f"Nama:{self.nama}, Nim: {self.nim}, Email: {self.email}, Buku Dipinjam: [{judul_buku}]")

#========================= CLASS PUSTAKA ================================
class Pustaka:
    def __init__(self):
        self.__daftar_buku = {}
        self.__daftar_member = {}

# Bagian untuk Menambahkan Member
    def add_member(self, member):
        try:
            if member.nim in self.__daftar_member:
                print(f"NIM {member.nim} sudah terdaftar.")
            else:
                self.__daftar_member[member.nim] = member
                print(f"Member '{member.nama}' berhasil ditambahkan.")
        except AttributeError:
            print("Error: Data member tidak valid.")

# Bagian untuk Mengecek Member
    def list_daftar_member(self):
        if not self.__daftar_member:
            print("Belum ada member terdaftar.")
        else:
            for member in self.__daftar_member.values():
                print(member)

# Bagian untuk Memperbarui data Member
    def update_member(self, nim, nama=None, email=None):
        if nim in self.__daftar_member:
            if nama:
                self.__daftar_member[nim].nama = nama
            if email:
                self.__daftar_member[nim].email = email
            print(f"Data Member NIM '{nim}' berhasil diperbarui.")
        else:
            print(f"Gagal: Member NIM '{nim}' tidak ditemukan.")

# Bagian untuk Menghapus Member
    def delete_member(self, nim):
        if nim in self.__daftar_member:
            if self.__daftar_member[nim].daftar_pinjaman:
                print(f"Gagal: Member {nim} masih meminjam buku.")
                return
            del self.__daftar_member[nim]
            print(f"Member dengan NIM {nim} berhasil dihapus.")

# Bagian untuk Menambahkan buku
    def add_buku(self, buku):
        try:
            self.__daftar_buku[buku.isbn] = buku
            print(f"Buku '{buku.judul}' Telah ditambahkan.")
        except AttributeError:
            print("Error: Data buku tidak valid.")

# Bagian untuk Melihat list buku
    def list_buku(self):
        if not self.__daftar_buku:
            print('Pustaka kosong.')
        else:
            for buku in self.__daftar_buku.values():
                print(buku.get_info())

#Bagian untuk Mengupdate buku
    def update_buku(self, isbn, judul=None, penulis=None):
        if isbn in self.__daftar_buku:
            print(f"Data buku {isbn} berhasil diperbarui.")
        else:
            print("Gagal: ISBN tidak ditemukan.")

#Bagian untuk Menghapus buku
    def delete_buku(self, isbn):
        if isbn in self.__daftar_buku:
            if self.__daftar_buku[isbn].status_pinjaman:
                print(f"Gagal: Buku {isbn} sedang dipinjam.")
                return
            # -------------------------
            del self.__daftar_buku[isbn]

# Bagian untuk Meminjam buku
    def borrow_buku(self, isbn, nim):
        if nim not in self.__daftar_member:
            print(f'NIM {nim} tidak ditemukan.')
            return
        
        buku = self.__daftar_buku.get(isbn)
        if not buku: # <<< Tambahkan pengecekan ini
            print("Gagal: ISBN buku tidak ditemukan.")
            return
        if buku:
            if not buku.status_pinjaman:
                buku.status_pinjaman = True
                buku.dipinjam_oleh = nim
                self.__daftar_member[nim].daftar_pinjaman.append(buku)
                print(f"Berhasil! {self.__daftar_member[nim].nama} meminjam '{buku.judul}'.")
            else:
                print(f"Maaf, buku '{buku.judul}' sedang dipinjam.")
        else:
            print("ISBN tidak ditemukan.")

# Bagian untuk Mengembalikan buku 
    def return_buku(self, isbn, nim):
        if nim not in self.__daftar_member:
            print(f"NIM {nim} tidak ditemukan.")
            return

        buku = self.__daftar_buku.get(isbn)
        if buku and buku.status_pinjaman and buku.dipinjam_oleh == nim:
            buku.status_pinjaman = False
            buku.dipinjam_oleh = None
            self.__daftar_member[nim].daftar_pinjaman.remove(buku)
            print(f"Buku '{buku.judul}' telah kembali.")
        else:
            print("Gagal: Data peminjaman tidak sesuai.")


# =========================================================================
#                        KODE UNTUK MENGUJI DATA 
# =========================================================================

if __name__ == "__main__":
    try:
        print("=== 1. TES PROGRAM DENGAN DATA ===")
        my_pustaka = Pustaka()
        print()

        # 2. Pengujian Kode dari Buku & get_info (Fisik)
        print("=== 2.TES MENAMBAH BUKU FISIK ===")
        buku1 = Buku("Laskar Pelangi", "Andrea Hirata", "978-602", 2005)
        buku2 = Buku("Bumi Manusia", "Pramoedya Ananta Toer", "978-979", 1980)
        my_pustaka.add_buku(buku1)
        my_pustaka.add_buku(buku2)
        print()

        # 3. Pengujian Buku Digital
        print("=== 3.TES MENAMBAH BUKU DIGITAL ===")
        buku_digital = BukuDigital("Python for Beginners", "Guido van Rossum", "112-233", 2020, "https://pustaka.com/python-pdf")
        my_pustaka.add_buku(buku_digital)
        print()

        # 4. Pengujian List Buku (Menjalankan get_info secara polimorfik)
        print("=== 4.TES DAFTAR SEMUA BUKU (get_info) ===")
        my_pustaka.list_buku()
        print()

        # 5. Pengujian Member (Add Member)
        print("=== 5.TES MENAMBAH MEMBER ===")
        member1 = Member("22001", "Budi Santoso", "budi@gmail.com")
        member2 = Member("22002", "Siti Aminah", "siti@gmail.com")
        my_pustaka.add_member(member1)
        my_pustaka.add_member(member2)
        print()

        # 6. Pengujian List Daftar Member
        print("=== 6.TES DAFTAR SEMUA MEMBER ===")
        my_pustaka.list_daftar_member()
        print()

        # 7. Pengujian Update Member
        print("=== 7.TES UPDATE DATA MEMBER ===")
        my_pustaka.update_member("22001", nama="Budi S. Raharjo", email="budi_new@gmail.com")
        print("Setelah update:")
        my_pustaka.list_daftar_member()
        print()

        # 8. Pengujian Update Buku (Mengecek keberadaan ISBN)
        print("=== 8.TES UPDATE DATA BUKU ===")
        my_pustaka.update_buku("978-602") # Menguji fungsi update_buku yang ada
        print()

        # 9. Pengujian Borrow Buku (Peminjaman)
        print("=== 9.TES PROSES PEMINJAMAN BUKU ===")
        # Budi meminjam Laskar Pelangi
        my_pustaka.borrow_buku("978-602", "22001")
        # Siti meminjam Python Digital
        my_pustaka.borrow_buku("112-233", "22002")
        # Coba pinjam buku yang sama oleh orang berbeda
        my_pustaka.borrow_buku("978-602", "22002") 
        print()

        # 10. Melihat status setelah peminjaman
        print("=== 10.TES STATUS MEMBER & BUKU SETELAH PINJAM ===")
        print(member1)
        print(member2)
        print(buku1) # Cek status melalui __str__
        print()

        # 11. Pengujian Return Buku (Pengembalian)
        print("=== 11.TES PROSES PENGEMBALIAN BUKU ===")
        my_pustaka.return_buku("978-602", "22001")
        print("Setelah dikembalikan:")
        print(member1)
        print(buku1)
        print()

        # 12. Pengujian Delete Member
        print("=== 12.TES MENGHAPUS MEMBER ===")
        my_pustaka.delete_member("22002")
        my_pustaka.list_daftar_member()
        print()

        # 13. Pengujian Delete Buku
        print("=== 13.TES MENGHAPUS BUKU ===")
        my_pustaka.delete_buku("112-233")
        my_pustaka.list_buku()
        print()

    except ValueError as e: # Menginfokan jika error input kosong
            print(f"Kesalahan Input: {e}")
    except Exception as e: # Mengingfokan error sistem lainnya
            print(f"Terjadi error tak terduga: {e}")
