from Deck import Deck, Card
from Game import Game
import random
from tqdm import trange
import numpy as np

N_GAMES = 10 ** 8
PLAYER_THRESHOLD = 18
# 21 states for sum of cards + 22 which is a state for all states over 21
N_STATES = 22
# For definition of theta - look at slide 32 on lecture 6
THETA = 1


def TD0():
    game = Game()

    # States are between  1-31 and initialized randomly and state 0 that is the initial state and -1 is the final state
    # From state -1 you always transition to state 0
    V = {i: 0 for i in range(-1, N_STATES + 1)}

    for i in trange(N_GAMES):

        alpha_t = 1 / (i + 1)

        # Execute A new game
        game.new_game()
        game.execute_house()
        s = game.get_state()

        # Update value of initial state 0 to see how good it is as
        V[0] = V[0] + alpha_t * (V[s] - V[0])
        while len(game.player_cards) <= 5 and s < PLAYER_THRESHOLD:
            a = 1
            r = 0
            game.player_hit()
            s_prime = game.get_state()

            # Perform TD(0) updates
            V[s] = V[s] + alpha_t * (r + V[s_prime] - V[s])

            s = game.get_state()

        a = 0
        r = game.evaluate_winner()
        s_prime = -1
        V[s] = V[s] + alpha_t * (r + V[s_prime] - V[s])
    return V


def epsilon_greedy(Q, s, epsilon=0.1):
    if Q[(s, 0)] < Q[(s, 1)]:
        best_action = 1
        worse_action = 0

    if Q[(s, 0)] == Q[(s, 1)]:
        best_action = random.randint(0, 1)
        worse_action = 1 - best_action

    else:
        best_action = 0
        worse_action = 1

    if random.random() < epsilon:
        return worse_action

    return best_action


def update_Q (Q, s, a, r, next_s, next_a, count_sa):
    count_sa[(s, a)] += 1
    Gamma_t = r + Q[(next_s, next_a)] - Q[(s, a)]
    alpha_t = 1 / count_sa[(s, a)]
    Q[(s, a)] = Q[(s, a)] + alpha_t * Gamma_t


def SARSA():
    game = Game()
    # Initialize Q function
    sa_combination = [(s, a) for s in range(N_STATES +1) for a in range(2)]

    # Initialize Q value to 0 for each pair of state and action , and policy randomly
    Q = {(s, a): 0 for s, a in sa_combination}
    count_sa = {(s, a): 0 for s, a in sa_combination}

    for t in trange(N_GAMES):

        # parameters for current iteration
        eps_t = 1 / ((t + 1) ** THETA)

        # Execute A new game
        game.new_game()
        game.execute_house()
        s = game.get_state()

        next_a = epsilon_greedy(Q, s, eps_t)
        while len(game.player_cards) <= 5 and next_a == 1:
            # SARSA sampling
            s = game.get_state()
            a = next_a
            r_t = 0
            game.player_hit()
            next_s = game.get_state()
            next_a = epsilon_greedy(Q, s, eps_t)

            update_Q(Q, s, a, r_t, next_s, next_a, count_sa)

        s = game.get_state()
        a = next_a
        r_t = game.evaluate_winner()
        next_s = 0
        next_a = epsilon_greedy(Q, s, eps_t)
        update_Q(Q, s, a, r_t, next_s, next_a, count_sa)

    return Q


if __name__ == '__main__':
    print('-'*25, "TD0", '-'*25)
    V = TD0()
    for key, value in V.items():
        print(f"{key}:{value}")

    print('-' * 24, "SARSA", '-' * 24)
    Q = SARSA()
    policy = {}
    for s in range(N_STATES+1):
        policy[s] = 0 if Q[(s,0)] >= Q[(s,1)] else 1
        print(f"state: {s} | Q for stop(0): {round(Q[(s,0)],2)}  |  Q for hit (1):{round(Q[(s,1)],2)}  | pi({s}) = {policy[s]}")

