class BankAccount:
    def __init__(self, owner, balance=0):
        # Validasi Nama: Tidak boleh kosong, harus teks, tidak boleh angka saja
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("Nama pemilik harus berupa teks dan tidak boleh kosong")
        if owner.strip().isdigit():
            raise ValueError("Nama pemilik tidak boleh hanya berisi angka")
        
        # Validasi Saldo Awal: Harus angka
        if not isinstance(balance, (int, float)):
            raise TypeError("Saldo awal harus berupa angka")
        
        self.owner = owner.strip()
        self.balance = float(balance)
    
    def deposit(self, amount):
        if not isinstance(amount, (int, float)):
            raise TypeError("Jumlah setoran harus berupa angka")
        if amount <= 0:
            raise ValueError("Jumlah setoran harus lebih dari nol")
        
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if not isinstance(amount, (int, float)):
            raise TypeError("Jumlah penarikan harus berupa angka")
        if amount <= 0:
            raise ValueError("Jumlah penarikan tidak valid")
        if amount > self.balance:
            raise ValueError("Saldo tidak cukup")
        
        self.balance -= amount
        return self.balance

    def get_balance(self):
        return self.balance

    def __str__(self):
        return f"BankAccount(Owner: {self.owner}, Balance: {self.balance})"