import random

class Player(object):
    """ Uczestnik gry. """
    def __init__(self, name, score = 0):
        self.name = name
        self.score = score

    def __str__(self):
        rep = self.name + ":\t" + str(self.score)
        return rep

def ask_yes_no(question):
    """Zadaj pytanie, na które można odpowiedzieć tak lub nie."""
    response = None
    while response not in ("t", "n"):
        response = input(question).lower()
    return response

def ask_number(question, low, high):
    """Poproś o podanie liczby z określonego zakresu."""
    response = None
    while response not in range(low, high):
        response = int(input(question))
    return response


print("Witaj w najprostszej grze na świecie!\n")
again = None
while again != "n":
    players = []
    num = ask_number(question="Podaj liczbę graczy (2 - 5): ", low=2, high=5)

    for i in range(num):
        name = input("Nazwa gracza: ")
        score = random.randrange(100) + 1
        player = Player(name, score)
        players.append(player)

    print("\nOto wyniki gry:")
    for player in players:
        print(player)

        again = ask_yes_no("\nCzy chcesz zagrać ponownie? (t/n): ")

input("\n\nAby zakończyć program, naciśnij klawisz Enter.")

