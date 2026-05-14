import random
from models.base import BaseAI

# ==========================================
# CONCRETE BASE AI (Inheritance)
# ==========================================

class SmartAI(BaseAI): # Mewarisi BaseAI (Inheritance )
    """
    Kelas dasar untuk logika kecerdasan buatan di Crimson Arena.
    """
    def __init__(self, difficulty="Normal"):
        # Hubungin ke constructor induk (Syarat super() )
        super().__init__() 
        self.difficulty = difficulty

    def decide_action(self, character):
        # Method ini wajib di-override sama anak-anaknya (Polymorphism)
        pass

# ==========================================
# AI SUBTYPES (Subtyping & Polymorphism)
# ==========================================

class RandomAI(SmartAI): # Subtype AI (Level 3) - Aksi acak 
    """
    Subtype AI yang memilih aksi secara acak.
    """
    def decide_action(self, character):
        actions = ["attack", "defend", "move"]
        choice = random.choice(actions)
        print(f"  [AI-Random] {character.name} ({self.difficulty}) memilih: {choice.upper()}.")
        return choice

class AggressiveAI(SmartAI): # Subtype AI (Level 3) - Nyederang terus 
    """
    Subtype AI yang fokus sepenuhnya pada serangan.
    """
    def __init__(self):
        # Maksa set kesulitan ke 'Hard' lewat super() 
        super().__init__(difficulty="Hard")

    def decide_action(self, character):
        print(f"  [AI-Aggressive] {character.name} terus menekan! Memilih ATTACK.")
        return "attack"

class AnalyticalAI(SmartAI): # Subtype AI (Level 3) - Strategis 
    """
    Subtype AI dengan pendekatan strategis dan analitis.
    """
    def decide_action(self, character):
        # Logika subtyping: Aksi beda tergantung kondisi HP
        if character.hp < 30:
            print(f"  [AI-Analytical] {character.name} menganalisis risiko tinggi... Memilih DEFEND.")
            return "defend"
        else:
            print(f"  [AI-Analytical] {character.name} melihat celah pertahanan lawan! Memilih ATTACK.")
            return "attack"