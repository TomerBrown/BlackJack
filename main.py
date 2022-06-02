from Deck import Deck, Card
from Game import Game

if __name__ == '__main__':

    game = Game()
    print(game.simulate(player_threshold=18))
    #print(sum(game.player_cards))