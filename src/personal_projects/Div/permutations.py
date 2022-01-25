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


if __name__ == '__main__':
    N = 10
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
