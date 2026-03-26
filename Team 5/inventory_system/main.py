# ==============================================================================
# FILE: main.py (SIMULASI TOTAL & JELAS - TEAM 5)
# ==============================================================================

from app.services.inventory_service import InventoryService
from app.models.product import Category, ElectronicProduct, Buku, Pakaian, Aksesoris
from app.models.location import Warehouse
from app.models.transaction import StockInTransaction, StockOutTransaction
from app.models.price import WholesalePrice # Fitur Strategi Harga Grosir

# --- 1. KELAS USER (KEAMANAN) ---
class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def login(self, password):
        """Mengecek akses masuk admin."""
        # Tetap menggunakan password admin123 sesuai permintaanmu
        if password == "admin123":
            print(f"\n[LOGIN] Admin '{self.username}' Sudah masuk.")
            return True
        return False

def main():
    print("=== [SIMULASI SISTEM INVENTARIS LENGKAP - TEAM 5] ===\n")

    # --- SKENARIO 1: LOGIN ---
    # Nama admin tetap RAFLI sesuai kodemu
    admin = User("RAFLI", "Administrator")
    admin.login("admin123") 

    # --- SKENARIO 2: PERSIAPAN Insfasruktur---
    service = InventoryService()
    # Pastikan 'capacity' di sini dikirim ke Warehouse
    gudang = Warehouse("WH-01", "Gudang Utama", capacity=50)
    kat = Category("General")

    # --- SKENARIO 3: DEFINISI BARANG (INHERITANCE) ---
    p1 = ElectronicProduct("B001", "Laptop ASUS", 10000000, kat, 24, 10)
    p2 = Buku("B002", "Filosofi Teras", 100000, kat, "Henry M.", 20)
    p3 = Pakaian("B003", "Kaos Polos", 100000, kat, "L", 15)
    p4 = Aksesoris("B004", "Jam Tangan", 500000, kat, 5)

    service.add_product(p1); service.add_product(p2)
    service.add_product(p3); service.add_product(p4)

    # --- SKENARIO 4: SIMULASI HARGA GROSIR (WHOLESALEPRICE) ---
    print("\n--- [Untuk Ngecek Harga Barang yang Grosir] ---")
    strategi_grosir = WholesalePrice(p3.price, 20) 
    jumlah_beli = 10
    total_bayar = strategi_grosir.calculate_total(jumlah_beli)
    
    print(f"Barang      : {p3.name}") 
    print(f"Harga Ecer  : {strategi_grosir.format_rupiah()}")
    print(f"Beli Banyak : {jumlah_beli} unit")
    print(f"Total Bayar : Rp{total_bayar:,.0f} (Setelah diskon 20%)")

    # --- SKENARIO 5: SIMULASI DISKON MIXIN (BEFORE VS AFTER) ---
    print("\n--- [Untuk Ngecek Harga Diskon] ---")
    harga_asli = p1.price
    harga_promo = p1.get_discounted_price(15) 
    
    print(f"Barang      : {p1.name}")
    print(f"Harga Awal  : Rp{harga_asli:,.0f}")
    print(f"Setelah Diskon 15%: Rp{harga_promo:,.0f}")
    p1.price = harga_promo 

    # --- SKENARIO 6: TRANSAKSI (GUDANG & STOK) ---
    # Menjalankan transaksi melalui service agar tercatat di LOG
    service.execute_transaction(StockInTransaction(p1, 5, gudang))
    service.execute_transaction(StockOutTransaction(p3, 2))

    # --- SKENARIO 7: LAPORAN AKHIR (PAJAK PPN 11%) ---
    print("\n" + "="*95)
    print(f"{'LAPORAN FINAL TEAM 5 (OTOMATIS PAJAK PPN 11%)':^95}")
    print("="*95)
    for item in service.get_all_products():
        print(item.get_details())
    print("-" * 95)

    # --- SKENARIO 8: RIWAYAT (LOGGABLE MIXIN) ---
    print("\nRIWAYAT TRANSAKSI (LOG):")
    for log in service.get_transaction_history():
        print(f"- {log}")

if __name__ == "__main__":
    main()