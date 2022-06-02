import random
from collections import deque


class Card:
    def __init__(self, number:int, shape: str):
        self.number = number
        self.shape = shape

    def value(self)->int:
        """ :returns the value of the card when playing blackjack"""
        if self.number == 1:
            return 11
        else:
            return min(10, self.number)

    def __repr__(self):
        return f"{self.number}  {self.shape}"

    def __add__(self, other):
        return self.value() + other.value()

    def __radd__(self, other):
        if type(other) == int:
            return other + self.value()
        return self.value() + other.value()

class Deck:

    def __init__(self):
        self.deck = deque()
        self.reset()

    def __len__(self):
        return len(self.deck)

    def draw(self):
        return self.deck.pop()

    def reset(self):
        """Shuffle a new deck"""
        self.deck = deque()
        shapes = ['heart', 'spade', 'diamond', 'clubs']
        for num in range(1, 14):
            for shape in shapes:
                self.deck.append(Card(num, shape))
        random.shuffle(self.deck)