import unittest
from app.services.inventory_service import InventoryService
from app.models.product import Category, FoodProduct, DrinkProduct
from app.models.location import Warehouse
from app.models.price import RetailPrice, WholesalePrice
from app.models.transaction import StockInTransaction
from app.models.payment import Payment
from app.models.user import Cashier
from app.models.transaction import StockOutTransaction
#Terakhir, kami menerapkan Unit Testing menggunakan library unittest

class TestSistemSwalayan(unittest.TestCase):

    def setUp(self):
        # Logika: Menyiapkan 'panggung' tes. Fungsi ini berjalan otomatis sebelum setiap test case dimulai 
        # agar setiap tes punya data yang bersih (fresh).
        """Inisialisasi environment sebelum setiap test dijalankan."""
        self.service = InventoryService()
        self.kat_food = Category("Makanan")
        self.kat_drink = Category("Minuman")
        
        # Setup Lokasi & Produk
        self.gudang = Warehouse("WH-01", "Gudang Utama", capacity=50)
        self.p_eceran = FoodProduct("F001", "Indomie", RetailPrice(3500), self.kat_food, "2026-01-01")
        self.p_grosir = DrinkProduct("D001", "Susu", WholesalePrice(10000, 10, min_qty=10), self.kat_drink, "1L")
        
        # Daftarkan produk ke service
        self.service.add_product(self.p_eceran)
        self.service.add_product(self.p_grosir)

    # --- 1. TESTING HARGA & DISKON (price.py & mixins.py) ---
    def test_retail_price_calculation(self):
        # Logika: Memastikan perkalian harga eceran tidak salah hitung.
        """Pastikan harga eceran dihitung dengan benar (tanpa diskon grosir)."""
        # Menggunakan name mangling _Product__price_obj karena atributnya private.
        total = self.p_eceran._Product__price_obj.calculate_total(5)
        self.assertEqual(total, 17500) # 3500 * 5

    def test_wholesale_price_trigger(self):
        # Logika: Menguji 'ambang batas' harga grosir. Diskon harus menyala saat mencapai min_qty.
        """Pastikan diskon grosir aktif saat mencapai minimal kuantitas."""
        # Harga 10.000, diskon 10% jadi 9.000 jika beli >= 10
        total_grosir = self.p_grosir._Product__price_obj.calculate_total(10)
        self.assertEqual(total_grosir, 90000) # (10.000 - 10%) * 10
        
        # Logika: Memastikan jika beli di bawah batas (misal 5), harga tetap normal (Retail).
        # Jika di bawah 10, harus harga normal
        total_normal = self.p_grosir._Product__price_obj.calculate_total(5)
        self.assertEqual(total_normal, 50000)

    # --- 2. TESTING TRANSAKSI GUDANG (transaction.py & location.py) ---
    def test_stock_in_capacity_validation(self):
        # Logika: Tes keamanan gudang. Sistem harus menolak barang jika total stok melebihi kapasitas rak/gudang.
        """Pastikan tidak bisa restock melebihi kapasitas gudang."""
        # Kapasitas gudang setup di 50 unit
        trx = StockInTransaction(self.p_eceran, 60, self.gudang)
        hasil = trx.execute()
        self.assertFalse(hasil) # Harus gagal (False) karena 60 > 50
        self.assertEqual(self.p_eceran.stock, 0) # Stok produk harus tetap 0 karena transaksi gagal.

    def test_stock_in_success(self):
        # Logika: Memastikan saat barang masuk, baik data di 'Produk' maupun di 'Lokasi' keduanya terupdate secara sinkron.
        """Pastikan stok produk dan kapasitas gudang bertambah saat restock sukses."""
        trx = StockInTransaction(self.p_eceran, 20, self.gudang)
        trx.execute()
        self.assertEqual(self.p_eceran.stock, 20)
        self.assertEqual(self.gudang.current_count, 20)

    # --- 3. TESTING PEMBAYARAN (payment.py) ---
    def test_payment_member_discount(self):
        # Logika: Menguji tumpukan logika (Subtotal -> PPN 11% -> Diskon Member 5%).
        """Pastikan member mendapatkan diskon tambahan 5% setelah PPN."""
        # Berikan stok dulu agar bisa belanja
        self.p_eceran.add_stock(10)
        
        keranjang = [(self.p_eceran, 2)] # Subtotal: 7000
        # Logika Matematika: ((7000 + 11%) - 5%) = 7381.5
        
        bayar = Payment(keranjang, is_member=True)
        _, _, total_akhir = bayar.calculate_total_bill()
        # assertAlmostEqual digunakan karena hasil hitungan diskon biasanya berupa float desimal.
        self.assertAlmostEqual(total_akhir, 7381.5)

    def test_insufficient_payment(self):
        # Logika: Tes keamanan kasir. Jika uang kurang dari total tagihan, sistem wajib memblokir transaksi.
        """Pastikan pembayaran gagal jika uang yang diberikan kurang."""
        self.p_eceran.add_stock(10)
        keranjang = [(self.p_eceran, 1)] # Total setelah PPN: 3885
        bayar = Payment(keranjang, is_member=False)
        
        hasil = bayar.proses_bayar_tunai(2000) # Bayar cuma 2000, padahal butuh 3885.
        self.assertFalse(hasil)

    # --- 4. TESTING AUTH & USER (user.py) ---
    def test_cashier_login(self):
        # Logika: Memastikan enkapsulasi password bekerja. Hanya string yang sama persis yang bisa lewat.
        """Pastikan login kasir hanya berhasil dengan password yang benar."""
        kasir = Cashier("Rafli", "rahasia123", "KSR-01")
        self.assertTrue(kasir.login("rahasia123"))
        self.assertFalse(kasir.login("salah_pass"))

    # --- 5. TESTING INVENTORY SERVICE (inventory_service.py) ---
    def test_inventory_report_value(self):
        # Logika: Memastikan laporan keuangan manajer akurat dengan menjumlahkan seluruh nilai aset barang.
        """Pastikan perhitungan total aset manajer akurat."""
        self.p_eceran.add_stock(10) # Aset: 10 * 3500 = 35.000
        self.p_grosir.add_stock(2)  # Aset: 2 * 10.000 = 20.000
        # Total aset harusnya 55.000
        
        report = self.service.get_inventory_report()
        self.assertIn("Rp55,000", report) # Mengecek apakah angka 55.000 muncul di dalam string laporan.

    def test_negative_price_update(self):
        # Logika: Menguji validasi pada @setter. Harga barang tidak boleh diubah menjadi negatif.
        """Memastikan harga tidak bisa diubah menjadi negatif (Validation Test)"""
        original_price = self.p_eceran.price
        self.p_eceran.price = -5000  # Mencoba merusak data harga.
        self.assertEqual(self.p_eceran.price, original_price) # Sistem harus tetap mempertahankan harga lama.

    def test_stock_out_insufficient(self):
        # Logika: Memastikan integritas data. Tidak boleh membuang barang yang stoknya tidak ada di rak.
        """Memastikan tidak bisa membuang barang (StockOut) lebih banyak dari stok yang ada"""
        self.p_eceran.add_stock(10)
        # Mencoba membuang 15 barang (melebihi stok 10).
        trx = StockOutTransaction(self.p_eceran, 15, self.gudang, "Rusak")
        self.assertFalse(trx.execute()) # Transaksi harus ditolak.

    def test_duplicate_product_id(self):
        # Logika: Menguji integritas database (InventoryService). ID Produk wajib unik (Unique Constraint).
        """Memastikan sistem menolak pendaftaran ID produk yang sama (KeyError)"""
        with self.assertRaises(KeyError):
            # Logika: Mencoba mendaftarkan p_eceran lagi padahal di setUp sudah didaftarkan.
            self.service.add_product(self.p_eceran) 

if __name__ == '__main__':
    unittest.main()