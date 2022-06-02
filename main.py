from Deck import Deck, Card
from Game import Game
import random
from tqdm import trange

N_GAMES = 10**7
PLAYER_THRESHOLD = 18



def TD0():
    game = Game()

    # States are between  1-31 and initialized randomly and state 0 that is final
    V = {i:0 for i in range (0,32)}

    for i in trange(N_GAMES):
        game.new_game()
        game.execute_house()
        s = game.get_state()
        alpha_t = 1/ (i+1)
        while len(game.player_cards) <= 5 and s <= PLAYER_THRESHOLD:
            a = 1
            r = 0
            game.player_hit()
            s_prime = game.get_state()

            # Perform TD(0) updates
            V[s] = V[s] + alpha_t * (r + V[s_prime]-V[s])

            s = game.get_state()

        a = 0
        r = game.evaluate_winner()
        s_prime = 0
        V[s] = V[s] + alpha_t * (r + V[s_prime] - V[s])
    return V


if __name__ == '__main__':
    print(TD0())