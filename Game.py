from Deck import Deck

THRESHOLD_HOUSE = 15


class Game:

    def __init__(self):
        self.deck = Deck()
        self.house_cards = []
        self.player_cards = []

    def new_game(self):
        self.deck.reset()
        self.house_cards = []
        self.player_cards = []
        for i in range(2):
            self.house_cards.append(self.deck.draw())
            self.player_cards.append(self.deck.draw())

    def execute_house(self):
        while len(self.house_cards) <= 5 and sum(self.house_cards) <= THRESHOLD_HOUSE:
            self.house_cards.append(self.deck.draw())

    def execute_player (self , player_threshold):
        while (len(self.player_cards) <= 5) and sum(self.player_cards) < player_threshold:
            card = self.deck.draw()
            self.player_cards.append(card)

    def evaluate_winner(self):
        sum_house = sum(self.house_cards)
        sum_player = sum(self.player_cards)

        # If both over 21 or it's a tie: it is a draw (0)
        if sum_house > 21 and sum_player > 21 or sum_house == sum_player:
            return 0

        # If only player is over 21: it is a lose(-1)
        if sum_house<= 21 and sum_player > 21:
            return -1

        # If only house is over: 21 it is a win(+1)
        if sum_house> 21 and sum_player <= 21:
            return 1

        # otherwise if player>house it is a win ,and otherwise a lose
        return 1 if sum_player>sum_house else -1

    def __repr__(self):
        s1 = f"House Cards : {self.house_cards} - sum = {sum(self.house_cards)}\n"
        s2 = f"Player Cards : {self.player_cards} - sum = {sum(self.player_cards)}"
        return s1+s2

    def simulate(self, player_threshold):
        self.new_game()
        self.execute_house()
        self.execute_player(player_threshold)
        return self.evaluate_winner()

