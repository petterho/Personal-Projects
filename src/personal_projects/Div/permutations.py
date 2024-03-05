"""
This is all for coins not landing on the sides. It is always assumed that
there is only two possible outcomes.
"""


# import numpy as np
import math as m
import matplotlib.pyplot as plt


def perm_coin_toss(n, d):
    if d < 1:
        a_1 = int(n*d)
        a_2 = n - a_1
    elif type(d) is int:
        a_1 = d
        a_2 = n - a_1
    else:
        raise TypeError

    w = m.factorial(n) / (m.factorial(a_1) * m.factorial(a_2))
    return w


def sum_perm(n):
    sum_w = 0
    for i in range(n+1):
        sum_w += perm_coin_toss(n, i)
    return sum_w


def prob_coin_toss(n, d):
    w = perm_coin_toss(n, d)
    sigma_w = sum_perm(n)
    return w/sigma_w


def coin_tossing():
    N = 100
    D = [d for d in range(N + 1)]
    sum_of_w = sum_perm(N)
    prob = []
    for a in D:
        W = perm_coin_toss(N, a)
        p_a = W / sum_of_w
        prob.append(p_a)

    plt.plot(D, prob)
    plt.show()

    print(sum(prob))

    print(perm_coin_toss(52, 5))


def card_permutations(number_of_cards=4, number_of_aces=2, last_ace_by=2):
    if last_ace_by < number_of_aces:
        return 0

    """
    permutations_numerator = perm_coin_toss(last_ace_by, number_of_aces)
    permutations_divisor = perm_coin_toss(number_of_cards, number_of_aces)
    favorable_permutations_fraction = permutations_numerator / \
                                      permutations_divisor
    print(favorable_permutations_fraction)
    total_chance = favorable_permutations_fraction
    """

    total_chance_numerator = m.factorial(last_ace_by) * \
                             m.factorial(number_of_cards - number_of_aces)
    total_chance_divisor = m.factorial(number_of_cards) * \
                           m.factorial(last_ace_by - number_of_aces)

    return total_chance_numerator / total_chance_divisor


def card_permutations_exact_placement(number_of_cards=4, number_of_aces=2,
                                      last_ace_on=3):
    chance_by_this = card_permutations(number_of_cards, number_of_aces,
                                       last_ace_on)
    chance_by_last = card_permutations(number_of_cards, number_of_aces,
                                       last_ace_on - 1)
    return chance_by_this - chance_by_last


def card_picking():
    num = 52
    aces = 4
    chance = []
    pick_at = []
    for i in range(num + 1):
        pick_at.append(i)
        chan = card_permutations_exact_placement(num, aces, i)
        chance.append(chan)
    summation = sum(chance)
    print(f'Sum should be 1: {summation}')
    plt.plot(pick_at, chance)
    plt.show()


if __name__ == '__main__':
    card_picking()
