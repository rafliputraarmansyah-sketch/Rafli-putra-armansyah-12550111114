
#==================================================*Simulasi Pengelolaan Informasi Buku dalam Sebuah Perpustakaan*===============================

#========================= CLASS BUKU ==================================
class Buku:
    def __init__(self, judul, penulis, isbn, tahun):
        self.judul = judul
        self.penulis = penulis
        self.isbn = isbn
        self.tahun = tahun
        self.status_pinjaman = False
        self.dipinjam_oleh = None

    def __str__(self):
        status_dipinjam = f"Buku sedang dipinjam oleh member dengan NIM {self.dipinjam_oleh}" if self.status_pinjaman else "Belum dipinjam siapapun"
        return (f"Judul: {self.judul}, "
                f"Penulis: {self.penulis}, "
                f"ISBN: {self.isbn}, "
                f"Status_pinjaman: {status_dipinjam}")

#======================== CLASS MEMBER =================================
class Member:
    def __init__(self, nim, nama, email):
        self.nim = nim
        self.nama = nama
        self.email = email
        self.daftar_pinjaman = []
    
    def __str__(self):
        if self.daftar_pinjaman:
            judul_buku = ",".join([buku.judul for buku in self.daftar_pinjaman])
        else:
            judul_buku = "Tidak ada buku yang dipinjam"
        return (f"Nama:{self.nama}, Nim: {self.nim}, Email: {self.email}, Buku Dipinjam: [{judul_buku}]")

#========================= CLASS PUSTAKA ================================
class Pustaka:
    def __init__(self):
        self.daftar_buku = []
        self.daftar_member = {}

# Bagian untuk Menambahkan Member
    def add_member(self, member):
        if member.nim in self.daftar_member:
            print(f"Nim {member.nim} sudah tersedia")
            return
        self.daftar_member[member.nim] = member
        print(f"Member '{member.nama}' Berhasil ditambahkan.")

# Bagian untuk Mengecek Member
    def list_daftar_member(self):
        if not self.daftar_member:
            print("Belum ada member terdaftar")
            return
        for member in self.daftar_member.values():
            print(member)

# Bagian untuk Memperbarui data Member
    def update_member(self, nim, nama=None, email=None):
        if nim not in self.daftar_member:
            print(f"Member dengan NIM '{nim}' tidak ditemukan:")
            return
        if nama:
            self.daftar_member[nim].nama = nama
        if email:
            self.daftar_member[nim].email = email
        print(f"Member dengan NIM '{nim}' diperbarui.")

# Bagian untuk Menghapus Member
    def delete_member(self, nim):
        if nim in self.daftar_member:
            del self.daftar_member[nim]
            print(f"Member dengan NIM {nim} berhasil dihapus.")
        else:
            print('Member tidak ditemukan.')

# Bagian untuk Menambahkan buku
    def add_buku(self, buku):
        self.daftar_buku.append(buku)
        print(f"Buku '{buku.judul}' Telah ditambahkan.")

# Bagian untuk Melihat list buku
    def list_buku(self):
        if not self.daftar_buku:
            print('Pustaka kosong')
            return
        for buku in self.daftar_buku:
            print(buku)

# Bagian untuk Meminjam buku
    def borrow_buku(self, isbn, nim):
        if nim not in self.daftar_member:
            print(f'NIM {nim} tidak ditemukan')
            return
        
        member = self.daftar_member[nim]
        
        for buku in self.daftar_buku:
            if buku.isbn == isbn:
                if not buku.status_pinjaman:
                    buku.status_pinjaman = True
                    buku.dipinjam_oleh = nim
                    
                    member.daftar_pinjaman.append(buku)
                    
                    print(f"Berhasil! {member.nama} meminjam '{buku.judul}'.")
                else:
                    print(f"Maaf, buku '{buku.judul}' sedang dipinjam orang lain.")
                return 
        
        print("Buku dengan ISBN tersebut tidak ditemukan.")

# Bagian untuk Mengembalikan buku 
    def return_buku(self, isbn, nim):
        if nim not in self.daftar_member:
            print(f"NIM {nim} tidak ditemukan.")
            return

        member = self.daftar_member[nim]

        for buku in self.daftar_buku:
            if buku.isbn == isbn:
                if buku.status_pinjaman and buku.dipinjam_oleh == nim:
                    buku.status_pinjaman = False
                    buku.dipinjam_oleh = None
                    
                    member.daftar_pinjaman.remove(buku)
                    
                    print(f"Terima kasih {member.nama}, buku '{buku.judul}' telah kembali.")
                else:
                    print("Gagal: Member ini tidak tercatat meminjam buku tersebut.")
                return 
        
        print("Buku dengan ISBN tersebut tidak ditemukan.")


#====================DATA PENGUJIAN======================

