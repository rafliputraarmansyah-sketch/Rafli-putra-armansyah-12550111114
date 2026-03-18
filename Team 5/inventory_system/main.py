from app.services.inventory_service import InventoryService
from app.models.product import Product, Category, ElectronicProduct, Buku, Pakaian, Aksesoris
from app.models.location import Warehouse
from app.models.transaction import StockInTransaction, StockOutTransaction

def tampilkan_jenis_produk():
    """Menampilkan daftar kategori barang yang tersedia."""
    print("\n" + "-"*30)
    print("      PILIH JENIS BARANG")
    print("-"*30)
    print("1. Electronic      3. Pakaian")
    print("2. Buku            4. Aksesoris")
    print("5. Umum (Tanpa Kategori)")
    print("-" * 30)

def input_validasi(prompt, tipe_data=str, hanya_angka=False):
    """Memvalidasi input sesuai tipe dan memastikan ID hanya angka."""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                raise ValueError("Input tidak boleh kosong!")
            
            if hanya_angka and not user_input.isdigit():
                raise ValueError("Input ini harus berupa angka!")
                
            return tipe_data(user_input)
        except ValueError as e:
            print(f"❌ KESALAHAN INPUT: {e}")

def main():
    service = InventoryService()
    kat_umum = Category("General")
    # Inisialisasi Gudang untuk transaksi masuk
    gudang_pusat = Warehouse("WH-01", "Gudang Utama", capacity=50)

    while True:
        print("\n" + "="*45)
        print("      SISTEM INVENTARIS - TEAM 5")
        print("="*45)
        print(" 1. Tambah Barang Baru")
        print(" 2. Lihat Laporan Lengkap")
        print(" 3. Update Informasi Barang")
        print(" 4. Hapus Barang")
        print(" 5. Transaksi Barang MASUK")
        print(" 6. Transaksi Barang KELUAR")
        print(" 7. Lihat Riwayat (Log)")
        print(" 0. Keluar")
        
        pilihan = input("\nPilih menu: ")

        # --- 1. TAMBAH BARANG ---
        if pilihan == "1":
            try:
                tampilkan_jenis_produk()
                while True:
                    tipe = input_validasi("Pilih nomor jenis barang (1-5): ", int)
                    if 1 <= tipe <= 5: break
                    print("❌ Pilih angka antara 1 sampai 5!")
                
                pid = input_validasi("ID Produk (Angka): ", hanya_angka=True)
                nama = input_validasi("Nama Produk: ")
                harga = input_validasi("Harga: ", float)
                stok = input_validasi("Stok Awal: ", int)

                if tipe == 1:
                    garansi = input_validasi("Masa Garansi (Bulan): ", int)
                    new_item = ElectronicProduct(pid, nama, harga, kat_umum, garansi, stok)
                elif tipe == 2:
                    penulis = input_validasi("Nama Penulis: ")
                    new_item = Buku(pid, nama, harga, kat_umum, penulis, stok)
                elif tipe == 3:
                    # REVISI: VALIDASI UKURAN PAKAIAN (S/M/L/XL)
                    while True:
                        ukuran = input_validasi("Ukuran (S/M/L/XL): ").upper()
                        if ukuran in ['S', 'M', 'L', 'XL']: break
                        print("❌ KESALAHAN: Ukuran hanya boleh S, M, L, atau XL!")
                    new_item = Pakaian(pid, nama, harga, kat_umum, ukuran, stok)
                elif tipe == 4:
                    new_item = Aksesoris(pid, nama, harga, kat_umum, stok)
                else:
                    new_item = Product(pid, nama, harga, kat_umum, stok)

                service.add_product(new_item)
                print(f"✅ Sukses: {nama} terdaftar sebagai {new_item.__class__.__name__}.")
            except (TypeError, ValueError, KeyError) as e:
                print(f"⚠️ GAGAL TAMBAH: {e}")

        # --- 2. LIHAT BARANG (REVISI: LAPORAN LEBIH DETAIL) ---
        elif pilihan == "2":
            print("\n" + "="*70)
            print(f"{'NO':<3} | {'DETAIL PRODUK (ID, NAMA, HARGA, INFO KHUSUS, STOK)':<60}")
            print("-" * 70)
            try:
                items = service.get_all_products()
                for i, p in enumerate(items, 1):
                    # Memanggil get_details() yang sudah lengkap dari product.py
                    print(f"{i:<3} | {p.get_details()}")
            except IndexError as e:
                print(f"⚠️ INFORMASI: {e}")

        # --- 3. UPDATE BARANG (REVISI: LOOPING INPUT ID & HARGA) ---
        elif pilihan == "3":
            while True:
                pid = input("\nMasukkan ID yang akan diupdate (atau ketik 'b' untuk batal): ").strip()
                if pid.lower() == 'b': break
                
                if service.exists(pid):
                    nama_baru = input("Nama baru (Kosongkan jika tetap): ")
                    
                    # Looping validasi untuk harga baru
                    harga_baru = None
                    while True:
                        h_raw = input("Harga baru (Kosongkan jika tetap): ").strip()
                        if not h_raw: break
                        try:
                            harga_baru = float(h_raw)
                            break
                        except ValueError:
                            print("❌ KESALAHAN: Harga harus berupa angka!")
                    
                    service.update_product(pid, new_name=nama_baru or None, new_price=harga_baru)
                    print(f"✅ Berhasil diupdate.")
                    break # Keluar dari loop ID jika sukses
                else:
                    print(f"❌ KESALAHAN: ID {pid} tidak ditemukan! Silakan coba lagi.")

        # --- 4. HAPUS BARANG (REVISI: LOOPING INPUT ID) ---
        elif pilihan == "4":
            while True:
                pid = input("\nMasukkan ID yang akan dihapus (atau ketik 'b' untuk batal): ").strip()
                if pid.lower() == 'b': break
                
                if service.exists(pid):
                    try:
                        service.delete_product(pid)
                        break # Keluar dari loop jika berhasil hapus
                    except KeyError as e:
                        print(f"⚠️ GAGAL: {e}")
                else:
                    print(f"❌ KESALAHAN: ID {pid} tidak terdaftar! Silakan coba lagi.")

        # --- 5. TRANSAKSI MASUK ---
        elif pilihan == "5":
            try:
                pid = input_validasi("ID Produk: ", hanya_angka=True)
                produk = service.get_product_by_id(pid)
                if not produk: raise KeyError("ID Produk tidak ditemukan!")
                
                qty = input_validasi(f"Jumlah {produk.name} masuk: ", int)
                trx = StockInTransaction(produk, qty, gudang_pusat)
                
                if service.execute_transaction(trx):
                    print(f"✅ Stok berhasil masuk ke {gudang_pusat.name}")
                else:
                    print("❌ Gagal: Kapasitas gudang penuh!")
            except (KeyError, ValueError) as e:
                print(f"⚠️ ERROR TRANSAKSI: {e}")

        # --- 6. TRANSAKSI KELUAR ---
        elif pilihan == "6":
            try:
                pid = input_validasi("ID Produk: ", hanya_angka=True)
                produk = service.get_product_by_id(pid)
                if not produk: raise KeyError("ID Produk tidak ditemukan!")
                
                qty = input_validasi(f"Jumlah {produk.name} keluar: ", int)
                trx = StockOutTransaction(produk, qty)
                
                if service.execute_transaction(trx):
                    print(f"✅ Stok {produk.name} berhasil dikurangi.")
                else:
                    print(f"❌ Gagal: Stok tidak cukup! (Sisa: {produk.stock})")
            except Exception as e:
                print(f"⚠️ ERROR: {e}")

        # --- 7. LIHAT RIWAYAT ---
        elif pilihan == "7":
            print("\n" + "-"*40)
            print("       RIWAYAT TRANSAKSI")
            print("-"*40)
            logs = service.get_transaction_history()
            if isinstance(logs, list):
                for i, log in enumerate(logs, 1): print(f"{i}. {log}")
            else:
                print(logs)

        elif pilihan == "0":
            print("\n[INFO] Keluar. Terima kasih, Team 5!")
            break

if __name__ == "__main__":
    main()