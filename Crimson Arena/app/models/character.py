from models.base import BaseCharacter
from models.mixins import (
    MoveMixin, AttackMixin, HealthMixin, BlockMixin, 
    UltimateSkillMixin, AnalyticalTraitMixin
)

# ==========================================
# CONCRETE BASE CLASS (Inheritance)
# ==========================================

# Mixin ditaruh di depan biar logic take_damage() dari HealthMixin yang diprioritaskan (MRO).
class CrimsonFighter(HealthMixin, MoveMixin, AttackMixin, BlockMixin, BaseCharacter):
    """
    Induk utama petarung Crimson Arena. 
    Menerapkan Inheritance (Pewarisan) dari BaseCharacter dan Mixins.
    """
    def __init__(self, name, hp, speed, side):
        # Manggil constructor Bapaknya (BaseCharacter) pake super() biar atributnya ke-set.
        super().__init__(name, hp)
        self.speed = speed
        self.side = side # Identitas faksi: 'Light' atau 'Dark'
        self.x = 0
        self.on_ground = True
        self.is_blocking = False

    def take_damage(self, amount):
        """Implementasi wajib method abstrak dari BaseCharacter."""
        # Oper tugas pengurangan HP ke HealthMixin pake super().
        super().take_damage(amount)

    def move(self):
        # Method dari BaseCharacter yang dikasih isi (Concrete Method)
        print(f"  [MOVE] {self.name} bergerak dengan kecepatan {self.speed}.")

    def attack(self, target: BaseCharacter):
        """
        INI BUKTI SUBTYPING: 
        Parameter 'target' tipenya BaseCharacter, jadi bisa diisi objek apa aja (Hayato, Yoru, dll).
        """
        print(f"  [ATTACK] {self.name} ({self.side}) menyerang {target.name}!")
        self.punch() # Pake kemampuan dari AttackMixin
        target.take_damage(10) # Skill Subtyping: nyerang siapapun yang bertipe BaseCharacter.

    def defend(self):
        # Aktifin mode block dari BlockMixin
        self.toggle_block(True) 

    def update(self):
        """Implementasi update biar class ini gak dianggap abstrak lagi sama Python."""
        pass

# ==========================================
# SPECIFIC CHARACTERS (Subclasses)
# ==========================================

# --- CHARACTER LIGHT ---

class Hayato(CrimsonFighter, UltimateSkillMixin, AnalyticalTraitMixin): # Warisin CrimsonFighter
    def __init__(self):
        # MC kita: Set stats seimbang pake super().
        super().__init__(name="Hayato", hp=100, speed=10, side="Light")

    def special_move(self, target):
        # Gabungan skill dari dua Mixin berbeda
        self.analyze_enemy(target) # Dari AnalyticalTraitMixin
        self.execute_ultimate(target) # Dari UltimateSkillMixin

class Mizunami(CrimsonFighter):
    def __init__(self):
        # Heroine: Fokus di kecepatan.
        super().__init__(name="Mizunami", hp=80, speed=15, side="Light")

class Kurogane(CrimsonFighter):
    def __init__(self):
        # Tanker faksi Light: HP paling tebel.
        super().__init__(name="Kurogane", hp=150, speed=5, side="Light")

# --- CHARACTER DARK ---

class Yoru(CrimsonFighter, UltimateSkillMixin):
    def __init__(self):
        # Assassin faksi Dark yang punya Ultimate.
        super().__init__(name="Yoru", hp=90, speed=12, side="Dark")

class Goro(CrimsonFighter):
    def __init__(self):
        # Karakter tipe Brute.
        super().__init__(name="Goro", hp=130, speed=7, side="Dark")

class Selene(CrimsonFighter):
    def __init__(self):
        # Tipe karakter Magic.
        super().__init__(name="Selene", hp=85, speed=11, side="Dark")