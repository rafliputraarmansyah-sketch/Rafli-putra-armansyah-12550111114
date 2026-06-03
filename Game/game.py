from pilihan import Pilihan
from juri import Juri

class Game:
    
    def play_game(self):
        print("=== Game Batu Gunting Kertas ===")
        print("Ketik: batu / gunting / kertas")
        print("Ketik 'exit' untuk keluar\n")

        while True:
            player = input("Pilihan kamu: ").lower()

            if player == "exit":
                print("Terima kasih sudah bermain!")
                break

            if player not in ["batu", "gunting", "kertas"]:
                print("Input tidak valid, coba lagi.\n")
                continue

            obj_pilihan = Pilihan()
            computer = obj_pilihan.get_computer_choice()
            print(f"Komputer memilih: {computer}")

            obj_juri = Juri()
            obj_juri.determine_winner(player, computer)


if __name__ == "__main__":
    game = Game()   # membuat object game
    game.play_game()