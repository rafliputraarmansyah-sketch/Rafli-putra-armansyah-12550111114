from models.base import BaseAttack

# ==========================================
# CONCRETE BASE ATTACK (Inheritance)
# ==========================================

class PhysicalAttack(BaseAttack): # Warisin sifat dari BaseAttack 
    """
    Kelas dasar untuk semua serangan fisik.
    """
    def __init__(self, name, power):
        # Pakai super() biar atribut 'name' & 'power' dikenali bapaknya 
        super().__init__()
        self.name = name
        self.power = power

    def execute(self, attacker, target):
        """
        Mendemonstrasikan SUBTYPING:
        'attacker' & 'target' bisa diisi siapa aja asal turunan BaseCharacter.
        """
        print(f"  [ATTACK] {attacker.name} menggunakan {self.name}!")
        damage = self.get_damage()
        target.take_damage(damage) # Kurangi darah target lewat HealthMixin

    def get_damage(self):
        return self.power


# ==========================================
# ATTACK SUBTYPES (Subtyping & Specialization)
# ==========================================

class Punch(PhysicalAttack): # Level 3: Anak dari PhysicalAttack (Subtype)
    def __init__(self):
        # Set otomatis nama & damage buat Pukulan 
        super().__init__(name="Pukulan (Punch)", power=10)

class Kick(PhysicalAttack): # Level 3: Anak dari PhysicalAttack (Subtype)
    def __init__(self):
        # Set otomatis nama & damage buat Tendangan 
        super().__init__(name="Tendangan (Kick)", power=15)

class SpecialAttack(PhysicalAttack): # Level 3: Serangan khusus pake multiplier
    """
    Serangan spesial yang memiliki multiplier damage.
    """
    def __init__(self, name, power, multiplier):
        # Kirim nama & power ke bapaknya (PhysicalAttack) 
        super().__init__(name, power)
        self.multiplier = multiplier

    def get_damage(self):
        # Hitung damage pake pengali biar makin sakit
        return int(self.power * self.multiplier)