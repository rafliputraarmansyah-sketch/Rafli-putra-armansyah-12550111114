import time
from models.character import Hayato, Yoru
from models.attacks import Punch, Kick, SpecialAttack

def arena_crimson_simulation(p1, p2):
    """
    Fungsi utama untuk mensimulasikan pertarungan.
    Mendemonstrasikan SUBTYPING: Menerima objek apa pun yang merupakan 
    turunan dari BaseCharacter.
    """
    print(f"=== ARENA CRIMSON TERBUKA ===")
    print(f"PETARUNG 1: {p1.name} (LIGHT)")
    print(f"PETARUNG 2: {p2.name} (DARK)")
    print("-" * 30)
    print("READY... FIGHT!\n")

    # Daftar serangan Hayato (P1) dirancang agar Yoru K.O. di ronde 4
    serangan_hayato = [
        Punch(),                            # Ronde 1: Damage 10
        Kick(),                             # Ronde 2: Damage 15
        SpecialAttack("Crimson Slash", 20, 1.5), # Ronde 3: Damage 30
        SpecialAttack("FINAL BLOW", 50, 2)       # Ronde 4: Damage 100 (Finisher)
    ]

    # Daftar serangan Yoru (P2)
    serangan_yoru = [Punch(), Kick(), Punch(), Kick()]

    for ronde in range(1, 5):
        print(f">>> RONDE {ronde}")
        
        # --- Giliran Hayato Menyerang ---
        aksi_h = serangan_hayato[ronde-1]
        aksi_h.execute(p1, p2) # Mendemonstrasikan Subtyping pada parameter execute 
        
        if p2.hp <= 0:
            p2.hp = 0 # Memastikan HP tidak minus agar tampilan bagus
            break

        # --- Giliran Yoru Menyerang ---
        aksi_y = serangan_yoru[ronde-1]
        aksi_y.execute(p2, p1)
        
        if p1.hp <= 0:
            p1.hp = 0
            break
        
        # Tampilkan Status HP setelah setiap ronde
        print(f"Status: {p1.name} [{p1.hp} HP] | {p2.name} [{p2.hp} HP]")
        print("-" * 20)
        time.sleep(1) # Jeda agar simulasi mudah diikuti

    # --- PENGUMUMAN PEMENANG ---
    print("\n" + "=" * 30)
    if p2.hp <= 0:
        print(f" K.O.! {p2.name} TELAH DIKALAHKAN.")
        print(f" PEMENANG: {p1.name} (HP Tersisa: {p1.hp})")
    else:
        print(f" K.O.! {p1.name} TELAH DIKALAHKAN.")
        print(f" PEMENANG: {p2.name} (HP Tersisa: {p2.hp})")
    print("=" * 30)

if __name__ == "__main__":
    # 1. Instansiasi Objek Karakter
    # Membuktikan penggunaan SUPER() di konstruktor
    pahlawan = Hayato() 
    rival = Yoru()

    # 2. Jalankan Simulasi
    arena_crimson_simulation(pahlawan, rival)