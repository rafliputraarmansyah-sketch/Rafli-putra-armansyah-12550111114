import unittest
from bank import BankAccount

class TestBankAccountTheUltimate(unittest.TestCase):
    
    def setUp(self):
        """Menyiapkan objek untuk setiap tes."""
        self.acc = BankAccount("Rafli", 1000.0)

    # --- KELOMPOK 1: EQUALITY (PERSAMAAN) ---
    def test_equality_methods(self):
        self.assertEqual(self.acc.owner, "Rafli")
        self.assertNotEqual(self.acc.balance, 5000)

    # --- KELOMPOK 2: BOOLEAN (LOGIKA BENAR/SALAH) ---
    def test_boolean_methods(self):
        self.assertTrue(self.acc.balance > 0)
        self.assertFalse(self.acc.owner == "Budi")

    # --- KELOMPOK 3: MEMBERSHIP (KEANGGOTAAN) ---
    def test_membership_methods(self):
        vips = ["Rafli", "Admin", "Manager"]
        self.assertIn(self.acc.owner, vips)
        self.assertNotIn("Zaki", vips)

    # --- KELOMPOK 4: MATHEMATICAL (PERBANDINGAN ANGKA) ---
    def test_comparison_methods(self):
        self.assertGreater(self.acc.balance, 500)
        self.assertLess(self.acc.balance, 1500)
        self.assertGreaterEqual(self.acc.balance, 1000)
        self.assertLessEqual(self.acc.balance, 1000)

    # --- KELOMPOK 5: FLOATING POINT (PRESISI) ---
    def test_precision_methods(self):
        self.acc.deposit(0.1)
        self.acc.deposit(0.2)
        # 1000 + 0.1 + 0.2 = 1000.3
        self.assertAlmostEqual(self.acc.balance, 1000.3, places=1)

    # --- KELOMPOK 6: EXCEPTIONS (VALIDASI ERROR) ---
    def test_exception_methods(self):
        # Cek Error Nilai (ValueError)
        with self.assertRaises(ValueError):
            BankAccount("", 1000) # Nama kosong
        with self.assertRaises(ValueError):
            BankAccount("12345", 1000) # Nama angka
        with self.assertRaises(ValueError):
            self.acc.withdraw(99999) # Saldo kurang
        
        # Cek Error Tipe Data (TypeError)
        with self.assertRaises(TypeError):
            self.acc.deposit("seratus") # Input huruf
        with self.assertRaises(TypeError):
            BankAccount("Rafli", "kosong") # Saldo awal huruf

    # --- KELOMPOK 7: IDENTITY & NONE (KEBERADAAN OBJEK) ---
    def test_identity_methods(self):
        # assertIsInstance: Cek apakah objek buatan kelas BankAccount
        self.assertIsInstance(self.acc, BankAccount)
        # assertIsNotNone: Cek apakah objek berhasil dibuat
        self.assertIsNotNone(self.acc)
        # assertIs: Cek identitas objek di memori
        copy_acc = self.acc
        self.assertIs(self.acc, copy_acc)

    # --- TAMBAHAN: TEST UNTUK __STR__ ---
    def test_string_representation(self):
        self.assertEqual(str(self.acc), "BankAccount(Owner: Rafli, Balance: 1000.0)")

if __name__ == '__main__':
    unittest.main()