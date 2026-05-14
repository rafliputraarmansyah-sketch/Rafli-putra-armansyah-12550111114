
class MoveMixin:
    """Menangani pergerakan horizontal karakter."""
    def move_left(self):
        # Ambil speed karakter, kalau gak ada defaultnya 5
        speed = getattr(self, 'speed', 5)
        self.x -= speed

    def move_right(self):
        # Gerak ke kanan tinggal tambah koordinat x
        speed = getattr(self, 'speed', 5)
        self.x += speed

class JumpMixin:
    """Menangani logika melompat."""
    def jump(self):
        # Cek dulu lagi di tanah gak, biar gak bisa double jump sembarangan
        if getattr(self, 'on_ground', True):
            # Angka negatif di y berarti loncat ke atas
            self.velocity_y = -15
            self.on_ground = False

class DashMixin:
    """Menangani gerakan cepat (dash) ke arah tertentu."""
    def dash(self, direction=1):
        # direction: 1 (kanan), -1 (kiri). Biar dash-nya sat-set.
        dash_dist = getattr(self, 'dash_speed', 20)
        self.x += (dash_dist * direction)

class AttackMixin:
    """Kumpulan serangan dasar fisik."""
    def punch(self):
        # Animasi atau print buat pukulan standar
        print(f"  [ACTION] {getattr(self, 'name', 'Character')} melancarkan Pukulan!")

    def kick(self):
        # Animasi atau print buat tendangan standar
        print(f"  [ACTION] {getattr(self, 'name', 'Character')} melancarkan Tendangan!")

class HealthMixin:
    """Logika manajemen HP. Bisa dicampur ke karakter mana aja."""
    def take_damage(self, damage):
        # Kalo lagi block (tahan), damage dipotong setengah (modularitas!)
        if getattr(self, 'is_blocking', False):
            damage //= 2
            print(f"  [GUARD] DEFENDED! {self.name} menahan serangan. Damage berkurang: {damage}")
        
        # Kurangi HP, jangan sampe HP-nya jadi minus (mentok di 0)
        self.hp -= damage
        if self.hp < 0: self.hp = 0
        print(f"  [STATUS] HP {self.name} sekarang: {self.hp}")
    
    def heal(self, amount):
        # Buat nambah darah
        self.hp += amount
        print(f"  [STATUS] {self.name} memulihkan HP sebesar {amount}!")

class BlockMixin:
    """Menangani status pertahanan (Gak kena full damage)."""
    def toggle_block(self, status: bool):
        # True buat bertahan, False buat siaga lagi
        self.is_blocking = status
        state = "Bertahan" if status else "Siaga"
        print(f"  [ACTION] {self.name} sekarang dalam mode {state}.")

class UltimateSkillMixin:
    """Serangan spesial kalau lagi sekarat (Rage Art)."""
    def execute_ultimate(self, target):
        # Syaratnya HP harus di bawah 35 baru bisa aktif
        if self.hp < 35: 
            print(f"  !!! CRIMSON OVERDRIVE !!!")
            print(f"  [ULTIMATE] {self.name} mengeluarkan energi penuh ke {target.name}!")
            target.take_damage(50) # Damage-nya gede banget (50)
        else:
            # Pengingat kalau belum bisa ulti
            print(f"  [SYSTEM] Energi {self.name} tidak cukup untuk Ultimate (HP > 35).")

class AnalyticalTraitMixin:
    """Kemampuan pasif buat karakter yang pinter/analitis."""
    def analyze_enemy(self, enemy):
        # Nambahin buff defense setelah analisa musuh
        print(f"  [TRAIT] {self.name} sedang menganalisis pola serangan {enemy.name}...")
        self.defense_multiplier = 1.5
        print(f"  [SYSTEM] Analisis selesai. Pertahanan {self.name} meningkat!")