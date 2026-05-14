from abc import ABC, abstractmethod

# ==========================================
# KONTRAK UTAMA (Abstract Base Class)
# ==========================================

class BaseCharacter(ABC): # Kelas induk abstrak (Gak bisa dibikin objek langsung)
    def __init__(self, name, hp):
        # Inisialisasi dasar buat semua karakter
        self.name = name
        self.hp = hp

    @abstractmethod
    def move(self): 
        # Wajib diisi sama kelas anak 
        pass

    @abstractmethod
    def attack(self, target): 
        # Target pake BaseCharacter biar bisa nyerang siapa aja (Subtyping) 
        pass 

    @abstractmethod
    def defend(self): pass

    @abstractmethod
    def take_damage(self, amount): 
        # Kontrak wajib buat ngurangin darah 
        pass

    @abstractmethod
    def update(self): pass

class BaseAttack(ABC): # Blueprint buat sistem serangan 
    @abstractmethod
    def execute(self, attacker, target): 
        # Logic serangan antara penyerang & target 
        pass 
    
    @abstractmethod
    def get_damage(self): pass

class BaseState(ABC): # Kontrak buat status karakter (Idle, Attack, dll)
    @abstractmethod
    def enter(self, character): pass 

    @abstractmethod
    def update(self, character): pass

    @abstractmethod
    def exit(self, character): pass

class BaseAI(ABC): # Standar buat otak musuh
    @abstractmethod
    def decide_action(self, character): 
        # AI bakal nentuin gerak apa 
        pass