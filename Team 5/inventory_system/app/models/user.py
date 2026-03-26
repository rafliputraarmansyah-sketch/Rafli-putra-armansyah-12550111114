class User:
    def __init__(self, username, password, role):
        # 1. SETUP DATA: Simpan identitas & kunci akses secara rahasia (Private)
        self.__username = username
        self.__role = role
        self.__password_benar = password 

    # 2. JENDELA BACA (Getter): Bisa melihat data tapi dilarang mengubahnya langsung
    @property
    def username(self): 
        return self.__username
    
    @property
    def role(self): 
        return self.__role

    # 3. FUNGSI LOGIN: Gerbang utama untuk mengecek izin masuk (Validasi)
    def login(self, password_input):
        # Cek apakah kunci yang dimasukkan cocok dengan yang disimpan
        if password_input == self.__password_benar:
            print(f"\n[SISTEM] User '{self.__username}' ({self.__role}) berhasil masuk.")
            return True # Izin diberikan
        else:
            print("\n[ERROR] Password salah! Akses ditolak.")
            return False # Izin ditolak