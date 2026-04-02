class User:
    def __init__(self, username, password, role):
        # Logika: Menggunakan double underscore (__) agar data penting seperti password 'terkunci' di dalam kelas (Enkapsulasi).
        # 1. SETUP DATA: Rahasia (Private)
        self.__username = username
        self.__role = role
        self.__password_benar = password 

    # 2. JENDELA BACA (Getter)
    # Logika: Memberikan izin akses 'baca' saja bagi pihak luar agar bisa melihat data tanpa bisa mengubahnya sembarangan.
    @property
    def username(self): 
        return self.__username
    
    @property
    def role(self): 
        return self.__role

    # 3. FUNGSI LOGIN
    # Logika: Pengecekan keamanan. Jika kunci (password) yang dimasukkan cocok dengan data rahasia, akses diberikan (True).
    def login(self, password_input):
        if password_input == self.__password_benar:
            print(f"\n[SISTEM] Login Berhasil! Selamat datang, {self.__username}.")
            return True 
        else:
            print("\n[ERROR] Password salah! Akses untuk user ini ditolak.")
            return False 

    # 4. POLYMORPHISM: Method dasar yang bisa diubah oleh kelas anak
    # Logika: Menyediakan kerangka info umum yang nantinya bisa 'dimodifikasi' oleh jabatan yang lebih spesifik.
    def get_info(self):
        """Menampilkan profil singkat user."""
        return f"User: {self.__username} | Peran: {self.__role}"


# --- 5. KELAS ANAK: CASHIER (Penerapan Inheritance & Polymorphism) ---
# Logika: Cashier mewarisi semua sifat User (bisa login, punya username) tanpa perlu menulis ulang kodenya dari nol.
class Cashier(User):
    def __init__(self, username, password, cashier_id):
        # Logika: Mengoper data ke kelas induk (User) untuk diproses, sambil menetapkan peran default sebagai "Kasir Swalayan".
        # Memanggil __init__ milik User.
        super().__init__(username, password, role="Kasir Swalayan")
        self.__cashier_id = cashier_id 

    @property
    def cashier_id(self):
        # Logika: Menambahkan identitas unik yang hanya dimiliki oleh seorang Kasir, bukan User biasa.
        return self.__cashier_id

    # OVERRIDE: Mengubah isi get_info khusus untuk Kasir
    # Logika: Polimorfisme beraksi. Kita mengubah isi get_info agar lebih lengkap dengan mencantumkan ID Pegawai.
    def get_info(self):
        """Implementasi Polimorfisme: Menambahkan ID Kasir di profil."""
        return f"User: {self.username} | Peran: {self.role} | ID Pegawai: {self.__cashier_id}"

    def sambut_pelanggan(self):
        # Logika: Fitur spesial. Hanya objek Kasir yang bisa melakukan ini; user biasa tidak punya akses ke fungsi sapaan ini.
        """Method unik: Hanya kasir yang bisa menyapa seperti ini."""
        return f"\n[KASIR - {self.username}]: Selamat datang di Swalayan Team 5! Ada kartu membernya?"