# Membuat data buku untuk class Buku
buku1 = Buku("Atomic Habits", "James Clear", "9780735211292", "2018")
buku2 = Buku("The 7 Habits of Highly Effective People", "Stephen R. Covey", "9781982137274", "1988")
buku3 = Buku("Think and Grow Rich", "Napoleon Hill", "9781585424337", "1937")
buku4 = Buku("You are a Badass", "Jen Sincero", "9780762447695", "2013")

# Menampilkan informasi detail buku1   #Ini yang bakal keluar
print(buku1)#                           Judul: Atomic Habits, Penulis: James Clear, ISBN: 9780735211292, Status_pinjaman: Tidak

print()

# Membuat objek utama 'pustaka' untuk mengelola seluruh sistem
pustaka = Pustaka()

# Memasukkan data buku yang sudah dibuat sebelumnya ke dalam daftar_buku di pustaka    #Ini yang bakal keluar
pustaka.add_buku(buku1)                                                                 #Buku 'Atomic Habits' Telah ditambahkan.
pustaka.add_buku(buku2)#                                                                 Buku 'The 7 Habits of Highly Effective People' Telah ditambahkan.
pustaka.add_buku(buku3)#                                                                 Buku 'Think and Grow Rich' Telah ditambahkan.
pustaka.add_buku(buku4)#                                                                 Buku 'You are a Badass' Telah ditambahkan.

# Menambahkan buku baru secara langsung
pustaka.add_buku(Buku("Learn Java", "Jane Doe", "12345678", "2000"))#                    Buku 'Learn Java' Telah ditambahkan.

print()

# Menampilkan semua koleksi buku yang ada di dalam pustaka  #Ini yang bakal keluar
pustaka.list_buku()                                         #Judul: Atomic Habits, Penulis: James Clear, ISBN: 9780735211292, Status_pinjaman: Belum dipinjam siapapun
#                                                            Judul: The 7 Habits of Highly Effective People, Penulis: Stephen R. Covey, ISBN: 9781982137274, Status_pinjaman: Tidak
#                                                            Judul: Think and Grow Rich, Penulis: Napoleon Hill, ISBN: 9781585424337, Status_pinjaman: Belum dipinjam siapapun
#                                                            Judul: You are a Badass, Penulis: Jen Sincero, ISBN: 9780762447695, Status_pinjaman: Belum dipinjam siapapun
#                                                            Judul: Learn Java, Penulis: Jane Doe, ISBN: 12345678, Status_pinjaman: Belum dipinjam siapapun

print()

# Mendaftarkan member baru ke dalam daftar_member                   #Ini yang bakal keluar
pustaka.add_member(Member("999", "Azzam", "Azzam@gmail.com"))       #Member 'Azzam' Berhasil ditambahkan.
pustaka.add_member(Member("888", "Turas", "Turas@gmail.com"))       #Member 'Turas' Berhasil ditambahkan.

print() 

# Menampilkan daftar member yang sudah terdaftar    #Ini yang bakal keluar
pustaka.list_daftar_member()                        #Nama:Azzam, Nim: 999, Email: Azzam@gmail.com
#                                                   Nama:Turas, Nim: 888, Email: Turas@gmail.com

print()

# Mengubah data member berdasarkan NIM                                 #Ini yang bakal keluar
pustaka.update_member("999", nama="Zahid", email="Zahid@gmail.com")    #Member dengan NIM '999' diperbarui.
pustaka.update_member("888", email="Maut@gmail.com")                   #Member dengan NIM '888' diperbarui.

print()

# Menampilkan daftar member setelah update      #Ini yang bakal keluar
pustaka.list_daftar_member()                    #Nama:Zahid, Nim: 999, Email: Zahid@gmail.com,
#                                               Nama:Turas, Nim: 888, Email: Maut@gmail.com

print() 

# Mencoba menghapus member dengan NIM '999'     Ini yang bakal keluar:
pustaka.delete_member('999')                    #Member dengan NIM 999 berhasil dihapus.

print() 

# Menampilkan daftar member setelah proses penghapusan data diatas  Ini yang bakal keluar:
pustaka.list_daftar_member()                                        #Nama:Turas, Nim: 888, Email: Maut@gmail.com


print()

#Contoh simpel peminjaman: mencocokkan ISBN buku dengan NIM member    Ini yang bakal keluar:
pustaka.borrow_buku("9780735211292", "999")                          # NIM 999 tidak ditemukan (karena nim 999 udah dihapus)
pustaka.borrow_buku("9781982137274", "888")                          # Berhasil! Turas meminjam 'The 7 Habits of Highly Effective People'.
pustaka.borrow_buku("9780735211292", "888")                          # Maaf, buku 'Atomic Habits' sedang dipinjam orang lain.

print()

#Contoh simpel pengembalian buku            Ini yang bakal keluar:
pustaka.return_buku("9780735211292", "999") # NIM 999 tidak ditemukan (karena nim 999 udah dihapus)
pustaka.return_buku("9781982137274", "888") # Turas mengembalikan buku
pustaka.return_buku("9780735211292", "888") # Gagal: member ini tidak meminjam buku tersebut
