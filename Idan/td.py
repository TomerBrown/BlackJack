import os
import random
import numpy as np
from tqdm import tqdm

ALPHA = 0.5

class Blackjack(object):
    def __init__(self):
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4

    def new_deck(self):
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4

    def deal(self):
        hand = []
        for i in range(2):
            random.shuffle(self.deck)
            card = self.deck.pop()
            card = self.card_val(card)
            hand.append(card)
        return hand

    def card_val(self, card):
        if card == 11: card = "J"
        if card == 12: card = "Q"
        if card == 13: card = "K"
        if card == 14: card = "A"
        return card

    def total(self, hand):
        total = 0
        for card in hand:
            if card == "J" or card == "Q" or card == "K":
                total += 10
            elif card == "A":
                if total >= 11:
                    total += 1
                else:
                    total += 11
            else:
                total += card
        return total

    def hit(self, hand):
        card = self.deck.pop()
        if card == 11: card = "J"
        if card == 12: card = "Q"
        if card == 13: card = "K"
        if card == 14: card = "A"
        hand.append(card)
        return hand

    def score(self, dealer_hand, player_hand):
        if self.total(player_hand) == 21:
            return 1
        elif self.total(dealer_hand) == 21:
            return -1
        elif self.total(player_hand) > 21:
            return -1
        elif self.total(dealer_hand) > 21:
            return 1
        elif self.total(player_hand) < self.total(dealer_hand):
            return -1
        elif self.total(player_hand) > self.total(dealer_hand):
            return 1
        else:
            return -1

    def agent_game(self, T: int):
        num_wins = 0
        alpha_t = 1.0
        V = np.zeros(21)
        pbar = tqdm(range(1, T+1))
        for t in pbar:
            self.new_deck()
            player_hand = self.deal()
            dealer_hand = self.deal()
            s_t = self.total(player_hand)
            if s_t < 18:
                self.hit(player_hand)
            while self.total(dealer_hand) <= 15:
                self.hit(dealer_hand)
            r_t = self.score(dealer_hand, player_hand)
            if r_t == 1:
                num_wins += r_t
            pbar.set_description('percent_wins=%f.2' % (num_wins / t))
            # There is no state t+1
            V[s_t - 1] += alpha_t * (r_t - V[s_t - 1])
            # alpha_t /= np.log(t + 1)
            alpha_t = ALPHA / (t ** 0.5)  # np.log(t+1)
        return V

    def p_states(self):
        self.new_deck()
        states = []
        for i in range(len(self.deck)):
            self.new_deck()
            c1 = self.deck.pop(i)
            for j in range(len(self.deck)):
                c2 = self.deck.pop()
                s = self.total([self.card_val(c1), self.card_val(c2)])
                states.append(s)
        total_states = len(states)
        states = np.array(states)
        unique_states = np.sort(np.unique(states))
        states_prob = [None] * len(unique_states)
        for s in unique_states:
            count_s = np.count_nonzero(states == s)
            states_prob[s - 4] = count_s / total_states
        self.new_deck()
        return states_prob


def p_win(E_reward):
    """
    E_reward = p -(1-p) = 2p - 1 -> p = (E_reward + 1) / 2
    :param E_reward: Expected total reward with policy
    :return: Probability of winning with policy
    """
    p = (1 + E_reward) / 2
    return p


def p_win_state(V):
    """
    V(s) = p_s -(1-p_s) = 2p_s - 1 -> p_s = (V(s) + 1) / 2
    :param V: V function of optimal policy
    :return: Probability of winning with policy
    """
    p = (1 + V) / 2
    return p

if __name__ == "__main__":
    blackjack = Blackjack()
    V = blackjack.agent_game(10000)
    P = blackjack.p_states()
    print('Estimated reward')
    print(np.sum(V[3:] * P))
    print('Probability of winning')
    print(p_win(np.sum(V[3:] * P)))
    print('Probability of winning in state')
    print(p_win_state(V[3:]))
