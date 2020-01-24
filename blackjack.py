import cards, games


class BjCard(cards.Card):
    ace_value = 1

    @property
    def value(self):
        if self.is_face_up:
            v = BjCard.RANKS.index(self.rank) + 1
            if v > 10:
                v = 10
        else:
            v = None
        return v


class BjDeck(cards.Deck):
    """ Talia kart do blackjacka. """

    def populate(self):
        for suit in BjCard.SUITS:
            for rank in BjCard.RANKS:
                self.cards.append(BjCard(rank, suit))


class BjHand(cards.Hand):
    """ Ręka w blackjacku. """

    def __init__(self, name):
        super(BjHand, self).__init__()
        self.name = name

    def __str__(self):
        rep = self.name + ":\t" + super(BjHand, self).__str__()
        if self.total:
            rep += "(" + str(self.total) + ")"
        return rep

    @property
    def total(self):
        # jeśli karta w ręce ma wartość None, to i wartość sumy wynosi None
        for card in self.cards:
            if not card.value:
                return None

        # zsumuj wartości kart, traktuj każdego asa jako 1
        t = 0
        for card in self.cards:
            t += card.value

        # ustal, czy ręka zawiera asa
        contains_ace = False
        for card in self.cards:
            if card.value == BjCard.ace_value:
                contains_ace = True

        # jeśli ręka zawiera asa, a suma jest wystarczająco niska,
        # potraktuj asa jako 11
        if contains_ace and t <= 11:
            # dodaj tylko 10, ponieważ już dodaliśmy 1 za asa
            t += 10

        return t

    def is_busted(self):
        return self.total > 21


class BjPlayer(BjHand):
    """ Gracz w blackjacku. """

    def is_hitting(self):
        response = games.ask_yes_no("\n" + self.name + ", chcesz dobrać kartę? (T/N): ")
        return response == "t"

    def bust(self):
        print(self.name, "ma furę.")
        self.lose()

    def lose(self):
        print(self.name, "przegrywa.")

    def win(self):
        print(self.name, "wygrywa.")

    def push(self):
        print(self.name, "remisuje.")


class BjDealer(BjHand):
    """ Rozdający w blackjacku. """

    def is_hitting(self):
        return self.total < 17

    def bust(self):
        print(self.name, "ma furę.")

    def flip_first_card(self):
        first_card = self.cards[0]
        first_card.flip()


class BjGame(object):
    """ Gra w blackjacka. """

    def __init__(self, names):
        self.players = []
        for name in names:
            player = BjPlayer(name)
            self.players.append(player)

        self.dealer = BjDealer("Rozdający")

        self.deck = BjDeck()
        self.deck.populate()
        self.deck.shuffle()

    @property
    def still_playing(self):
        sp = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp

    def __additional_cards(self, player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust()

    def play(self):
        # rozdaj każdemu początkowe dwie karty
        self.deck.deal(self.players + [self.dealer], per_hand=2)
        self.dealer.flip_first_card()  # ukryj pierwszą kartę rozdającego
        for player in self.players:
            print(player)
        print(self.dealer)

        # rozdaj graczom dodatkowe karty
        for player in self.players:
            self.__additional_cards(player)

        self.dealer.flip_first_card()  # odsłoń pierwszą kartę rozdającego

        if not self.still_playing:
            # ponieważ wszyscy gracze dostali furę, pokaż tylko rękę rozdającego
            print(self.dealer)
        else:
            # daj dodatkowe karty rozdającemu
            print(self.dealer)
            self.__additional_cards(self.dealer)

            if self.dealer.is_busted():
                # wygrywa każdy, kto jeszcze pozostaje w grze
                for player in self.still_playing:
                    player.win()
            else:
                # porównaj punkty każdego gracza pozostającego w grze z punktami rozdającego
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        player.win()
                    elif player.total < self.dealer.total:
                        player.lose()
                    else:
                        player.push()

        # usuń karty wszystkich graczy
        for player in self.players:
            player.clear()
        self.dealer.clear()


def main():
    print("\t\tWitaj w grze 'Blackjack'!\n")

    names = []
    number = games.ask_number("Podaj liczbę graczy (1 - 7): ", low=1, high=8)
    for i in range(number):
        name = input("Wprowadź nazwę gracza: ")
        names.append(name)
    print()

    game = BjGame(names)

    again = None
    while again != "n":
        game.play()
        again = games.ask_yes_no("\nCzy chcesz zagrać ponownie?: ")


main()
input("\n\nAby zakończyć program, naciśnij klawisz Enter.")
