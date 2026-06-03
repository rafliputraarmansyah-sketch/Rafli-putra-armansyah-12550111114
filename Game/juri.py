
class Juri:
    def determine_winner(self, player, computer):
        if player == computer:
            print("Hasil: Seri!\n")
        elif (player == "batu" and computer == "gunting") or \
            (player == "gunting" and computer == "kertas") or \
            (player == "kertas" and computer == "batu"):
            print("Hasil: Menang!\n")
        else:
            print("Hasil: Kalah!\n")

