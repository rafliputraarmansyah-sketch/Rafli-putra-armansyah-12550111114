from datetime import datetime
from app.models.base import AbstractPayment 
from app.models.mixins import FinansialMixin, MemberMixin

# Logika: Kelas Payment 'meminjam' kemampuan dari AbstractPayment (kontrak), 
# FinansialMixin (hitung pajak), dan MemberMixin (hitung diskon member).
class Payment(AbstractPayment, FinansialMixin, MemberMixin):
    def __init__(self, items: list, is_member: bool = False):
        # Logika: Mengunci data transaksi dalam variabel private (__variable) agar tidak bisa diubah sembarangan dari luar.
        self.__items = items # Daftar belanjaan (produk & jumlah)
        self.__is_member = is_member # Status loyalitas pelanggan
        self.__timestamp = datetime.now() # Mencatat waktu presisi saat objek dibuat
        # Logika: Membuat kode unik otomatis berdasarkan waktu (TahunBulanHariJamMenitDetik)
        self.__transaction_id = f"TRX-{self.__timestamp.strftime('%Y%m%d%H%M%S')}"
        self.__uang_diterima = 0
        self.__kembalian = 0

    def calculate_total_bill(self):
        # Logika: Menghitung total belanja kotor (harga x qty) untuk semua item di keranjang.
        subtotal = 0
        for product, qty in self.__items:
            subtotal += product.price * qty
            
        # Logika: Memanggil fungsi hitung_ppn dari FinansialMixin.
        total_pajak = self.hitung_ppn(subtotal)
        total_setelah_pajak = subtotal + total_pajak
        # Logika: Memanggil fungsi hitung_diskon_member dari MemberMixin untuk hasil akhir.
        total_akhir = self.hitung_diskon_member(total_setelah_pajak, self.__is_member)
        
        return subtotal, total_pajak, total_akhir

    def proses_bayar_tunai(self, jumlah_uang):
        """Logika eksekusi pembayaran dengan VALIDASI & EKSEKUSI STOK."""
        
        # --- 1. VALIDASI STOK ---
        # Logika: Cek fisik. Jika ada satu saja barang yang kurang di gudang, gagalkan seluruh transaksi.
        for product, qty in self.__items:
            if product.stock < qty:
                print(f"\n[ERROR] Stok tidak mencukupi!")
                print(f"Barang: {product.name} | Dibutuhkan: {qty} | Tersedia: {product.stock}")
                return False 

        # --- 2. VALIDASI PEMBAYARAN ---
        # Logika: Mengambil total tagihan akhir untuk dibandingkan dengan uang di tangan (cash).
        _, _, total_tagihan = self.calculate_total_bill()
        
        if jumlah_uang < total_tagihan:
            # Logika: Jika uang kurang, berikan informasi selisih kekurangannya.
            print(f"\n[ERROR] Uang Kurang! Dibutuhkan: Rp{total_tagihan - jumlah_uang:,.0f}")
            return False
            
        self.__uang_diterima = jumlah_uang
        self.__kembalian = jumlah_uang - total_tagihan
        
        # --- 3. EKSEKUSI PENGURANGAN STOK ---
        # Logika: Setelah uang dipastikan cukup, barulah kita kurangi stok di database/sistem.
        # Jika uang sudah cukup, kurangi stok barang di sistem secara otomatis
        for product, qty in self.__items:
            product.add_stock(-qty) 
            
        # Logika: Tahap final, jika semua validasi lewat, cetak bukti bayar.
        # Jika semua sukses, cetak struk
        self.print_receipt()
        return True

    def print_receipt(self):
        # Logika: Mengambil ulang data perhitungan untuk ditampilkan di struk.
        subtotal, pajak, total_akhir = self.calculate_total_bill()
        
        # Logika: Mengatur format teks agar rata tengah (^), rata kiri (<), dan rata kanan (>) supaya rapi seperti struk asli.
        print("\n" + "="*45)
        print(f"{'STRUK BELANJA SWALAYAN RAFLI':^45}")
        print(f"{'ID Transaksi: ' + self.__transaction_id:^45}")
        print(f"{self.__timestamp.strftime('%d/%m/%Y %H:%M:%S'):^45}")
        print("-" * 45)
        
        for product, qty in self.__items:
            # Logika: Looping untuk menampilkan setiap baris barang yang dibeli pelanggan.
            # Menggunakan fitur scan_barcode dari FinansialMixin agar struk makin keren
            print(f"{product.name:<20} {qty:>2} x Rp{product.price:>10,.0f}")
            
        print("-" * 45)
        print(f"{'Subtotal':<30} : Rp{subtotal:>10,.0f}")
        print(f"{'PPN (11%)':<30} : Rp{pajak:>10,.0f}")
        
        if self.__is_member:
            # Logika: Menghitung nominal penghematan pelanggan member untuk ditampilkan di struk.
            diskon_member = (subtotal + pajak) * 0.05
            print(f"{'Diskon Member (5%)':<30} : -Rp{diskon_member:>9,.0f}")
            
        print("-" * 45)
        print(f"{'TOTAL AKHIR':<30} : Rp{total_akhir:>10,.0f}")
        print(f"{'BAYAR (TUNAI)':<30} : Rp{self.__uang_diterima:>10,.0f}")
        print(f"{'KEMBALIAN':<30} : Rp{self.__kembalian:>10,.0f}")
        
        print("="*45)
        print(f"{'TERIMA KASIH TELAH BERBELANJA':^45}")
        print("="*45)