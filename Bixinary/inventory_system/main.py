import os
from app.services.inventory_service import InventoryService
from app.models.product import Category, FoodProduct, DrinkProduct, ToolsProduct
from app.models.location import Warehouse
from app.models.price import RetailPrice, WholesalePrice
from app.models.transaction import StockInTransaction
from app.models.payment import Payment
from app.models.user import User, Cashier
#File ini mensimulasikan seluruh komponen yang sudah dibuat.

# Logika: Fungsi utilitas untuk membersihkan tampilan terminal agar user interface (UI) terlihat profesional.
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print("="*60)
    print(f"{'SISTEM SWALAYAN TEAM 5 - VERSI PRODUKSI':^60}")
    print("="*60)

    # --- 1. INISIALISASI INFRASTRUKTUR ---
    # Logika: Menyiapkan objek service sebagai database pusat dan objek Warehouse sebagai representasi fisik tempat penyimpanan.
    service = InventoryService()
    gudang_utama = Warehouse("WH-01", "Gudang Belakang", capacity=100)
    rak_display = Warehouse("RK-01", "Rak Depan", capacity=50)
    
    kat_food = Category("Makanan")
    kat_drink = Category("Minuman")
    kat_tools = Category("Peralatan")

    # --- 2. REGISTRASI PRODUK (Menggunakan Object Composition untuk Harga) ---
    # Logika: Menerapkan 'Composition' di mana objek Price (Retail/Wholesale) dimasukkan ke dalam objek Product.
    # Produk 1: Makanan dengan Harga Eceran
    p1 = FoodProduct("F001", "Indomie Goreng", RetailPrice(3500), kat_food, "2026-12-01")
    
    # Produk 2: Minuman dengan Harga Grosir (Min. beli 12 diskon 10%)
    # Logika: Menggunakan WholesalePrice sehingga perhitungan total akan otomatis berubah jika mencapai min_qty.
    p2 = DrinkProduct("D001", "Susu Ultra 1L", WholesalePrice(18000, 10, min_qty=12), kat_drink, "1000ml")
    
    # Produk 3: Peralatan
    p3 = ToolsProduct("T001", "Sapu Lantai", RetailPrice(25000), kat_tools, "Plastik")

    # Masukkan ke database sistem
    # Logika: Mendaftarkan objek produk ke dalam InventoryService agar bisa dikelola secara global.
    service.add_product(p1); service.add_product(p2); service.add_product(p3)

    # --- 3. SKENARIO RESTOCK (Barang Masuk ke Gudang) ---
    # Logika: Menjalankan perintah logistik. Di sini terjadi sinkronisasi antara jumlah stok produk dan kapasitas Warehouse.
    print("\n[STEP 1] Melakukan Restock Barang dari Supplier...")
    service.execute_transaction(StockInTransaction(p1, 20, gudang_utama))
    service.execute_transaction(StockInTransaction(p2, 24, rak_display))
    service.execute_transaction(StockInTransaction(p3, 5, rak_display))

    # --- 4. LOGIN KASIR ---
    # Logika: Menerapkan 'Inheritance'. Objek Cashier memiliki semua fungsi User (seperti login) ditambah fungsi unik (sapaan).
    kasir = Cashier("Rafli", "admin123", "KSR-005")
    
    if kasir.login("admin123"):
        # Logika: Menampilkan info kasir yang sudah di-'Override' (Polymorphism) untuk menyertakan ID Kasir.
        print(kasir.get_info())
        print(kasir.sambut_pelanggan())

        # --- 5. SIMULASI BELANJA (KERANJANG) ---
        print("\n[STEP 2] Simulasi Scan Barang di Kasir...")
        #Simulasi Scan Barang dengan barcode
        # Logika: Menjalankan fungsi dari 'Mixin' (FinansialMixin) yang diwarisi oleh produk untuk simulasi visual barcode.
        print(p1.scan_barcode())
        print(p2.scan_barcode())

        # Logika: Mengumpulkan data belanja dalam struktur list of tuples (Produk, Qty) untuk diproses ke modul Payment.
        keranjang_belanja = [
            (p1, 5),  # Beli Indomie 5 bungkus
            (p2, 12), # Beli Susu 12 botol (Logika WholesalePrice akan otomatis aktif di sini)
            (p3, 1)   # Beli Sapu 1 buah
        ]

        # --- 6. PROSES PEMBAYARAN & STRUK ---
        # Logika: Menginisialisasi objek Payment. Karena is_member=True, MemberMixin akan memberikan diskon tambahan 5%.
        proses_bayar = Payment(keranjang_belanja, is_member=True)
        
        print("\n[STEP 3] Memproses Pembayaran Tunai...")
        # Logika: Melakukan validasi total bill vs uang tunai. Jika cukup, stok fisik produk dikurangi.
        if proses_bayar.proses_bayar_tunai(300000):
            # Logika: Finalisasi. Sinkronisasi data ke InventoryService agar database pusat mencatat pengurangan stok.
            # Jika bayar sukses, Update Stok di InventoryService
            service.record_sale(keranjang_belanja)
            
    # --- 7. LAPORAN AKHIR MANAJER ---
    # Logika: Menampilkan status akhir seluruh sistem setelah terjadi transaksi masuk (restock) dan keluar (penjualan).
    print("\n" + "="*60)
    print(f"{'LAPORAN INVENTARIS AKHIR':^60}")
    print("="*60)
    for item in service.get_all_products():
        # Logika: Polimorfisme; memanggil get_details() yang formatnya berbeda-beda tiap kategori produk.
        print(item.get_details())
    
    # Logika: Menghitung nilai rupiah dari seluruh sisa stok sebagai laporan aset bagi pemilik toko.
    print(service.get_inventory_report())

    print("\n[INFO] Riwayat Logistik Gudang:")
    # Logika: Menampilkan log audit dari transaksi StockIn yang dilakukan di awal program.
    for log in service.get_transaction_history():
        print(f"- {log}")

if __name__ == "__main__":
    main()