from models.base import BaseState

# ==========================================
# IMPLEMENTASI SUBTYPING & INHERITANCE
# ==========================================

class IdleState(BaseState): # Turunan dari BaseState (Inheritance)
    """State saat karakter sedang diam/siaga."""
    def __init__(self):
        # Manggil bapaknya biar konek (konsep super())
        super().__init__()

    def enter(self, character):
        # Dipanggil pas karakter mulai diem
        print(f"  [STATE] {character.name} masuk ke mode IDLE.")

    def update(self, character):
        # Logic pas lagi diem (misal: isi stamina pelan-pelan)
        pass

    def exit(self, character):
        # Pas ganti ke state lain
        pass


class AttackState(BaseState): # Subtype dari BaseState
    """State saat karakter sedang melakukan serangan."""
    def enter(self, character):
        print(f"  [STATE] {character.name} masuk ke mode ATTACK!")

    def update(self, character):
        # Logic pas lagi ngayun pedang/mukul
        pass

    def exit(self, character):
        print(f"  [STATE] {character.name} selesai menyerang.")


class HitState(BaseState): # Subtype dari BaseState
    """State pas karakter bonyok/kena pukul."""
    def enter(self, character):
        print(f"  [STATE] {character.name} TERKENA HIT! (Stunned)")

    def update(self, character):
        # Pas lagi kena hit, biasanya karakter gak bisa gerak
        pass

    def exit(self, character):
        print(f"  [STATE] {character.name} pulih dari stun.")

# ==========================================
# STATE MACHINE (Mendemonstrasikan Subtyping)
# ==========================================

class StateMachine:
    def __init__(self, character):
        self.character = character
        self.current_state = IdleState() # Default-nya diem dulu

    def change_state(self, new_state: BaseState):
        """
        INI CONTOH NYATA SUBTYPING:
        Metode ini nerima tipe 'BaseState'. 
        Tapi praktiknya, kita bisa masukin IdleState, AttackState, atau HitState.
        Jadi kodenya fleksibel (Interchangeable).
        """
        if self.current_state:
            self.current_state.exit(self.character) # Keluar dari state lama
        
        self.current_state = new_state # Masuk ke state baru (Subtyping beraksi)
        self.current_state.enter(self.character)

    def update(self):
        # Update state yang lagi aktif sekarang
        if self.current_state:
            self.current_state.update(self.character)